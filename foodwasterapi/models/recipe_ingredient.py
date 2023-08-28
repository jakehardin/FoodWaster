from django.db import models
from .recipe import Recipe
from .ingredient import Ingredient

class RecipeIngredient(models.Model):

    recipe_id = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient_id = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
