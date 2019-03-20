from django.conf.urls import url
from ask_students import views

# app_name = 'ask_students'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register_profile/$', views.register_profile, name="register_profile"),
    url(r'^my_profile/$', views.my_profile, name="my_profile"),
    url(r'^profile/(?P<username>[\w\-]+)/$', views.profile, name="profile"),
    url(r'^category/(?P<category_name_slug>[\w\-]+)/$', views.category, name='category'),
    url(r'^category/(?P<category_name_slug>[\w\-]+)/(?P<question_id>[1-9]\d*)/$', views.show_question, name='show_question'),
    url(r'^delete_question/(?P<question_id>[1-9]\d*)/$', views.delete_question, name='delete_question'),
    url(r'^delete_answer/(?P<question_id>[1-9]\d*)/(?P<answer_id>[1-9]\d*)/$', views.delete_answer, name='delete_answer'),
    url(r'^request_category/$', views.request_category, name="request_category"),
    url(r'^category/(?P<category_name_slug>[\w\-]+)/ask_question/$', views.add_question, name='ask_question'),
    url(r'^about_us/$', views.about_us, name="about_us"),
    url(r'^contact_us/$', views.contact_us, name="contact_us"),
    url(r'^faq/$', views.faq, name="faq"),
    url(r'^search/$', views.search, name='search'),
    url(r'^ask/$', views.add_question, name='ask_question'),

    url(r'^request_category/$', views.request_category, name='request_category'),
	url(r'^approve_category/$', views.approve_category, name='approve_category')


    # AJAX REQUESTS
    url(r'^ajax/search/$', views.search, name='search_ajax'),
]
