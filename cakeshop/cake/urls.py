from django.urls import path,include
from . import views
from accounts.views import UserViewSet
from rest_framework import permissions
from rest_framework import routers

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="CakeShop API",
      default_version='',
 
   ),
   public=True,
#    authentication_classes=(BasicAuthentication,),
   permission_classes=(permissions.IsAuthenticatedOrReadOnly,),
)


router = routers.DefaultRouter()
router.register(r'cake', views.CakeViewSet)
router.register(r'order', views.PlaceOrder,basename='place-order')
router.register(r'user', UserViewSet)

urlpatterns = [
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/', include(router.urls), name='rest-api'),
    path('swagger/', schema_view.with_ui('swagger')),
    path('bill/',views.pdf_generation,name='pdf-gen'),
    path('celery/',views.celeryCheck,name='celery-check')
    
    # path('order/', views.PlaceOrder.as_view()),
    
]
