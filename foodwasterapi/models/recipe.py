from django.db import models


class Recipe(models.Model):
    """DOCTSRING
    """
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=50)
    completed = models.BooleanField(null=True, blank=True)
