"""View module for handling requests about categories"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from foodwasterapi.models import Ingredient, FoodType, Recipe, RecipeIngredient
from rest_framework.decorators import action

class IngredientView(ViewSet):
    """food type view"""

    def retrieve(self, request, pk):
        """DOCSTRING
        """
        ingredient = Ingredient.objects.get(pk=pk)
        serializer = IngredientSerializer(ingredient)
        return Response(serializer.data)


    def list(self, request):
        """Handle GET requests to get all category

        Returns:
            Response -- JSON serialized list of category
        """
        ingredients = Ingredient.objects.all()
        uid = request.query_params.get('uid', None)
        if uid is not None:
            ingredients = ingredients.filter(uid=uid)
        serializer = IngredientSerializer(ingredients, many=True)
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
    
    # Custom action that adds a book to a customer
    @action(methods=['post'], detail=True)
    def addtorecipe(self, request, pk):
        """Add Book To Customer"""
        # Get the Customer instance using the customerId from the request data
        recipe = Recipe.objects.get(pk=request.data["recipeId"])
        # Get the Book instance using the primary key (pk) parameter
        ingredient = Ingredient.objects.get(pk=pk)
            
        # Create a CustomerBook instance linking the customer and book
        RecipeIngredient.objects.create(
            recipe=recipe,
            ingredient=ingredient
        )
        return Response({'message': 'Book added to Customer'}, status=status.HTTP_201_CREATED)
    
    @action(methods=['delete'], detail=True)
    def removefromrecipe(self, request, pk):
        """Remove Book From Customer"""
        # Get the Customer instance using the customerId from the request data
        recipe = Recipe.objects.get(pk=request.data["recipeId"])
        # Get the Book instance using the primary key (pk) parameter
        ingredient = Ingredient.objects.get(pk=pk)
            
        # Get the specific CustomerBook instance connecting the customer and book
        recipe_ingredient = RecipeIngredient.objects.get(
            recipe_id=recipe.id,
            ingredient_id=ingredient.id
        )
        
        # Delete the CustomerBook instance            
        recipe_ingredient.delete()
        
        # Return a success response
        return Response({'message': 'Book removed from Customer'}, status=status.HTTP_204_NO_CONTENT)

class IngredientSerializer(serializers.ModelSerializer):
    """JSON serializer for categories
    """
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'food_type', 'uid', 'date')
