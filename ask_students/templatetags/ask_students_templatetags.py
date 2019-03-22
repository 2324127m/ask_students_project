from django import template
from ask_students.models import Category, Question, Answer

register = template.Library()


@register.inclusion_tag('ask_students/template_tags/category_list.html')
def get_category_list():
    return {'categories': Category.objects.all()}


@register.inclusion_tag('ask_students/template_tags/latest_questions.html')
# def get_latest_questions(question=None):
def get_latest_questions():
    return {'latest_questions': Question.objects.order_by('-posted')[:10]}


@register.inclusion_tag('ask_students/template_tags/question_card.html')
def show_question(question):
    if not isinstance(question, Question):
        return None
    else:
        return {'question': question}


@register.inclusion_tag('ask_students/template_tags/answer_card.html')
def show_answer(answer, question, liked, disliked, user):
    if not isinstance(answer, Answer):
        return None
    else:
        return {'answer': answer, 'liked': liked, 'disliked': disliked, 'question': question, 'user': user}


@register.inclusion_tag('ask_students/template_tags/form_error_fields.html')
def display_form_error_fields(form):
    return {'form': form}

