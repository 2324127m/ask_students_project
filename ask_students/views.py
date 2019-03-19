import sys

from django.shortcuts import render, redirect, reverse
from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect

from django.core.paginator import Paginator, InvalidPage

import json
from django.forms.models import model_to_dict
from django.core import serializers

from ask_students.models import Category, Question, Answer, UserProfile, User, Permission
from ask_students.forms import UserProfileForm, RequestCategoryForm, AskQuestionForm, AnswerForm

from django.contrib.auth.decorators import login_required
from registration.backends.simple.views import RegistrationView

from datetime import datetime, timedelta


class MyRegistrationView(RegistrationView):
    def get_success_url(self, user):
        return reverse('register_profile')


def index(request):
    # Get top questions in past week
    past_week = timezone.now() - timedelta(days=7)

    # Filter doesn't work here, fix this - temp solution is to ignore datetime
    top_questions_list = Question.objects.filter(posted__gte=past_week).order_by('-views')[:10]

    # Oldest unanswered question first
    unanswered_questions_list = Question.objects.filter(answered=None).order_by('posted')[:10]

    context_dict = {'top_questions': top_questions_list,
                    'unanswered_questions': unanswered_questions_list
                    }

    return render(request, 'ask_students/index.html', context_dict)


def category(request, category_name_slug):
    context_dict = {}

    try:
        category_obj = Category.objects.get(slug=category_name_slug)
        context_dict['category'] = category_obj

        question_list = Question.objects.filter(category=category_obj).order_by('-posted')
        question_paginator = Paginator(question_list, 10)  # Where second argument is max questions per page.

        # Get ?page=xxx from request and return that page in the context_dict
        requested_page = request.GET.get('page')

        # If request does not specify a page, choose first page.
        if requested_page is None:
            requested_page = 1

        question_page = question_paginator.page(requested_page)  # Throws InvalidPage if no valid questions to display.

        context_dict['questions'] = question_page

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
    categories = Category.objects.all()
    form = AskQuestionForm()
    
    if request.method == 'POST':
        form = AskQuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit = True)
            question.posted = datetime.now()
            up = UserProfile.objects.get(user=request.user)
            question.user = up

            if 'support_file' in request.FILES:
                question.support_file = request.FILES['support_file']

            
            question.save()
            category_name = form.cleaned_data['category']
            category_slug = Category.objects.get(name=category_name).slug
            print(question.pk)
            return HttpResponseRedirect(reverse('index'), request)

        else:
            # Display errors if question cannot be added
            print(form.errors)

    context_dict['form'] = form
    context_dict['categories']=categories

    return render(request, 'ask_students/add_question.html', context_dict)


def show_question(request, category_name_slug, question_id):
    context_dict = {}

    try:
        question = Question.objects.get(pk=question_id)
        # Earliest answer first

        answers_list = Answer.objects.filter(questiontop=question).order_by('-likes')

        # Return top answer

        context_dict['question'] = question
        context_dict['answers_list'] = answers_list
        context_dict['number_of_answers'] = len(answers_list)

        try:
            user_profile = UserProfile.objects.get(pk=question.user.pk)
            context_dict['user_profile'] = user_profile
        except:
            context_dict['user_profile'] = None

        if question.answered is not None:
            context_dict['answer'] = question.answered

        form = AnswerForm

        if request.method == 'GET':
            question.views += 1
            question.save()

        # If method of the request is POST, then a user posting an answer to the question
        if request.method == 'POST':
            form = AnswerForm(request.POST)

            if form.is_valid():
                answer = form.save(commit=False)
                answer.category = Category.objects.get(slug=category_name_slug)
                answer.questiontop = question
                # answer needs a user
                # answer.user = user
                answer.user = request.user
                answer.save()

            else:
                print(form.errors)

            # Add the form to context dictionary
            context_dict['form'] = form

    except Question.DoesNotExist:
        context_dict['question'] = None
        context_dict['answers_list'] = None

    return render(request, 'ask_students/question.html', context_dict)


def request_category(request):
    form = RequestCategoryForm()

    if request.method == 'POST':
        form = RequestCategoryForm(request.POST)

        if form.isvalid():
            form.save(commit=True)
            return reverse('index')
        else:
            print(form.errors)
    return render(request, 'ask_students/request_category.html', {'form': form})


def profile(request, username):
    # Get user, if doesn't exist -> redirect to home page
    try:
        user = User.objects.get(username=username)
        all_answers = Answer.objects.filter(user=user.pk)
        most_liked_answers = all_answers.order_by('-likes')[:5]
        number_of_answers = len(all_answers)
        ###ADDED THIS LINE AS EMAIL NOT SHOWING PROPERLY###
        this_user_email = user.email
        userprofile = UserProfile.objects.get(user=user)
        user_permission = userprofile.permission
        likes = userprofile.likes
        dislikes = userprofile.dislikes
        #user_permission = user.permission
        if user_permission == None:
            role = "Student"
        else:
            # Adding a permission via admin interface causes error here
            # Permission.objects.filter(pk=user_permission)
            role = user_permission.title

    except User.DoesNotExist:
        return redirect('index')

    # select user's profile instance or create a blank one
    # users_profile = UserProfile.objects.get_or_create(user=user)[0]

    context_dict = {'this_user': user, 'top_five_answers': most_liked_answers, 'likes': likes, 'dislikes': dislikes,
                    'number_of_answers': number_of_answers, 'role' : role, 'userprofile' : userprofile, 'this_user_email' : this_user_email }

    return render(request, 'ask_students/profile.html', context_dict)


@login_required
def my_profile(request):
    user = User.objects.get(username=request.user)

    context_dict = {'user': user}

    return render(request, 'ask_students/my_profile.html', context_dict)


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
        results = []

        print("Search for " + query)

        for result in queryset:
            print(result.name)
            results.append(result.name)

        data = json.dumps(results)
        mt = 'application/json'

        return HttpResponse(data, mt)

    else:
        search_query = request.GET.get('q')
        context_dict = {}

        if search_query:
            search_terms = search_query.split()
            result = Question.objects.filter(name__contains=search_terms[0])
            for term in search_terms[1:]:
                result = result & Question.objects.filter(name__icontains=term)  # Case insensitive containment filter
            context_dict['search_results'] = result

        return render(request, 'ask_students/search.html', context_dict)
