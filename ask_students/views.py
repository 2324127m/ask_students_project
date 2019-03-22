import urllib
import json

from ask_students.models import Category, Question, Answer, UserProfile, User
from ask_students.forms import UserProfileForm, RequestCategoryForm, AskQuestionForm, AnswerForm, ApproveCategoryForm, \
    SelectAnswerForm, EditQuestionForm

from django.shortcuts import render, redirect, reverse
from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.contrib.sites.shortcuts import get_current_site
from django.core.paginator import Paginator, InvalidPage
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import get_user_model

from datetime import datetime, timedelta

from registration.backends.default.views import RegistrationView, ActivationView
from registration.forms import RegistrationFormUniqueEmail
from registration import signals


# Required For Register Method
UserModel = get_user_model()


# Custom View To Handle User/UserProfile Dependency
class MyRegistrationView(RegistrationView):
    form_class = RegistrationFormUniqueEmail

    # Almost entirely a copy of django-registration-redux register
    # but also creates a profile for every user to ensure
    # this dependency condition is met.
    def register(self, form):

        site = get_current_site(self.request)

        if hasattr(form, 'save'):
            new_user_instance = form.save()
        else:
            new_user_instance = (UserModel().objects
                                 .create_user(**form.cleaned_data))

        new_user = self.registration_profile.objects.create_inactive_user(
            new_user=new_user_instance,
            site=site,
            send_email=self.SEND_ACTIVATION_EMAIL,
            request=self.request,
        )
        signals.user_registered.send(sender=self.__class__,
                                     user=new_user,
                                     request=self.request)

        # Create a Dependent User
        profile = UserProfile()
        profile.user = new_user
        new_user.profile = profile
        profile.save()

        return new_user

# Override Activation View To Redirect To My Profile Edit Page On Activation.
# We want to encourage people to fill out their profile.
class MyActivationView(ActivationView):
    # Override On Success To Take To Edit Profile
    def get_success_url(self, user):
        return 'my_profile', (), {}


def index(request):

    # Get top questions in past week
    past_week = timezone.now() - timedelta(days=7)

    top_questions_list = Question.objects.filter(posted__gte=past_week).order_by('-views')[:10]

    # Oldest unanswered question first
    unanswered_questions_list = Question.objects.filter(answered=None).order_by('posted')[:10]

    context_dict = {'top_questions': top_questions_list,
                    'unanswered_questions': unanswered_questions_list
                    }

    return render(request, 'ask_students/index.html', context_dict)


# SHOW CATEGORIES
def category(request, category_name_slug):

    context_dict = {}

    try:
        category_obj = Category.objects.get(slug=category_name_slug)
        context_dict['category'] = category_obj

        question_list = Question.objects.filter(category=category_obj).order_by('-posted')
        question_paginator = Paginator(question_list, 10)  # Where second argument is max questions per page.

        # Get ?page=xxx from request and return that page in the context_dict to template
        requested_page = request.GET.get('page')

        # If request does not specify a page, choose first page.
        if requested_page is None:
            requested_page = 1

        question_page = question_paginator.page(requested_page)
        # Above Throws InvalidPage if no valid questions to display.

        context_dict['questions'] = question_page

    # We Want To Send Null Values To Template On Failure To Find Request
    except Category.DoesNotExist:
        context_dict['category'] = None
        context_dict['questions'] = None

    # If there's no valid page, return null, we'll handle in template.
    except InvalidPage:
        context_dict['questions'] = None

    return render(request, 'ask_students/category.html', context_dict)


@login_required
def add_question(request):
    context_dict = {}

    # Fetch All Categories
    categories = Category.objects.all()
    form = AskQuestionForm()

    # Set Up Context For Later Returns
    context_dict['form'] = form
    context_dict['categories'] = categories

    # If POSTING
    if request.method == 'POST':
        form = AskQuestionForm(request.POST)
        if form.is_valid():

            # FETCH RECAPTCHA VALIDATION RESULTS
            # NOTE :  RECAPTCHA DOES NOT WORK ON PYTHON ANYWHERE AS THEY WHITELIST ALLOWED APIS
            #           WE MUST REMOVE THIS TO USE ON PYTHON ANYWHERE
            recaptcha_response = request.POST.get('g-recaptcha-response')

            # Where do we query for validation
            url = 'https://www.google.com/recaptcha/api/siteverify'

            values = {
                'secret': '6LcqVZkUAAAAAMhBsxELP97pi_G_xNsvfXosUMdr',
                'response': recaptcha_response
            }

            # Parse Results
            data = urllib.parse.urlencode(values).encode()
            req = urllib.request.Request(url, data=data)
            response = urllib.request.urlopen(req)
            result = json.loads(response.read().decode())

            # If reCAPTCHA says no
            if not result['success']:

                # Then lets return an error in the form and ask user to resubmit.
                form.add_error(None, "Invalid ReCAPTCHA Response, Try Again")
                return render(request, 'ask_students/add_question.html', context_dict)

            # END OF THE RECAPTCHA CONTENT

            # Otherwise, form and captcha are valid, lets save!
            question = form.save(commit=True)
            question.posted = datetime.now()
            up = UserProfile.objects.get(user=request.user)
            question.user = up

            # If user has uploaded a file, then lets add it to their question
            if 'support_file' in request.FILES:
                question.support_file = request.FILES['support_file']

            question.save()

            category_name = form.cleaned_data['category']
            category_slug = Category.objects.get(name=category_name).slug

            return HttpResponseRedirect(reverse('show_question', kwargs={'category_name_slug': category_slug,
                                                                         'question_id': question.pk}))

    # If we're not saving a new question, return the form to the add question view
    # with errors if appropriate.
    return render(request, 'ask_students/add_question.html', context_dict)


# QUESTION PAGE
def show_question(request, category_name_slug, question_id):
    context_dict = {}

    # Default Value
    was_question_answered = False
    try:
        # Get Question from id in URL
        question = Question.objects.get(pk=question_id)

        try:
            user_profile = UserProfile.objects.get(user=request.user)  # user_profile is ALWAYS the requester's profile

        except UserProfile.DoesNotExist:
            # This User Somehow Doesn't Have a Profile, Exit Gracefully.
            user_profile = None

        except TypeError:
            # This can happen when request user is anonymous, so once again, obviously no profile
            user_profile = None

        # Basic Handling Of View Count
        # Iterates if there is no vq_id key set for user session
        if request.method == 'GET' and not ('vq_%s' % question.id) in request.session:
            request.session['vq_%s' % question.id] = True
            question.views += 1
            question.save()

        # If method of the request is POST, then a user posting an answer to the question
        if request.method == 'POST':
            form = AnswerForm(request.POST)

            if form.is_valid():
                # Then lets start making the answer.
                answer = form.save(commit=False)
                answer.category = Category.objects.get(slug=category_name_slug)
                answer.questiontop = question
                answer.user = user_profile

                # If question is anonymous and answerer is the original asker
                # then answer has no user, template will show anonymous
                if question.anonymous and question.user == user_profile:
                    answer.anonymous = True

                answer.save()

                was_question_answered = True

        # Earliest answer first list of answers.
        answers_list = Answer.objects.filter(questiontop=question).order_by('-likes')

        if user_profile is not None:
            # Lets set up the users likes and dislikes to display to them on page.
            user_liked_answers = list(answers_list.filter(up_voters=user_profile))
            user_disliked_answers = list(answers_list.filter(down_voters=user_profile))

            user_liked_answers = [x.pk for x in user_liked_answers]
            user_disliked_answers = [y.pk for y in user_disliked_answers]

            context_dict['liked'] = user_liked_answers
            context_dict['disliked'] = user_disliked_answers
        else:
            # If the user has no profile (i.e. anonymous) they don't have any already set likes/dislikes.
            context_dict['liked'] = None
            context_dict['disliked'] = None

        # Lets get the selected answer if there is one.
        new_answers_list = []

        if question.answered is not None:

            selected_answer = Answer.objects.get(pk=question.answered.pk)
            new_answers_list.append(selected_answer)
            for item in answers_list:
                if item != selected_answer:
                    new_answers_list.append(item)

            context_dict['selected_answer'] = True

        else:
            # there isn't a selected answer, return none.
            context_dict['selected_answer'] = None

        context_dict['question'] = question
        if context_dict['selected_answer']:
            context_dict['answers_list'] = new_answers_list
            context_dict['number_of_answers'] = len(new_answers_list)

        else:
            context_dict['answers_list'] = answers_list
            context_dict['number_of_answers'] = len(answers_list)

        try:
            # Lets try to get the profile of the question asker.
            asker_profile = UserProfile.objects.get(pk=question.user.pk)
            context_dict['asker_profile'] = asker_profile

        # Multiple exceptions, if question has not user or user does not exist
        except:
            context_dict['asker_profile'] = None

        if question.answered is not None:
            context_dict['answer'] = question.answered
        else:
            context_dict['answer'] = None

        # Init a form to let the current user add a new answer to this question.
        answer_form = AnswerForm

        # Add the form to context dictionary
        context_dict['answer_form'] = answer_form

    except Question.DoesNotExist:
        # This request is invalid, send null to template.
        context_dict['question'] = None
        context_dict['answers_list'] = None

    if was_question_answered:
        if category_name_slug and question_id:
            return HttpResponseRedirect(reverse('show_question', kwargs={'category_name_slug': category_name_slug,
                                                                         'question_id': question_id}))

    return render(request, 'ask_students/question.html', context_dict)


@login_required
def delete_question(request, question_id):
    question = Question.objects.get(pk=question_id)

    # Check user requesting to delete is user who posted question
    if request.user == question.user.user:
        question.delete()

    return redirect('index')


@login_required
def delete_answer(request, question_id, answer_id):

    answer = Answer.objects.get(pk=answer_id)
    question = Question.objects.get(pk=question_id)

    # Check user requesting to delete is user who posted answer
    if request.user == answer.user.user:
        # Delete the number of likes and dislikes from overall user likes and dislikes
        user_profile = answer.user
        user_profile.likes -= answer.likes
        user_profile.dislikes -= answer.dislikes
        user_profile.save()

        answer.delete()

    return redirect('show_question', category_name_slug=question.category.slug, question_id=question.pk)


@login_required
def edit_question(request, question_id):

    try:
        question = Question.objects.get(pk=question_id)
        form = EditQuestionForm()

    except Question.DoesNotExist:
        return redirect('index')

    if request.method == 'POST':
        form = EditQuestionForm(request.POST, request.FILES, instance=question)
        if form.is_valid():
            question = form.save(commit=False)
            question.edited = timezone.now()
            question.save()

            return HttpResponseRedirect(reverse('show_question', kwargs={'category_name_slug': question.category.slug,
                                                                         'question_id': question_id}))

    return render(request, 'ask_students/edit_question.html', {'form': form, 'old_question': question,
                                                               'categories': Category.objects.all().filter(
                                                                   approved=True)})


@login_required
def edit_answer(request, answer_id):
    try:
        answer = Answer.objects.get(pk=answer_id)
        form = AnswerForm()

    except Answer.DoesNotExist:
        return redirect('index')

    if request.method == 'POST':
        form = AnswerForm(request.POST, instance=answer)

        if form.is_valid():
            answer = form.save(commit=False)
            answer.edited = timezone.now()
            answer.text = request.POST['text']
            answer.save()

            return HttpResponseRedirect(reverse('show_question', kwargs={'category_name_slug': answer.category.slug,
                                                                         'question_id': answer.questiontop_id}))
        else:
            print(form.errors)

    return render(request, 'ask_students/edit_answer.html', {'form': form, 'old_answer': answer.text})


@login_required
def request_category(request):

    form = RequestCategoryForm()

    if request.method == 'POST':
        form = RequestCategoryForm(request.POST)

        if form.is_valid():
            category = form.save(commit=False)
            up = UserProfile.objects.get(user=request.user)
            category.user = up
            category.save()
            return render(request, 'ask_students/category_requested.html', {})

    return render(request, 'ask_students/request_category.html', {'form': form})


@login_required
def select_answer(request, question_id):
    q = Question.objects.get(pk=question_id)
    form = SelectAnswerForm()
    answers = Answer.objects.filter(questiontop=q)

    if request.method == 'POST':
        form = SelectAnswerForm(request.POST)

        if form.is_valid():
            a = form.save(commit=False)
            q.answered = Answer.objects.get(pk=a.answered.pk)
            q.save()
            return redirect('show_question', category_name_slug=q.category.slug, question_id=q.pk)

    return render(request, 'ask_students/select_answer.html', {'form': form, 'question' : q, 'answers': answers,})


def profile(request, username):
    # Set Defaults For Context
    user = None
    most_liked_answers = None
    number_of_answers = None
    this_user_email = None
    likes = None
    dislikes = None
    role = "Student"

    # Get user, if doesn't exist -> redirect to home page
    try:
        user = User.objects.get(username=username)

    except User.DoesNotExist:
        return redirect('index')

    joined = user.date_joined.date()
    all_answers = Answer.objects.filter(user=user.pk)
    most_liked_answers = all_answers.order_by('-likes')[:5]
    number_of_answers = len(all_answers)
    this_user_email = user.email
    this_profile = UserProfile.objects.get(user=user)
    user_permission = this_profile.permission
    likes = this_profile.likes
    dislikes = this_profile.dislikes

    if user_permission is not None:
        # Adding a permission via admin interface causes error here
        # Permission.objects.filter(pk=user_permission)
        role = user_permission.title

    # select user's profile instance or create a blank one
    # users_profile = UserProfile.objects.get_or_create(user=user)[0]

    context_dict = {'this_user': user, 'top_five_answers': most_liked_answers, 'likes': likes, 'dislikes': dislikes,
                    'number_of_answers': number_of_answers, 'role': role, 'this_profile': this_profile,
                    'this_user_email' : this_user_email, 'date_joined': joined}

    return render(request, 'ask_students/profile.html', context_dict)


@login_required
def my_profile(request):
    try:
        user = User.objects.get(username=request.user)

    except User.DoesNotExist:
        return redirect('index')

    user_profile = UserProfile.objects.get(user=user)
    form = UserProfileForm(initial={'bio': user_profile.bio,
                                    'image': user_profile.image,
                                    'place_of_study': user_profile.place_of_study,
                                    'permission': user_profile.permission
                                    })

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)

        if form.is_valid():
            form.save(commit=True)
            return redirect('profile', user.username)

    return render(request, 'ask_students/my_profile.html',
                  {'user_profile': user_profile, 'selected_user': user, 'form': form})


@login_required
def delete_user_profile(request, user_id):
    user_profile = UserProfile.objects.get(pk=user_id)
    user = user_profile.user

    # Check user requesting to delete is the user who will be deleted
    if request.user == user:
        user_profile.delete()
        user.delete()

    return redirect('index')


@login_required
def register_profile(request):
    form = UserProfileForm()

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            users_profile = form.save(commit=False)
            users_profile.user = request.user
            users_profile.save()
            return render(request, 'registration/registration_complete.html', {})
        else:
            print(form.errors)

    context_dict = {"form": form}

    return render(request, 'ask_students/profile_registration.html', context_dict)


def faq(request):
    return render(request, 'ask_students/faq.html', {})


def about_us(request):
    return render(request, 'ask_students/about_us.html', {})


def contact_us(request):
    return render(request, 'ask_students/contact_us.html', {})


def search(request):
    if request.is_ajax():
        query = request.GET.get('term', '')
        queryset = Question.objects.filter(name__istartswith=query)
        querylist = queryset.order_by('views')[:7]
        results = []

        for result in querylist:
            out = dict()
            out['label'] = result.name
            out['url'] = "/category/" + result.category.slug + "/" + str(result.id)
            results.append(out)

        data = json.dumps(results)
        mt = 'application/json'

        return HttpResponse(data, mt)

    else:

        search_query = request.GET.get('q')
        context_dict = {}

        if search_query:
            search_terms = search_query.split()
            questions = Question.objects.filter(name__icontains=search_terms[0])
            answers = Answer.objects.filter(text__icontains=search_terms[0])

            for term in search_terms[1:]:
                questions = questions & Question.objects.filter(name__icontains=term)
                answers = answers & Answer.objects.filter(text__icontains=term)

            for answer in answers:
                questions = questions | Question.objects.filter(id=answer.questiontop_id)

            results = list(questions)

            try:
                paginator = Paginator(results, 8)

                # Get ?page=xxx from request and return that page in the context_dict
                requested_page = request.GET.get('page')

                # If request does not specify a page, choose first page.
                if requested_page is None:
                    requested_page = 1

                page = paginator.page(requested_page)  # Throws InvalidPage if no valid questions to display.
                context_dict['search_results'] = page

            # If there's no valid page, return null, we'll handle in template.
            except InvalidPage:
                context_dict['search_results'] = None

        # Pass this back for further page display
        context_dict['query'] = search_query
        return render(request, 'ask_students/search.html', context_dict)


@login_required
def vote(request):
    try:
        user_profile = request.user.userprofile

    except UserProfile.DoesNotExist:
        return redirect('register_profile')

    # Request must be AJAX, and if its not a secure POST with valid CSRF, we ain't interested.
    if request.is_ajax() and request.method == 'POST':
        try:
            # Parse the answer we need to change.
            answer = request.POST.get('answer_id')
            answer = int(answer.strip('dislike-btn-').strip('like-btn-'))
            answer = Answer.objects.get(pk=answer)

            # Get the profile we need to update dis/likes on
            answerer_profile = answer.user

            # And what kind of vote is this user placing.
            vote = int(request.POST.get('vote'))

            # Feedback to client what action server took, defaults to no action
            action = ""

            # I clicked like!
            if vote == 1:
                if user_profile not in answer.up_voters.all():
                    # I'm not currently liking this
                    if user_profile in answer.down_voters.all():
                        # But I already dislike this, time to change that.
                        decr_dislikes(answer, answerer_profile)
                        answer.down_voters.remove(user_profile)

                    # Now make me a liker!
                    incr_likes(answer, answerer_profile)
                    answer.up_voters.add(user_profile)
                    action = "like"

                # I currently have a like, but I've changed my mind.
                else:
                    decr_likes(answer, answerer_profile)
                    answer.up_voters.remove(user_profile)
                    action = "remove"

            # I clicked dislike
            elif vote == 0:
                if user_profile not in answer.down_voters.all():
                    # I'm not in the downvoters pool

                    if user_profile in answer.up_voters.all():
                        # But I am currently a liker, time to change that.
                        decr_likes(answer, answerer_profile)
                        answer.up_voters.remove(user_profile)

                    # Make me a hater
                    incr_dislikes(answer, answerer_profile)
                    answer.down_voters.add(user_profile)
                    action = "dislike"

                # I have a dislike, but I've changed my mind, remove it!
                else:
                    decr_dislikes(answer, answerer_profile)
                    answer.down_voters.remove(user_profile)
                    action = "remove"

            # Commit any changes to DB
            answer.save()
            answerer_profile.save()
            user_profile.save()

            # Lets send back the new likes/dislikes for the page to display
            response = {"likes": answer.likes,
                        "dislikes": answer.dislikes,
                        "answer_id": answer.id,
                        "action": action}

            response = json.dumps(response)

            return HttpResponse(response)

        except Answer.DoesNotExist:
            # This is an ASYNC error response
            return HttpResponseNotFound("Specified Answer Not Found")


# Helper Functions NOTE THESE DON'T SAVE STATE
def decr_likes(answer, answerer_profile):
    if answer.likes > 0:
        answer.likes -= 1

    if answerer_profile.likes > 0:
        answerer_profile.likes -= 1


def decr_dislikes(answer, answerer_profile):
    if answer.dislikes > 0:
        answer.dislikes -= 1

    if answerer_profile.dislikes > 0:
        answerer_profile.dislikes -= 1


def incr_likes(answer, answerer_profile):
    answer.likes += 1
    answerer_profile.likes += 1


def incr_dislikes(answer, answerer_profile):
    answer.dislikes += 1
    answerer_profile.dislikes += 1


# This view requires a user who is also a member of staff to be logged in
@login_required
@user_passes_test(lambda u: u.is_staff)
def approve_category(request):
    context_dict = {}

    # Get a list of categories that have not been approved
    cat_list = Category.objects.all().filter(approved=False)

    # Get a list of tuples, each consists of a approve category form and a category that needs approving
    data = []
    for i in range(len(cat_list)):
        form = ApproveCategoryForm()
        tup = (form, cat_list[i])
        data.append(tup)

    # Add to context dictionary so template can display this
    context_dict['data'] = data

    # If the staff member approves a category, it's a post request
    if request.method == 'POST':
        # Get the submitted form
        form = ApproveCategoryForm(request.POST)
        if form.is_valid():

            # If it's valid, get the category we wish to approve
            cat = Category.objects.get(pk=request.POST['category'])

            # Approve it and save it
            cat.description = request.POST['description']
            cat.approved = True
            cat.save()

            # Safely redirect user back to approve category page and display categories that still need approving
            return HttpResponseRedirect(reverse('approve_category'))

    return render(request, 'ask_students/approve_category.html', context_dict)


# This view requires a user who is also a member of staff to be logged in
@login_required
@user_passes_test(lambda u: u.is_staff)
def delete_category_request(request, category_id):

    category = Category.objects.get(pk=category_id)
    category.delete()
    return redirect('approve_category')

