from django.conf.urls import url
from ask_students import views

# app_name = 'ask_students'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^category/(?P<category_name_slug>[\w\-]+)/$', views.category, name='category'),
    url(r'^category/(?P<category_name_slug>[\w\-]+)/(?P<question_id>[1-9]\d*)/$', views.show_question, name='show_question'),

]
