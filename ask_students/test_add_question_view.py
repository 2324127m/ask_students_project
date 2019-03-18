from django.test import TestCase
from ask_students.models import Question, Category, Answer
from django.core.urlresolvers import reverse
from datetime import datetime, timedelta
from django.utils import timezone


def test_fixture1(category):
    new_question = Question(name="Q1 has 90 views", category=category, views=90, posted=timezone.now() - timedelta(minutes=8), anonymous = True)

    return new_question


class AddQuestionViewTests(TestCase):

    def CheckEmptyFormRedisplaysForm(self):
        pass
        
    def TestQuestionFields(self):
        #Create a new category
        new_category = Category(name = "Test Category 1")
        new_category.save()
        
        #Create and save a question for that category
        question = test_fixture1(new_category)
        question.save()
        
        self.assertEqual('')

    def TestNonExistantQuestionReturnsNone(self):
        # Create a new category
        new_category = Category(name="Test Category 1")
        new_category.save()

        # Get a repsonse when the question does not exist
        response = self.client.get(reverse('add_question', kwargs={'category_name_slug': new_category.slug, 'question_id': 4321}))

        self.assertEqual(response.context['question'], None)

    def TestAnonymousWorks(self):
        #Create a new category
        new_category = Category(name = "Test Category 1")
        new_category.save()
        
        #Create and save a question for that category
        question = test_fixture1(new_category)
        question.save()

    def TestQuestionPostWithoutFile(self):
        #Create a new category
        new_category = Category(name = "Test Category 1")
        new_category.save()
        
        response = self.client.get(reverse('add_question', kwargs={'category_name_slug': new_category.slug, 'question_id': 4321}))

        self.assertEqual(response.context['question'], None)
