from rest_framework import serializers
from .models import MealType

class MealTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MealType
        fields = '__all__'
