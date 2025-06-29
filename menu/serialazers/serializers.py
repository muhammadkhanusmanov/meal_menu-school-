from rest_framework import serializers
from .models import MealType, MenuItem

class MealTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MealType
        fields = '__all__'

class AdminMealTypeSerializer(serializers.ModelSerializer):
    """Admin uchun to'liq ma'lumotlar"""
    class Meta:
        model = MealType
        fields = '__all__'

class StudentMealTypeSerializer(serializers.ModelSerializer):
    """Student uchun faqat asosiy ma'lumotlar"""
    class Meta:
        model = MealType
        fields = ['id', 'name', 'display_order', 'is_active']

class ParentMealTypeSerializer(serializers.ModelSerializer):
    """Parent uchun o'rtacha ma'lumotlar"""
    class Meta:
        model = MealType
        fields = ['id', 'name', 'display_order', 'is_active', 'school_id']
        
class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = '__all__'

