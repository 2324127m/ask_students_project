from django.conf.urls import url
from ask_students import views

# app_name = 'ask_students'

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^register_profile/', views.register_profile, name="register_profile"),
	url(r'^profile/(?P<username>[\w\-]+)/$', views.profile, name="profile"),
]
