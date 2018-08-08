 # coding: utf-8
 
from django.urls import path
from django.conf.urls import url
from django.contrib.auth import views as auth_views



from classmanagement import views

app_name = 'classmanagement'

urlpatterns = [
    url(r'^course/(\d+)/$', views.course_view),
    url(r'^course/(\d+)/student/(\d+)/summary/$', views.student_summary),
    url(r'^course/(\d+)/(\w+)/summary/$', views.activity_summary),
    url(r'^course/(\d+)/summary/$', views.course_summary),
    url(r'^redirect/(\d+)/$', views.redirect_activity),
    path('not_authenticated/', auth_views.LoginView.as_view(template_name='playexo/not_authenticated.html', redirect_authenticated_user=True), name="login"),
]

