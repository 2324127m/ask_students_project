from django.shortcuts import render
from django.http import HttpResponse
from ask_students.models import Category, Question, Answer
# from ask_students.forms import AskQuestionForm

from django.contrib.auth.decorators import login_required
from registration.backends.default.views import RegistrationView


class MyRegistrationView(RegistrationView):
    def get_success_url(self, user):
        return '/'


def index(request):
    top_questions_list = Question.objects.order_by('-views')[:10]
    unanswered_questions_list = Question.objects.all()[:10]

    context_dict = {'top_questions': top_questions_list,
                    'unanswered_questions': unanswered_questions_list
                    }

    return render(request, 'ask_students/index.html', context_dict)


#  Need to add category_name_slug to category model
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


def add_question(request):
    context_dict = {}

    """form = AskQuestionForm()

    if request.method == "POST":
        form = AskQuestionForm(request.POST)

        if form.is_valid():
            question = form.save(commit = False)

            if 'support_file' in request.FILES:
                question.support_file = request.FILES['support_file']

            return show_question(request)

        else:
            ## Display errors if question cannot be added
            print(form.errors)

    context_dict['form'] = form """

    return render(request, 'ask_students/add_question.html', context_dict)


def show_question(request, question_name_slug):
    context_dict = {}

    try:
        question = Question.objects.get(slug=question_name_slug)
        answers_list = Answer.objects.filter(question=question).order_by('-posted')

        context_dict['question'] = question
        context_dict['answers_list'] = answers_list

    except Question.DoesNotExist:
        context_dict['question'] = None
        context_dict['answers_list'] = None

    return render(request, 'ask_students/question.html', context_dict)
