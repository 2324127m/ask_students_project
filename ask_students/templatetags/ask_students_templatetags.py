from django import template
from ask_students.models import Category, Question, Answer

register = template.Library()


@register.inclusion_tag('ask_students/category_list.html')
def get_category_list():
	return {'categories': Category.objects.all()}


@register.inclusion_tag('ask_students/latest_questions.html')
# def get_latest_questions(question=None):
def get_latest_questions():
	return {'latest_questions': Question.objects.order_by('-posted')[:10]}


@register.inclusion_tag('ask_students/question_card.html')
def show_question(question):
	if not isinstance(question, Question):
		return None
	else:
		return {'question': question}

@register.inclusion_tag('ask_students/full_question_card.html')
def show_full_question(question):
        if not isinstance(question, Question):
                return None
        else:
                return {'question': question}

@register.inclusion_tag('ask_students/answer_card.html')
def show_answer(answer, liked, disliked):
        if not isinstance(answer, Answer):
                return None
        else:
                return {'answer': answer, 'liked': liked, 'disliked': disliked }
