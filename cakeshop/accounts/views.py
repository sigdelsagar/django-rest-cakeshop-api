from django.views.generic import ListView, DetailView, TemplateView, FormView
from rest_framework import permissions, viewsets
from rest_framework.permissions import BasePermission
from rest_framework.authentication import SessionAuthentication
from .serializers import UserSerializer
from .forms import SignupForm, SendMailForm
from .tasks import task_sendmail
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import get_user_model
from django.conf import settings
import os

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    authentication_classes = [SessionAuthentication]

    def get_permissions(self):
        permission_classes = [permissions.IsAdminUser]
        # print(type(self.request.user))
        # if self.request.user.is_anonymous:
        #     if self.action == 'create':
        #         permission_classes = []
        if self.action == 'create':
            permission_classes = [permissions.AllowAny]

        return [permission() for permission in permission_classes]


# class RegisterView(FormView):
#     template_name = "CRUD/RegistrationForm.html"
#     form_class = SignupForm
#     success_url = "/hostel/activation-sent/"

#     def form_valid(self, form):
#         email = form.cleaned_data["email"]
#         pword = form.cleaned_data["password"]
#         # send message and token for authentication
#         subject = 'Thank you for visiting our site'
#         email_from = settings.EMAIL_HOST_USER
#         recipient_list = [email, ]
#         current_site = get_current_site(self.request).domain

#         instance = User.objects.create_user(
#             email=email, password=pword, is_customer=True, is_active=False)
#         uid = urlsafe_base64_encode(force_bytes(instance.pk)).decode()
#         token = account_activation_token.make_token(instance)
#         message = 'Please use this link to login http://' + \
#             str(current_site)+'/hostel/activate/'+str(uid)+'/'+str(token)+'/'

#         send_mail(subject, message, email_from, recipient_list)
#         return super().form_valid(form)

class Formview(FormView):
    template_name = "account/RegistrationForm.html"
    form_class = SendMailForm
    context_object_name = 'form'
    # redirect_field_name = "/hostel/client-map/"
    success_url = "/accounts/sendmail/"


def sendmail(request):
    form = SendMailForm(request.POST or None)
    if form.is_valid:
        email = form.data['email']
        subject = '----Web development-----'
        email_from = settings.EMAIL_HOST_USER
        current_site = get_current_site(request).domain
        message = 'Thank you for visiting our site homepage://' + \
            str(current_site)+'/'
        recipient_list = [email, ]
        task_sendmail.delay(subject, message, email_from, recipient_list)
        return HttpResponse('Please check your email')
    else:
        return HttpResponse('Invalid email')
