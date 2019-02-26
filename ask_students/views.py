from django.shortcuts import render
<<<<<<< HEAD
from django.http import HttpResponse
from ask_students.models import Category, Questions
from ask_students.forms import AskQuestionForm
=======
from django.contrib.auth.decorators import login_required
>>>>>>> b68d109501d6559439714c61b62712192ede6a64


def index(request):
    top_questions_list = Questions.objects.order_by('-views')[:10]
    unanswered_questions_list = Question.objects.all()[:10]

    context_dict = {'top_questions': top_questions_list,
    				'unanswered_questions': unanswered_questions_list
    				}

    reponse = render(request, 'ask_students/index.html', context_dict)

    return reponse

## Need to add category_name_slug to category mode
def category(request, category_name_slug):
	context_dict = {}

	try:
		category = Category.objects.get(slug = category_name_slug)

		question_list = Question.objects.filter(category = category).order_by('-posted')

		context_dict['category'] = category
		context_dict['questions'] = question_list

	except Category.DoesNotExist:
		context_dict['category'] = None
		context_dict['questions'] = None

	return render(request, 'ask_students/category.html', context_dict)

def add_question(request):
	context_dict = {}

	form = AskQuestionForm()

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

	context_dict['form'] = form

	return render(request,'ask_students/add_question.html', context_dict)

def show_question(request,question_name_slug):
	context_dict = {}

	try:
		question = Question.objects.get(slug = question_name_slug)
		answers_list = 

