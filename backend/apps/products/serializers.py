from rest_framework import serializers
from .models import Product, Ingredient, ProductIngredient

class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'description', 'price', 'image', 'is_active')

class ProductIngredientSerializer(serializers.ModelSerializer):
    ingredient = IngredientSerializer(read_only=True)
    ingredient_id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(),
        source='ingredient',
        write_only=True
    )
    
    class Meta:
        model = ProductIngredient
        fields = ('id', 'ingredient', 'ingredient_id', 'is_default', 'max_quantity')

class ProductSerializer(serializers.ModelSerializer):
    ingredients = ProductIngredientSerializer(
        source='productingredient_set',
        many=True,
        read_only=True
    )
    
    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'base_price', 'image',
                 'is_active', 'ingredients', 'created_at', 'updated_at')

class ProductDetailSerializer(ProductSerializer):
    class Meta(ProductSerializer.Meta):
        fields = ProductSerializer.Meta.fields + ('available_ingredients',)

class ProductIngredientCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductIngredient
        fields = ('product', 'ingredient', 'is_default', 'max_quantity')
        
    def validate(self, data):
        # Verificar que el ingrediente no esté ya asociado al producto
        if ProductIngredient.objects.filter(
            product=data['product'],
            ingredient=data['ingredient']
        ).exists():
            raise serializers.ValidationError(
                "Este ingrediente ya está asociado al producto"
            )
        return data 