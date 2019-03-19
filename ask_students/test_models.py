from django.test import TestCase
from ask_students.models import UserProfile, PlaceOfStudy, User, Permission

def test_fixture_1():
        place_of_study = PlaceOfStudy(title='University of Glasgow')
        permission = Permission(title='student')
        testUser = User(username='testuser', password='test')
        testUserProfile = UserProfile(user=testUser, place_of_study=place_of_study, permission=permission)
        return testUser

class UserProfileModelTests(TestCase):
    
    def test_ensure_likes_are_positive(self):

        # ensure_likes_are_positive should result True for users who's likes
        # are zero or positive

        user = test_fixture_1()
        user.likes = 1
        user.save()
        self.assertEqual((user.likes >= 0), True)

""" def test_ensure_dislikes_are_positive(self):

    # ensure_dislikes_are_positive should result True for users who's dislikes
    # are zero or positive

    user = UserProfile(user=testUser, dislikes=-1)
    user.save()
    self.assertEqual((user.dislikes >= 0), True)

def test_ensure_valid_place_of_study(self):
    
    # ensure_valid_place_of_study should result True for users who's Place of Study is
    # on the predefined list of Scottish Universities
    
    user = UserProfile(user=testUser, place_of_study='University of Glasgow')
    user.save()
    self.assertIn(user.place_of_study, places_of_study)

def test_ensure_invalid_place_of_study(self):

    # ensure_invalid_place_of_study should raise a validation error when a user is created with an 
    # invalid place of study

    with self.assertRaises(ValidationError):
        user = UserProfile(user=testUser, place_of_study='the streets')
        user.save() """
