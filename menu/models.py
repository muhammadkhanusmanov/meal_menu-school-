from django.db import models

class MealType(models.Model):
    name = models.CharField(max_length=100)
    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    school_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['display_order']

    def __str__(self):
        return self.name


class NutritionInfo(models.Model):
    calories = models.FloatField(help_text="kcal")
    protein = models.FloatField(help_text="grams")
    fats = models.FloatField(help_text="grams")
    carbs = models.FloatField(help_text="grams")

    def __str__(self):
        return f"{self.calories} kcal | P:{self.protein} F:{self.fats} C:{self.carbs}"


class MenuItem(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='menu_items/', blank=True, null=True)
    meal_type = models.ForeignKey(MealType, on_delete=models.CASCADE, related_name='menu_items')
    nutrition_info = models.ForeignKey(NutritionInfo, on_delete=models.SET_NULL, null=True, blank=True, related_name='menu_items')
    is_active = models.BooleanField(default=True)
    school_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class MenuSchedule(models.Model):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE, related_name='schedules')
    date = models.DateField()
    school_id = models.IntegerField()
    class_id = models.IntegerField()
    section_id = models.IntegerField()
    academic_year = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['menu_item', 'date', 'class_id', 'section_id', 'school_id']
        indexes = [
            models.Index(fields=['school_id', 'date']),
            models.Index(fields=['class_id', 'section_id', 'academic_year']),
        ]

    def __str__(self):
        return f"{self.menu_item.name} on {self.date} for Class {self.class_id}-{self.section_id}"
