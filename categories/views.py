from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Category
from .serializer import CategorySerializer

class CategoriesView():
    @api_view(['GET'])
    def categoriesList(request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)
    
    @api_view(['POST'])
    def categoriesCreate(request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @api_view(['GET','PUT', 'DELETE'])
    def categoriesDetail(request, pk):
        try:
            categoria = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == 'GET':
            serializer = CategorySerializer(categoria)
            return Response(serializer.data)

        if request.method == 'PUT':
            serializer = CategorySerializer(categoria, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            categoria.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)