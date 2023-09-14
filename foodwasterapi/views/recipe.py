"""View module for handling requests about categories"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from foodwasterapi.models import Recipe, RecipeIngredient
from rest_framework.decorators import action
class RecipeView(ViewSet):
    """recipe view"""

    def retrieve(self, request, pk):
        """DOCTSRING
        """
        try:
            recipe = Recipe.objects.get(pk=pk)
            serializer = RecipeSerializer(recipe)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Recipe.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)


    def list(self, request):
        """Handle GET requests to get all category

        Returns:
            Response -- JSON serialized list of category
        """
        recipes = Recipe.objects.all()
        uid = request.query_params.get('uid', None)
        if uid is not None:
            recipes = recipes.filter(uid=uid)
        serializer = RecipeSerializer(recipes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        """Handle GET requests for single Category
        Returns:
            Response -- JSON serialized Category
        """

        recipe = Recipe.objects.create(
            name=request.data["name"],
            description=request.data["description"],
            uid=request.data["uid"],
            completed=request.data["completed"],
        )
        serializer = RecipeSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        """Handle PUT requests for a category

        Returns:
            Response -- Empty body with 204 status code
        """

        recipe = Recipe.objects.get(pk=pk)
        recipe.name = request.data["name"]
        recipe.description = request.data["description"]
        recipe.completed = request.data["completed"]
        recipe.save()

        serializer = RecipeSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk):

        recipe = Recipe.objects.get(pk=pk)
        recipe.delete()

        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    @action(methods=['get'], detail=True)
    def get_ingredients(self, request, pk):
        """Get the books for the customer"""
        try:
            recipe_ingredients = RecipeIngredient.objects.filter(recipe_id = pk)
            serializer = RecipeIngredientSerializer(recipe_ingredients, many=True)
            return Response(serializer.data)
        except RecipeIngredient.DoesNotExist:
            return Response(False)
        
class RecipeIngredientSerializer(serializers.ModelSerializer):
    """JSON serializer for categories
    """
    class Meta:
        model = RecipeIngredient
        fields = ('id', 'recipe', 'ingredient')
        depth = 1

class RecipeSerializer(serializers.ModelSerializer):
    """JSON serializer for categories
    """
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'description', 'completed')
        depth = 1
