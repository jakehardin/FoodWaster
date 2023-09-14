from django.db import models
from .food_type import FoodType

class Ingredient(models.Model):
    """Model that represents an ingredient"""
    name = models.CharField(max_length=50)
    food_type = models.ForeignKey(FoodType, on_delete=models.CASCADE)
    uid = models.CharField(max_length=50)
    image = models.URLField()
    date = models.DateField()
