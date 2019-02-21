from django.conf.urls import url
from ask_students import views

# app_name = 'ask_students'

urlpatterns = [
	url(r'^$', views.index, name='index')
]
