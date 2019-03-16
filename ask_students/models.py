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
	name = models.CharField(max_length=64, unique=True)
	description = models.CharField(max_length=512, null=True)
	approved = models.BooleanField(default=False)
	slug = models.SlugField(unique=True)

	user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

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

	bio = models.CharField(max_length=4096, null=True)
	likes = models.PositiveIntegerField(default=0)
	dislikes = models.PositiveIntegerField(default=0)

	location = "profile_images/" + str("test") + "/"
	image = models.ImageField(upload_to=location, null=True)

	slug = models.SlugField(unique=True)

	def save(self, *args, **kwargs):
		self.slug = slugify(self.user.username)
		super(UserProfile, self).save(*args, **kwargs)

	place_of_study = models.ForeignKey(PlaceOfStudy, on_delete=models.SET_NULL, null=True)
	permission = models.ForeignKey(Permission, on_delete=models.SET_NULL, default=None, null=True)

	def __str__(self):
		return self.user.username


class Answer(models.Model):
	text = models.CharField(max_length=4096)
	likes = models.PositiveIntegerField(default=0)
	dislikes = models.PositiveIntegerField(default=0)
	posted = models.DateTimeField(default=timezone.now)
	edited = models.DateTimeField(default=None, null=True)

	user = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True)
	category = models.ForeignKey(Category, on_delete=models.CASCADE)
	questiontop = models.ForeignKey("Question", on_delete=models.CASCADE)

	def __str__(self):
		return self.text


# A question MUST have the following:
# 1) name
# 2) posted
# 2) category
class Question(models.Model):
	name = models.CharField(max_length=128)
	text = models.CharField(max_length=4096, default="")
	anonymous = models.BooleanField(default=False)
	posted = models.DateTimeField(default=timezone.now)
	edited = models.DateTimeField(default=None, null=True)
	views = models.IntegerField(default=0)

	answered = models.ForeignKey(Answer, on_delete=models.SET_NULL, null=True, default=None)
	user = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True)
	category = models.ForeignKey(Category, on_delete=models.CASCADE)

	support_file = models.ImageField(upload_to='support_files', null=True)

	def __str__(self):
		return self.name
