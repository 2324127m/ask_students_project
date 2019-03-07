from django.conf.urls import url
from ask_students import views

# app_name = 'ask_students'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register_profile/', views.register_profile, name="register_profile"),
    url(r'^my_profile/$', views.my_profile, name="my_profile"),
    url(r'^profile/(?P<username>[\w\-]+)/$', views.profile, name="profile"),
    url(r'^category/(?P<category_name_slug>[\w\-]+)/$', views.category, name='category'),
    url(r'^category/(?P<category_name_slug>[\w\-]+)/(?P<question_id>[1-9]\d*)/$', views.show_question, name='show_question'),
    url(r'^contact_us/$', views.contact_us, name="contact_us"),
    url(r'^about_us/$', views.about_us, name="about_us"),
    url(r'^faq/$', views.faq, name="faq"),
    url(r'^request_category/$', views.request_category, name="request_category"),
]
