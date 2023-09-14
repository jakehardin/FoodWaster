from django.db import models

class FoodType(models.Model):
    """Model that represents a food type"""
    name = models.CharField(max_length=50)
