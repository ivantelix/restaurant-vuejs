from rest_framework import serializers
from .models import Order, OrderItem, OrderItemIngredient
from apps.products.serializers import ProductSerializer, IngredientSerializer
from apps.products.models import Ingredient, Product

class OrderItemIngredientSerializer(serializers.ModelSerializer):
    ingredient = IngredientSerializer(read_only=True)
    ingredient_id = serializers.PrimaryKeyRelatedField(
        write_only=True,
        queryset=Ingredient.objects.all(),
        source='ingredient'
    )
    
    class Meta:
        model = OrderItemIngredient
        fields = ('id', 'ingredient', 'ingredient_id', 'quantity')

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        write_only=True,
        queryset=Product.objects.all(),
        source='product'
    )
    selected_ingredients = OrderItemIngredientSerializer(
        source='ingredient_selections',
        many=True,
        read_only=True
    )
    ingredients = serializers.ListField(
        child=serializers.DictField(),
        write_only=True,
        required=False
    )
    
    class Meta:
        model = OrderItem
        fields = ('id', 'product', 'product_id', 'quantity', 'unit_price',
                 'selected_ingredients', 'ingredients')
    
    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients', [])
        order_item = OrderItem.objects.create(**validated_data)
        
        for ingredient_data in ingredients_data:
            OrderItemIngredient.objects.create(
                order_item=order_item,
                ingredient_id=ingredient_data['ingredient_id'],
                quantity=ingredient_data.get('quantity', 1)
            )
        
        return order_item

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    order_items = serializers.ListField(
        child=serializers.DictField(),
        write_only=True
    )
    
    class Meta:
        model = Order
        fields = ('id', 'user', 'status', 'total', 'notes', 'items',
                 'order_items', 'created_at', 'updated_at')
        read_only_fields = ('user', 'total', 'created_at', 'updated_at')
    
    def create(self, validated_data):
        items_data = validated_data.pop('order_items')
        order = Order.objects.create(
            user=self.context['request'].user,
            **validated_data
        )
        
        for item_data in items_data:
            product = Product.objects.get(id=item_data['product_id'])
            order_item = OrderItem.objects.create(
                order=order,
                product=product,
                quantity=item_data['quantity'],
                unit_price=product.base_price
            )
            
            for ingredient_data in item_data.get('ingredients', []):
                OrderItemIngredient.objects.create(
                    order_item=order_item,
                    ingredient_id=ingredient_data['ingredient_id'],
                    quantity=ingredient_data.get('quantity', 1)
                )
        
        order.calculate_total()
        return order

class OrderUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('status', 'notes')
        
    def validate_status(self, value):
        if self.instance.status == 'completed':
            raise serializers.ValidationError(
                "No se puede modificar una orden completada"
            )
        return value 