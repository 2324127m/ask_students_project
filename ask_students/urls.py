from django.conf.urls import url
from ask_students import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^search/$', views.search, name='search'),
    url(r'^ask/$', views.add_question, name='ask_question'),
    url(r'^about_us/$', views.about_us, name="about_us"),
    url(r'^contact_us/$', views.contact_us, name="contact_us"),
    url(r'^faq/$', views.faq, name="faq"),

    # PROFILE
    # url(r'^register_profile/$', views.register_profile, name="register_profile"),
    url(r'^profile/(?P<username>[\w\-]+)/$', views.profile, name="profile"),
    url(r'^my_profile/$', views.my_profile, name="my_profile"),
    url(r'^delete_user_profile/(?P<user_id>[1-9]\d*)/$', views.delete_user_profile, name="delete_user_profile"),

    # CATEGORY
    url(r'^category/(?P<category_name_slug>[\w\-]+)/$', views.category, name='category'),
    url(r'^request_category/$', views.request_category, name='request_category'),
    url(r'^approve_category/$', views.approve_category, name='approve_category'),
    url(r'^delete_category/(?P<category_id>[\w\-]+)/$', views.delete_category_request, name='delete_category_request'),

    # QUESTION
    url(r'^category/(?P<category_name_slug>[\w\-]+)/(?P<question_id>[1-9]\d*)/$', views.show_question, name='show_question'),
    url(r'^category/(?P<category_name_slug>[\w\-]+)/ask_question/$', views.add_question, name='ask_question'),
    url(r'^delete_question/(?P<question_id>[1-9]\d*)/$', views.delete_question, name='delete_question'),
    url(r'^edit_question/(?P<question_id>[1-9]\d*)/$', views.edit_question, name='edit_question'),

    # ANSWER
    url(r'^delete_answer/(?P<question_id>[1-9]\d*)/(?P<answer_id>[1-9]\d*)/$', views.delete_answer,
        name='delete_answer'),
    url(r'^edit_answer/(?P<answer_id>[1-9]\d*)/$', views.edit_answer, name='edit_answer'),
    url(r'^select_answer/(?P<question_id>[1-9]\d*)/$', views.select_answer, name='select_answer'),

    # AJAX REQUESTS
    url(r'^ajax/search/$', views.search, name='search_ajax'),
    url(r'^ajax/vote/$', views.vote, name="answer_vote"),
]
