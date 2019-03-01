from django.test import TestCase
from ask_students.models import Question, Category


# Returns 3 questions for a given category as a tuple
def create_three_questions(category):
    new_question_1 = Question(name="My First Question has 10 views", category=category, views=10)
    new_question_2 = Question(name="My Second Question has 30 views", category=category, views=30)
    new_question_3 = Question(name="My Third Question has 20 views", category=category, views=20)
    return new_question_1, new_question_2, new_question_3


class IndexViewTests(TestCase):
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

        # Create three questions for that category
        questions = create_three_questions(new_category)

        # Save the questions
        for question in questions:
            question.save()

        # Get top ten questions in order by views
        top_questions = Question.objects.order_by('-views')[:10]

        # Check if they are returned in order
        valid = True
        question_view = top_questions[0].views
        for question in top_questions[1:]:
            if question.views > question_view:
                valid = False

        self.assertTrue(valid, msg="FAILED")
