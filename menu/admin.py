from django.contrib import admin
from .models import MealType, MenuSchedule, NutritionInfo, MenuItem

admin.site.register(MealType)
admin.site.register(MenuSchedule)
admin.site.register(NutritionInfo)
admin.site.register(MenuItem)
