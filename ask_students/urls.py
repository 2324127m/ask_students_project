from django.conf.urls import url
from ask_students import views

# app_name = 'ask_students'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^category/(?P<category_name_slug>[\w\-]+)/$', views.category, name='category'),

]
