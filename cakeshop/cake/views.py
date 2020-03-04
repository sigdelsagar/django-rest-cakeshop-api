from .serializers import *
from .models import Cake,Order
from rest_framework import permissions, viewsets, filters
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.schemas.openapi import AutoSchema
from rest_framework.compat import coreapi, coreschema
from rest_framework.schemas import ManualSchema

class CakeViewSet(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication]
    queryset = Cake.objects.all()
    serializer_class = CakeSerializer

    def get_permissions(self):
        permission_classes = [permissions.IsAdminUser]
        if self.action == 'list':
            permission_classes = [permissions.IsAuthenticatedOrReadOnly]
        return [permission() for permission in permission_classes]

    # def list(self, request):
    #     """
    #         View the list of cake with individual costs
    #     """
    #     from rest_framework.response import Response
    #     print(request.session.get('test','0'))
    #     # request.session['test']=1
    #     print(request.session.get('test'))
        
    #     queryset = Cake.objects.all()
    #     serializer = CakeSerializer(queryset, many=True)
    #     return Response(serializer.data)



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