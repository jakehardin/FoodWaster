"""View module for handling requests about categories"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from foodwasterapi.models import FoodType

class FoodTypeView(ViewSet):
    """food type view"""

    def retrieve(self, request, pk):

        try:
            food_type = FoodType.objects.get(pk=pk)
            serializer = FoodTypeSerializer(food_type)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except FoodType.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)


    def list(self, request):
        """Handle GET requests to get all category

        Returns:
            Response -- JSON serialized list of category
        """
        food_type = FoodType.objects.all()
        serializer = FoodTypeSerializer(food_type, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        """Handle GET requests for single Category
        Returns:
            Response -- JSON serialized Category
        """

        food_type = FoodType.objects.create(
            name=request.data["name"],
        )
        serializer = FoodTypeSerializer(food_type)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        """Handle PUT requests for a category

        Returns:
            Response -- Empty body with 204 status code
        """

        food_type = FoodType.objects.get(pk=pk)
        food_type.name = request.data["name"]
        food_type.save()

        serializer = FoodTypeSerializer(food_type)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk):

        food_type = FoodType.objects.get(pk=pk)
        food_type.delete()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

class FoodTypeSerializer(serializers.ModelSerializer):
    """JSON serializer for categories
    """
    class Meta:
        model = FoodType
        fields = ('id', 'name')
