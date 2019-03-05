from django.test import TestCase
from ask_students.models import Question, Category, Answer

from django.core.urlresolvers import reverse
from datetime import datetime, timedelta

from django.utils import timezone


# Add a question to a category
def test_fixture1(category):
    new_question = Question(name="Q1 has 10 views", category=category, views=10, posted=timezone.now() - timedelta(minutes=8))
    answer_1 = Answer(text="Answer 1", category=category, questiontop=new_question, posted=timezone.now() - timedelta(minutes=7))
    
    return new_question


class IndexViewTests(TestCase):

    def test_if_answers_are_returned_in_order_earliest_first(self):
        # Create a new category
        new_category = Category(name="Test Category 1")
        new_category.save()

        # Create and save a question for that category
        question = test_fixture1(new_category)
        question.save()

        # Get response from show_question view
        response = self.client.get(reverse('show_question', kwargs={'category_name_slug': new_category.slug, 'question_id': question.pk}))
        response_answers = response.context['answers_list']

        valid = True
        # Check if they are returned in order
        # The time posted should be in anscending order
        answer_posted = response_answers[0].posted
        for answer in response_answers[1:]:
            if answer.posted < answer_posted:
                valid = False
            else:
                answer_posted = answer.posted

        self.assertEqual(valid, True)
