from djando.db import models
from django.contrib.auth.models import User

class Category(models.Model):
	name = models.CharField(max_length = 64, unique = True)
	description = models.CharField(max_length = 512)
	approved = models.BooleanField(default = False)

	user = models.ForeignKey(User, on_delete = models.SET_NULL)

	def __str__(self):
		return self.name

class UserProfile(models.Model):
	user = models.OneToOneField(User)

	bio = models.CharField(max_length = 4096)
	likes = models.IntegerField(default = 0)
	dislikes = models.IntegerField(default = 0)
	image = models.ImageField(upload_to='profile_images')

	place_of_study = models.ForeignKey(placeOfStudy, on_delete = models.SET_NULL)
	permission = models.ForeignKey(Permission, on_delete = models.set("student"))

	def __str__(self):
		return self.user.username

class Question(models.Model):
	name = models.CharField(max_length = 128)
	test = models.CharField(max_length = 4096)
	anonymous = models.BooleanField()
	posted = models.DateTimeField()
	edited = models.DateTimeField()
	views = models.IntegerField(default = 0 )

	answered = models.OneToOneField(Answer)
	user = models.ForeignKey(UserProfile, on_delete = models.SET_NULL)
	category = models.ForeignKey(Category, on_delete = models.CASCADE)

	def __str__(self):
		return self.name

class Answer(models.Model):
	text = models.CharField(max_length = 4096)
	likes = models.IntegerField(default = 0)
	dislikes = models.IntegerField(default = 0)
	posted = models.DateTimeField()
	edited = models.DateTimeField()

	user = models.ForeignKey(UserProfile, on_delete = models.SET_NULL)
	category = models.ForeignKey(Category, on_delete = models.CASCADE)

	def __str__(self):
		return self.text[30] + "..."

class placeOfStudy(models.Model):
	title = models.CharField(max_length = 256)

	def __str__(self):
		return self.title

class Permission(models.Model):
	title = models.CharField(max_lenth = 128)

	def __str__(self):
		return self.title
