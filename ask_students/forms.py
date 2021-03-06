from django import forms
from ask_students.models import UserProfile, Category, Question, Answer, PlaceOfStudy, Permission


# Form for creating and editing a user profile
class UserProfileForm(forms.ModelForm):
    bio = forms.CharField(required=False)
    image = forms.ImageField(required=False)
    place_of_study = forms.ModelChoiceField(required=True, queryset=PlaceOfStudy.objects.all())
    permission = forms.ModelChoiceField(required=True, queryset=Permission.objects.all())

    class Meta:
        model = UserProfile
        exclude = ('user', 'likes', 'dislikes', 'slug', 'up_votes', 'down_votes')


# Form for requesting a category
class RequestCategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=64)
    description = forms.CharField(max_length=512)

    class Meta:
        model = Category
        exclude = ('slug', 'user', 'approved')


# Form used to select your answer
class SelectAnswerForm(forms.ModelForm):
    answered=forms.ModelChoiceField(required=False, queryset=Answer.objects.all())

    class Meta:
        model = Question
        exclude = ('name', 'text', 'anonymous', 'posted', 'edited', 'views', 'user', 'category', 'support_file')


# Form for asking questions
class AskQuestionForm(forms.ModelForm):
    name = forms.CharField(max_length=128)
    text = forms.CharField(max_length=4096)
    anonymous = forms.BooleanField(widget=forms.CheckboxInput(), required=False)
    category = forms.ModelChoiceField(required=True, queryset=Category.objects.filter(approved=True))
    support_file = forms.ImageField(required=False)

    class Meta:
        model = Question
        exclude = ('posted', 'user', 'answered', 'edited', 'views', )


# Form for editing your question
class EditQuestionForm(forms.ModelForm):
    name = forms.CharField(max_length=128, required=True)
    text = forms.CharField(max_length=4096, required=True)
    category = forms.ModelChoiceField(required=True, queryset=Category.objects.filter(approved=True))
    support_file = forms.ImageField(required=False)

    class Meta:
        model = Question
        exclude = ('posted', 'user', 'answered', 'edited', 'views', 'anonymous')


# Form to submit an answer to a question
class AnswerForm(forms.ModelForm):
    text = forms.CharField(max_length=4096, help_text="Enter you answer here", required=True)

    class Meta:
        model = Answer
        fields = ('text',)


# Form to approve requested categories - for superusers only
class ApproveCategoryForm(forms.ModelForm):
    category = forms.IntegerField(widget=forms.HiddenInput())
    description = forms.CharField(max_length=512)
    
    class Meta:
        model = Category
        exclude = ('slug', 'user', 'approved', 'name')
