from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters import rest_framework as filters
from .models import Product, Ingredient, ProductIngredient
from .serializers import (
    ProductSerializer, ProductDetailSerializer,
    IngredientSerializer, ProductIngredientSerializer,
    ProductIngredientCreateSerializer
)

class ProductFilter(filters.FilterSet):
    min_price = filters.NumberFilter(field_name="base_price", lookup_expr='gte')
    max_price = filters.NumberFilter(field_name="base_price", lookup_expr='lte')
    
    class Meta:
        model = Product
        fields = ['is_active', 'min_price', 'max_price']

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly]
    filterset_class = ProductFilter
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ProductDetailSerializer
        return ProductSerializer
    
    @action(detail=True, methods=['post'])
    def add_ingredient(self, request, pk=None):
        serializer = ProductIngredientCreateSerializer(data={
            'product': pk,
            **request.data
        })
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors,
                      status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['delete'])
    def remove_ingredient(self, request, pk=None):
        try:
            ingredient_id = request.data.get('ingredient_id')
            product_ingredient = ProductIngredient.objects.get(
                product_id=pk,
                ingredient_id=ingredient_id
            )
            product_ingredient.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ProductIngredient.DoesNotExist:
            return Response(
                {"detail": "Ingrediente no encontrado en este producto"},
                status=status.HTTP_404_NOT_FOUND
            )

class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [IsAdminOrReadOnly]
    filterset_fields = ['is_active']
    
    @action(detail=True, methods=['get'])
    def products(self, request, pk=None):
        ingredient = self.get_object()
        products = ingredient.products.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data) 