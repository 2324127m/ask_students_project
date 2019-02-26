from django import template
from ask_student.models import Category

register = template.Library()

@register.inclusion_tag('ask_students/category_list.html')
def get_category_list(cat=None):
	return {'categories': Category.objects.all()}

@register.inclusion_tag('ask_students/latest_questions.html')
def get_latest_questions(question=None)
	return {'latest_questions': Question.objects.order_by('-posted')[:10]}