from django import forms
from ask_students.models import Category

class RequestCategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=64, unique=True, help_text = "Please enter the category name.")
    description = forms.CharField(max_length=512, null=True, help_text = "Please enter a description.")
    approved = forms.BooleanField(widget=forms.HiddenInput(), default=False)
    slug = forms.SlugField(widget=forms.HiddenInput(), unique=True)

    class Meta:
        model = Category
        fields= ('name', 'description',)


