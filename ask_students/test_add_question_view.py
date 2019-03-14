from django.test import TestCase
from ask_students.models import Question, Category, Answer
from django.core.urlresolvers import reverse
from datetime import datetime, timedelta
from django.utils import timezone


def test_fixture1(category):
    new_question = Question(name="Q1 has 90 views", category=category, views=90, posted=timezone.now() - timedelta(minutes=8))

    return new_question


class AddQuestionViewTests(TestCase):

    def CheckEmptyFormRedisplaysForm(self):
        pass
        
    def TestQuestionFields(self):
        pass

    def TestNonExistantQuestionReturnsNone(self):
        pass

    def TestAnonymousWorks(self):
        pass

    def TestQuestionPostWithoutFile(self):
        pass
