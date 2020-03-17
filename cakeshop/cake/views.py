from .serializers import *
from .models import Cake, Order
from rest_framework import permissions, viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response
from weasyprint import HTML, CSS
from django.template.loader import get_template, render_to_string
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from .tasks import *
import os


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
    queryset = Order.objects.all()

    # def perform_create(self, serializer):
    #     serializer.save(user_ins=self.request.user)

    def get_permissions(self):
        permission_classes = [permissions.IsAdminUser]
        if self.action == 'create':
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]


def pdf_generation(request):
    """
    Convert report html to pdf
    """
    html_template = render_to_string('bill.html')
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    css = [os.path.join(BASE_DIR, 'static/css/', 'bill.css')]
    pdf_file = HTML(string=html_template).write_pdf(
        target='/home/kobey/Desktop/mypdf.pdf', stylesheets=css)  # this line creates pdf
    fs = FileSystemStorage('/home/kobey/Desktop')

    with fs.open('mypdf.pdf') as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="mypdf.pdf"'
        return response
    # return render(request,'bill.html')
    return response


def celeryCheck(request):
    task = publish_message.delay({'hello': 'World'})
    add.delay(2, 5)
    print(task)
    return HttpResponse('Celery is working..')
