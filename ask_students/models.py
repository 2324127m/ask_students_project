from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.utils import timezone


class PlaceOfStudy(models.Model):
	title = models.CharField(max_length=256)

	def __str__(self):
		return self.title


class Permission(models.Model):
	title = models.CharField(max_length=128)

	def __str__(self):
		return self.title


# Define all the entities, attributes, and relationships from our ER diagram

class Category(models.Model):
	# Category details
	name = models.CharField(max_length=64, unique=True)
	description = models.CharField(max_length=512, null=True)
	approved = models.BooleanField(default=False)
	slug = models.SlugField(unique=True)

	# Each category has a UserProfile who requested it
	user = models.ForeignKey("UserProfile", on_delete=models.SET_NULL, null=True)

	def save(self, *args, **kwargs):
		self.slug = slugify(self.name)
		super(Category, self).save(*args, **kwargs)

	class Meta:
		verbose_name_plural = "Categories"

	def __str__(self):
		return self.name


class UserProfile(models.Model):
	# UserProfile inherits from django User Model
	# Has fields user.username, user.password (Optional user.firstname, user.lastname)
	user = models.OneToOneField(User)

	# These store links between users and the answers they vote on.
	up_votes = models.ManyToManyField('Answer', related_name="up_voters")
	down_votes = models.ManyToManyField('Answer', related_name="down_voters")

	# User profile details
	bio = models.CharField(max_length=4096, null=True)
	likes = models.PositiveIntegerField(default=0)
	dislikes = models.PositiveIntegerField(default=0)

	# Upload profile images to media/profile_imagees/
	image = models.ImageField(upload_to="profile_images/", null=True)

	slug = models.SlugField(unique=True)

	def save(self, *args, **kwargs):
		self.slug = slugify(self.user.username)
		super(UserProfile, self).save(*args, **kwargs)

	place_of_study = models.ForeignKey(PlaceOfStudy, on_delete=models.SET_NULL, null=True)
	permission = models.ForeignKey(Permission, on_delete=models.SET_NULL, default=None, null=True)

	def __str__(self):
		return self.user.username


class Answer(models.Model):
	# Answer details
	text = models.CharField(max_length=4096)
	anonymous = models.BooleanField(default=False)
	likes = models.PositiveIntegerField(default=0)
	dislikes = models.PositiveIntegerField(default=0)
	posted = models.DateTimeField(default=timezone.now)
	edited = models.DateTimeField(default=None, null=True, blank=True)

	# Answer has a UserProfile who posted it
	user = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, blank=True)

	# Answer has a Category it belongs to
	category = models.ForeignKey(Category, on_delete=models.CASCADE)

	# Answer has a Question sitting on top of it that it answers
	questiontop = models.ForeignKey("Question", on_delete=models.CASCADE)

	def __str__(self):
		return self.text


class Question(models.Model):
	# Question details
	name = models.CharField(max_length=128)
	text = models.CharField(max_length=4096, default="")
	anonymous = models.BooleanField(default=False)
	posted = models.DateTimeField(default=timezone.now)
	edited = models.DateTimeField(default=None, null=True, blank=True)
	views = models.IntegerField(default=0)

	# Question has an Answer that the poster has marked as the answer
	answered = models.ForeignKey(Answer, on_delete=models.SET_NULL, null=True, default=None, blank=True)

	# Question has a UserProfile who posted it
	user = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True)

	# Question has a Category that it belongs to
	category = models.ForeignKey(Category, on_delete=models.CASCADE)

	# Support files for questions are uploaded to media/support_files/
	support_file = models.ImageField(upload_to='support_files', null=True, blank=True)

	def __str__(self):
		return self.name
