from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    # path('register/', TemplateView.as_view(
    #     template_name="account/RegistrationForm.html"), name='register-view'),
    path('register/', views.Formview.as_view()),
    path('sendmail/', views.sendmail, name='sendmail')
]
