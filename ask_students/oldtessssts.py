from django.test import TestCase
from ask_students import default_student, PlaceOfStudy, Permission, Category
from ask_students import UserProfile, Answer, Question

class DefaultStudentMethodTests(TestCase):

class PlaceOfStudyMethodTests(TestCase):

class PermissionMethodTests(TestCase):

class CategoryMethodTests(TestCase):

class UserProfileMethodTests(TestCase):
    def test_ensure_likes_are_positive(self):
        """
        ensure_likes_are_positive should result True for users who's likes
        are zero or positive
        """
        #No sure if this is correct but it's a start
        user = UserProfile(bio='hello hello', likes=-1)
        user.save()
        self.assertEqual((user.likes>=0), True)
        
    def test_ensure_dislikes_are_positive(self):
        """
        ensure_dislikes_are_positive should result True for users who's dislikes
        are zero or positive
        """
        #No sure if this is correct but it's a start ctrl v
        user = UserProfile(bio='hello hello', dislikes=-1)
        user.save()
        self.assertEqual((user.dislikes>=0), True)

    def test_ensure_valid_place_of_study(self):
        """
        ensure_valid_place_of_study should result True for users who's Place of Study is
        on the predefined list of Scottish Universities
        """
        #Unsure what to do with this as not 100% sure how we're implementing it
        
    def test_ensure_valid_permission_group(self):
        """
        ensure_valid_permission_group should result True for users belonging to one of
        the four permission groups
        """
        #Not sure if it's four and also how exactly this is implemented (or if it needs tested)

class AnswerMethodTests(TestCase):
    def test_ensure_likes_are_positive(self):
        """
        ensure_likes_are_positive should result True for an Answer Category who's likes
        are zero or positive
        """
        #No sure if this is correct but it's a start
        ans = Answer(text='You are WRONG', likes=-1)
        ans.save()
        self.assertEqual((ans.likes>=0), True)
        
    def test_ensure_dislikes_are_positive(self):
        """
        ensure_dislikes_are_positive should result True for an Answer who's dislikes
        are zero or positive
        """
        #No sure if this is correct but it's a start ctrl v
        ans = Answer(text='You are WRONG', dislikes=-1)
        ans.save()
        self.assertEqual((ans.dislikes>=0), True)

    def test_ensure_posted_date_is_correct_format(self):
        """
        ensure_posted_date_is_correct_format should result true for an Answer who's
        posted date is valid - in the correct format and not in the year 3000 or pre 2019
        """
        #No idea

    def test_ensure_edited_date_is_correct_format(self):
        """
        ensure_edited_date_is_correct_format should result true for an Answer who's
        edited date is valid - in the correct format and not in the year 3000 or pre 2019
        """
        #No idea

    def test_ensure_valid_user_associated(self):
        """
        """
        
    def test_valid_category_associated(self):
        """
        """

    def test_valid_question_associated(self):
        """
        """

class QuestionMethodTests(TestCase):
    def test_ensure_views_are_positive(self):
        """
        test_ensure_views_are_positive should result true for a Question who's views
        are zero or positive
        """
        question = Question(anonymous=True, views=-1)
        question.save()
        self.assertEqual((question.views>=0), True)
        
