"""View module for handling requests about categories"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from foodwasterapi.models import Ingredient, FoodType

class IngredientView(ViewSet):
    """food type view"""

    def retrieve(self, request, pk):

        try:
            ingredient = Ingredient.objects.get(pk=pk)
            serializer = IngredientSerializer(ingredient)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Ingredient.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)


    def list(self, request):
        """Handle GET requests to get all category

        Returns:
            Response -- JSON serialized list of category
        """
        ingredient = Ingredient.objects.all()
        serializer = IngredientSerializer(ingredient, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        """Handle GET requests for single Category
        Returns:
            Response -- JSON serialized Category
        """
        food_type = FoodType.objects.get(id=request.data["food_type"])

        ingredient = Ingredient.objects.create(
            name=request.data["name"],
            food_type=food_type,
            uid=request.data["uid"],
            date=request.data["date"],
        )
        serializer = IngredientSerializer(ingredient)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        """Handle PUT requests for a category

        Returns:
            Response -- Empty body with 204 status code
        """

        ingredient = Ingredient.objects.get(pk=pk)
        ingredient.name = request.data["name"]
        food_type = FoodType.objects.get(pk=request.data["food_type"])
        ingredient.food_type = food_type
        ingredient.save()

        serializer = IngredientSerializer(ingredient)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk):

        ingredient = Ingredient.objects.get(pk=pk)
        ingredient.delete()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

class IngredientSerializer(serializers.ModelSerializer):
    """JSON serializer for categories
    """
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'food_type', 'uid', 'date')
