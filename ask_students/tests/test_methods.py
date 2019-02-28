from ask_students.models import Category, Question
from datetime import datetime


def create_category(name, description=None, approved=False, user=None):
    category = Category(name=name, description=description, approved=approved, user=user)
    category.save()
    return category


def create_question(name, category, text=None, anonymous=False, posted=datetime.now(), edited=None
                    , views=0, answered=None, user=None, support_file=None):
    question = Question(name=name, description=text, anonymous=anonymous, user=user
                        , posted=posted, edited=edited, views=views, answered=answered, category=category
                        , support_file=support_file)
    question.save()
    return question
