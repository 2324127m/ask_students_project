from django.test import TestCase
from ask_student.models import Question, Category, Answer
from django.core.urlresolvers import reverse
from datatime import datetime, timedelta
from django.utils import timezone

def test_fixture1(category):
    new_question = Question(name="Q1 has 90 views", category=category, views=90, posted=timezone.now() - timedelta(minutes=8))

    return new_question

class AddQuestionViewTests(TestCase):

    def CheckEmptyFormRedisplaysForm(self):
        
    def TestQuestionFields(self):

    def TestNonExistantQuestionReturnsNone(self):

    def TestAnonymousWorks(self):

    def TestQuestionPostWithoutFile(self):
    
