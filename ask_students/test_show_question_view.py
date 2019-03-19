from django.test import TestCase
from ask_students.models import Question, Category, Answer

from django.core.urlresolvers import reverse
from datetime import datetime, timedelta

from django.utils import timezone


# Add a question to a category
def test_fixture1(category):
    new_question = Question(name="Q1 has 10 views", category=category, views=10, posted=timezone.now() - timedelta(minutes=8))

    return new_question

# Add answers to a question
def test_fixture2(question, category):
    answer_1 = Answer(text="Answer 1", category=category, questiontop=question, posted=timezone.now() - timedelta(minutes=7))
    answer_2 = Answer(text="Answer 2", category=category, questiontop=question, posted=timezone.now() - timedelta(minutes=6))

    return (answer_1, answer_2)


class ShowQuestionViewTests(TestCase):

    def test_if_answers_are_returned_in_order_earliest_first(self):
        # Create a new category
        new_category = Category(name="Test Category 1")
        new_category.save()

        # Create and save a question for that category
        question = test_fixture1(new_category)
        question.save()

        # Create and save answers for the question
        answers = test_fixture2(question, new_category)
        for answer in answers:
            answer.save()

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


    def test_if_question_does_not_exist(self):
        # Create a new category
        new_category = Category(name="Test Category 1")
        new_category.save()

        # Get a repsonse when the question does not exist
        response = self.client.get(reverse('show_question', kwargs={'category_name_slug': new_category.slug, 'question_id': 1234}))

        self.assertEqual(response.context['question'], None)


    def test_if_question_is_answered(self):
        # Create a new category
        new_category = Category(name="Test Category 1")
        new_category.save()

        # Create and save a question for that category
        question = test_fixture1(new_category)
        question.save()

        # Create and save answers for the question
        answers = test_fixture2(question, new_category)
        for answer in answers:
            answer.save()

        # Set answer 1 as best answer
        question.answered = answers[0]
        question.save()

        # Get response from show_question view
        response = self.client.get(reverse('show_question', kwargs={'category_name_slug': new_category.slug, 'question_id': question.pk}))
        best_answer = response.context['answer']

        self.assertEqual(answers[0], best_answer)

    def TestAnonymousWorks(self):
        pass

