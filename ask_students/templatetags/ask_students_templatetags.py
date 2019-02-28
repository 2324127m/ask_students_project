from django import template
from ask_students.models import Category, Question

register = template.Library()


@register.inclusion_tag('ask_students/category_list.html')
def get_category_list():
	return {'categories': Category.objects.all()}


@register.inclusion_tag('ask_students/latest_questions.html')
# def get_latest_questions(question=None):
def get_latest_questions():
	return {'latest_questions': Question.objects.order_by('-posted')[:10]}
