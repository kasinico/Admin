from django.urls import path

from e_mail import views
urlpatterns = [
    # Email
    path('email_inbox', views.EmailInbox.as_view(),name='email_inbox'),
    path('email_read', views.EmailRead.as_view(),name='email_read'),
    path('email/email-compose', views.EmailCompose,name='email_compose'),
]