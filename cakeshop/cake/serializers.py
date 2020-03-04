from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Cake ,Order

User = get_user_model()


class CakeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cake
        fields = "__all__"

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields ='__all__'
        extra_kwargs = {'user_ins': {'read_only': True}
                       }


