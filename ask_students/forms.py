from django import forms
from ask_students.models import UserProfile, Category, Question, Answer, PlaceOfStudy, Permission


class UserProfileForm(forms.ModelForm):
    bio = forms.CharField(required=False)
    image = forms.ImageField(required=False)
    place_of_study = forms.ModelChoiceField(required=True, queryset=PlaceOfStudy.objects.all())
    permission = forms.ModelChoiceField(required=True, queryset=Permission.objects.all())

    class Meta:
        model = UserProfile
        exclude = ('user', 'likes', 'dislikes', 'slug')


class RequestCategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=64, help_text="Please enter the category name.")
    description = forms.CharField(max_length=512, help_text="Please enter a description.")
    approved = forms.BooleanField(widget=forms.HiddenInput())
    slug = forms.SlugField(widget=forms.HiddenInput())

    class Meta:
        model = Category
        exclude = ('slug',)

class AskQuestionForm(forms.ModelForm):
    name = forms.CharField(max_length=128, help_text="Enter your question title here!")
    text = forms.CharField(max_length=4096, help_text="Enter your question as descriptively as possible, max char limit 4096")
    anonymous = forms.BooleanField(widget=forms.CheckboxInput())
    posted = forms.DateTimeField(widget=forms.HiddenInput())
    user = forms.IntegerField(widget=forms.HiddenInput())
    category = forms.CharField(widget=forms.HiddenInput())
    support_file = forms.FileField()
    
    class Meta:
        model = Question
        exclude = ('posted', 'user', 'category',)

class AnswerForm(forms.ModelForm):
	text = forms.CharField(max_length=4096, help_text="Enter you answer here", required=True)
	
	class Meta:
		model = Answer
		fields = ('text',)
