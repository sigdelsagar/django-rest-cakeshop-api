from .serializers import *
from .models import Cake,Order
from rest_framework import permissions, viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response


class CakeViewSet(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication]
    queryset = Cake.objects.all()
    serializer_class = CakeSerializer

    def get_permissions(self):
        permission_classes = [permissions.IsAdminUser]
        if self.action == 'list':
            permission_classes = [permissions.IsAuthenticatedOrReadOnly]
        return [permission() for permission in permission_classes]


class PlaceOrder(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    queryset= Order.objects.all()
    

    def perform_create(self, serializer):
        serializer.save(user_ins=self.request.user)

    def get_permissions(self):
        permission_classes = [permissions.IsAdminUser]
        if self.action == 'create':
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]