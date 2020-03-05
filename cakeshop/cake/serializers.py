from rest_framework import serializers
from drf_yasg import openapi
from django.contrib.auth import get_user_model
from .models import Cake ,Order


User = get_user_model()


class CakeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cake
        fields = "__all__"

# class OrderSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Order
#         fields ='__all__'
#         extra_kwargs = {'user_ins': {'read_only': True},
#                         'timetodeliver':{'label': 'H:M'},
#                         'pickupdate':{'label': 'YYYY-MM-DD'},
#                         'text':{'label': 'text decoration for cake like Happy Birthday'},
#                        }

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields ='__all__'
        extra_kwargs = {'user_ins': {'read_only': True},
                        'timetodeliver':{'label': 'H:M'},
                        'pickupdate':{'label': 'YYYY-MM-DD'},
                        'text':{'label': 'text decoration for cake like Happy Birthday'},
                       }

        # swagger_schema_fields = {
        #     "type": openapi.TYPE_OBJECT,
        #     "title": "Email",
        #     "properties": {
        #         "subject": openapi.Schema(
        #             title="Email subject",
        #             type=openapi.TYPE_STRING,
        #         ),
        #         "body": openapi.Schema(
        #             title="Email body",
        #             type=openapi.TYPE_STRING,
        #         ),
        #     },
        #     "required": ["subject", "body"],
        #  }