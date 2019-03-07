from django.test import TestCase
from ask_students.models import Question, Category

from django.core.urlresolvers import reverse
from datetime import datetime, timedelta

from django.utils import timezone


# Add 10 questions to a category
def test_fixture1(category):
    new_question_1 = Question(name="Q1 has 10 views", category=category, views=10, posted=timezone.now() - timedelta(minutes=8))
    new_question_2 = Question(name="Q2 has 20 views", category=category, views=20 ,posted=timezone.now() - timedelta(minutes=4))
    new_question_3 = Question(name="Q3 has 3000 views", category=category, views=3000, posted=timezone.now() - timedelta(minutes=16))
    new_question_4 = Question(name="Q4 has 40 views", category=category, views=40, posted=timezone.now() - timedelta(minutes=13))
    new_question_5 = Question(name="Q5 has 50 views", category=category, views=50, posted=timezone.now() - timedelta(minutes=9))
    new_question_6 = Question(name="Q6 has 6000 views", category=category, views=6000, posted=timezone.now() - timedelta(minutes=2))
    new_question_7 = Question(name="Q7 has 70 views", category=category, views=70, posted=timezone.now() - timedelta(minutes=18))
    new_question_8 = Question(name="Q8 has 80 views", category=category, views=80, posted=timezone.now() - timedelta(minutes=1))
    new_question_9 = Question(name="Q9 has 9000 views", category=category, views=9000, posted=timezone.now() - timedelta(minutes=14))
    new_question_10 = Question(name="Q10 has 100 views", category=category, views=100, posted=timezone.now() - timedelta(minutes=8))

    questions = (new_question_1, new_question_2, new_question_3, new_question_4, new_question_5, new_question_6,
                 new_question_7, new_question_8, new_question_9, new_question_10)
    return questions


class IndexViewTests(TestCase):

    # move this, it's a Model test
    def test_category_contains_correct_slug_field(self):
        # Create a new category
        new_category = Category(name="Test Category 1")
        new_category.save()

        # Check slug was generated correctly
        self.assertEquals(new_category.slug, "test-category-1")


    def test_if_top_questions_are_returned_in_order_by_views(self):
        # Create a new category
        new_category = Category(name="Test Category 1")
        new_category.save()

        # Create ten questions for that category
        questions = test_fixture1(new_category)

        # Save the questions
        for question in questions:
            question.save()

        # Get response from index view
        response = self.client.get(reverse('index'))
        response_questions = response.context['top_questions']

        valid = True
        # Check if they are returned in order
        question_view = response_questions[0].views
        for question in response_questions[1:]:
            if question.views > question_view:
                valid = False
            else:
                question_view = question.views

        self.assertEqual(valid, True)


    def test_if_an_old_question_appears_in_top_questions(self):
        # Create a new category
        new_category = Category(name="Test Category 1")
        new_category.save()

        # Create ten questions for that category
        questions = test_fixture1(new_category)

        eight_days_ago = timezone.now() - timedelta(days=8)
        some_old_question = Question(name="old question 1", category=new_category, views=100000, posted=eight_days_ago)
        some_old_question.save()

        # Save the questions
        for question in questions:
            question.save()

        # Get response from index view
        response = self.client.get(reverse('index'))
        response_questions = response.context['top_questions']

        last_week = timezone.now() - timedelta(days=7)

        valid = True
        # Check if they are returned in order
        for question in response_questions:
            if question.posted < last_week:
                valid = False

        self.assertEqual(valid, True)


    def test_if_unaswered_questions_are_actually_unaswered(self):
        # Create a new category
        new_category = Category(name="Test Category 1")
        new_category.save()

        # Create ten questions for that category
        questions = test_fixture1(new_category)

        # Save the questions
        for questions in questions:
            questions.save()

        # Get response from index view
        response = self.client.get(reverse('index'))
        response_questions = response.context['unanswered_questions']

        valid = True
        # Check all questions are unanswered
        for question in response_questions:
            if question.answered != None:
                valid = False

        self.assertEqual(valid, True)


    def test_if_unanswered_questions_are_returned_in_order_of_posted(self):
        # Create a new category
        new_category = Category(name="Test Category 1")
        new_category.save()

        # Create ten questions for that category
        questions = test_fixture1(new_category)

        # Save the questions
        for question in questions:
            question.save()

        # Get response from index view
        response = self.client.get(reverse('index'))
        response_questions = response.context['unanswered_questions']

        valid = True
        # Check if they are returned in order
        # The time posted should be in ascending order
        question_posted = response_questions[0].posted
        for question in response_questions[1:]:
            if question.posted < question_posted:
                valid = False
            else:
                question_view = question.views

        self.assertEqual(valid, True)
