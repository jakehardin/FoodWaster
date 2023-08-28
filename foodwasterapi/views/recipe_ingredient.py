"""View module for handling requests about categories"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from foodwasterapi.models import RecipeIngredient

class RecipeIngredientView(ViewSet):
    """recipe_ingredient view"""

    def retrieve(self, request, pk):
        """DOCTSRING
        """
        try:
            recipe_ingredient = RecipeIngredient.objects.get(pk=pk)
            serializer = RecipeIngredientSerializer(recipe_ingredient)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except RecipeIngredient.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)


    def list(self, request):
        """Handle GET requests to get all category

        Returns:
            Response -- JSON serialized list of category
        """
        recipe_ingredient = RecipeIngredient.objects.all()
        serializer = RecipeIngredientSerializer(recipe_ingredient, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        """Handle GET requests for single Category
        Returns:
            Response -- JSON serialized Category
        """

        recipe_ingredient = RecipeIngredient.objects.create(
            label=request.data["label"],
        )
        serializer = RecipeIngredientSerializer(recipe_ingredient)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # def update(self, request, pk):
    #     """Handle PUT requests for a category

    #     Returns:
    #         Response -- Empty body with 204 status code
    #     """

    #     category = Category.objects.get(pk=pk)
    #     category.label = request.data["label"]
    #     category.description = request.data["description"]
    #     category.save()

    #     serializer = CategorySerializer(category)
    #     return Response(serializer.data, status=status.HTTP_200_OK)

    # def destroy(self, request, pk):

    #     category = Category.objects.get(pk=pk)
    #     category.delete()

    #     return Response(None, status=status.HTTP_204_NO_CONTENT)

    # def popular_genres(self, request):
    #     """
    #     Retrieve a list of popular genres based on the number of songs associated with each genre
    #     """

    #     genres = Genre.objects.annotate(song_count=Count('songs')).order_by('-song_count')[:1]

    #     serializer = SongsgitGenreSerializer(genres, many=True)
    #     return Response(serializer.data, status=status.HTTP_200_OK)

class RecipeIngredientSerializer(serializers.ModelSerializer):
    """JSON serializer for categories
    """
    class Meta:
        model = RecipeIngredient
        fields = ('id', 'recipe_id', 'ingredient_id')
