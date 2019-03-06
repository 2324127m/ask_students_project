import datetime
from django.shortcuts import render, redirect, reverse
from django.utils import timezone
from django.http import HttpResponse

from ask_students.models import Category, Question, Answer, UserProfile, User
from ask_students.forms import UserProfileForm, RequestCategoryForm
# from ask_students.forms import AskQuestionForm

from django.contrib.auth.decorators import login_required
from registration.backends.simple.views import RegistrationView

from datetime import timedelta


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

        question_list = Question.objects.filter(category=category_obj).order_by('-posted')

        context_dict['category'] = category_obj
        context_dict['questions'] = question_list

    except Category.DoesNotExist:
        context_dict['category'] = None
        context_dict['questions'] = None

    return render(request, 'ask_students/category.html', context_dict)

@login_required
def add_question(request):
    context_dict = {}

    """form = AskQuestionForm()

    if request.method == "POST":
        form = AskQuestionForm(request.POST)

        if form.is_valid():
            question = form.save(commit = False)
            question.posted = datetime.now()

            if 'support_file' in request.FILES:
                question.support_file = request.FILES['support_file']


            return show_question(request)

        else:
            ## Display errors if question cannot be added
            print(form.errors)

    context_dict['form'] = form """

    return render(request, 'ask_students/add_question.html', context_dict)


def show_question(request, category_name_slug, question_id):
    context_dict = {}

    try:
    	# 
        question = Question.objects.get(pk=question_id)
        # Earliest answer first
        answers_list = Answer.objects.filter(question=question).order_by('posted')

        # return top answer

        context_dict['question'] = question
        context_dict['answers_list'] = answers_list

        if question.answered != None:
            context_dict['answer'] = question.answer

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

    except User.DoesNotExist:
        return redirect('index')

    # select user's profile instance or create a blank one
    # users_profile = UserProfile.objects.get_or_create(user=user)[0]

    context_dict = {'user': user, 'top_five_answers': most_liked_answers, 'number_of_answers': number_of_answers}

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
        form = UserProfileForm(request.POST)
        if form.is_valid():
            users_profile = form.save(commit=False)
            users_profile.user = request.user
            users_profile.save()
            return render(request, 'registration/registration_complete.html', {})
        else:
            print(form.errors)

    context_dict = {"form": form}

    return render(request, 'ask_students/profile_registration.html', context_dict)
