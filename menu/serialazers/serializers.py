from rest_framework import serializers
from .models import MealType, MenuItem

class MealTypeDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = MealType
        fields = '__all__'
        
class MealTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MealType
        fields = ['id', 'name', 'display_order', 'is_active', 'school_id']

        
class MenuItemDetailSerializer(serializers.ModelSerializer):
    meal_type = MealTypeDetailSerializer()
    class Meta:
        model = MenuItem
        fields = '__all__'

class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ['id', 'name', 'image', 'meal_type', 'is_active']
        
class MenuItemCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = '__all__'

