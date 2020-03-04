from rest_framework import permissions, viewsets
from rest_framework.permissions import BasePermission
from .serializers import UserSerializer
from rest_framework.authentication import SessionAuthentication
from django.contrib.auth import get_user_model

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    serializer_class=UserSerializer
    queryset=User.objects.all()
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

        

    # def list(self,request):
    #     if self.request.user.is_authenticated:
    #         print('logged in' )    

