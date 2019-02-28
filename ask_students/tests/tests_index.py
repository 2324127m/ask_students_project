from django.test import TestCase
from ask_students.models import Question
from ask_students.tests.test_methods import create_category, create_question

category1 = create_category(name="TestCategory1", description="This is just some category", approved=True)

question1 = create_question(name="SampleQuestion1", category=category1, text="question_text1", views=10)
question2 = create_question(name="SampleQuestion2", category=category1, text="question_text2", views=20)
question3 = create_question(name="SampleQuestion3", category=category1, text="question_text3", views=30)


class IndexViewTests(TestCase):
    def test_if_questions_are_returned_in_order_by_views(self):
        top_questions = Question.objects.order_by('-views')[:10]

        valid = True
        question_view = top_questions[0].views;
        for question in top_questions[1:]:
            if question.views > question_view:
                valid = False

        self.assertEqual(self, valid, True)
