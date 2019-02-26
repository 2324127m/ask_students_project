from django.contrib import admin
from ask_students.models import Category, UserProfile, Question, Answer, PlaceOfStudy, Permission


admin.site.register(Category)
admin.site.register(UserProfile)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(PlaceOfStudy)
admin.site.register(Permission)
