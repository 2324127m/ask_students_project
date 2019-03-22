from django.contrib import admin
from ask_students.models import Category, UserProfile, Question, Answer, PlaceOfStudy, Permission

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	exclude = ('slug',)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
	exclude = ('up_votes', 'down_votes', 'likes', 'dislikes', 'slug',)

@admin.register(Question)
class QuestioAdmin(admin.ModelAdmin):
	exclude = ('posted', 'edited', 'views',)

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
	exclude = ('likes', 'dislikes', 'posted', 'edited', 'questiontop',)


admin.site.register(PlaceOfStudy)
admin.site.register(Permission)

admin.site.site_header = "Ask Students Administration"
admin.site.index_title = "Ask Students Administration"