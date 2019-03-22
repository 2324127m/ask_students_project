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
