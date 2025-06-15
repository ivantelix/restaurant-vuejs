from django.db import models
from django.conf import settings
from apps.products.models import Product, Ingredient

class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pendiente'),
        ('accepted', 'Aceptado'),
        ('rejected', 'Rechazado'),
        ('completed', 'Completado'),
    )
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='orders'
    )
    status = models.CharField(
        'Estado',
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    total = models.DecimalField(
        'Total',
        max_digits=10,
        decimal_places=2,
        default=0
    )
    notes = models.TextField('Notas', blank=True, null=True)
    created_at = models.DateTimeField('Fecha de Creación', auto_now_add=True)
    updated_at = models.DateTimeField('Fecha de Actualización', auto_now=True)
    
    class Meta:
        verbose_name = 'Orden'
        verbose_name_plural = 'Órdenes'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Orden #{self.id} - {self.user.username}"
    
    def calculate_total(self):
        total = sum(item.calculate_subtotal() for item in self.items.all())
        self.total = total
        self.save()

class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField('Cantidad', default=1)
    unit_price = models.DecimalField(
        'Precio Unitario',
        max_digits=10,
        decimal_places=2
    )
    selected_ingredients = models.ManyToManyField(
        Ingredient,
        through='OrderItemIngredient',
        related_name='order_items'
    )
    
    class Meta:
        verbose_name = 'Item de Orden'
        verbose_name_plural = 'Items de Orden'
    
    def __str__(self):
        return f"{self.quantity}x {self.product.name}"
    
    def calculate_subtotal(self):
        base_total = self.quantity * self.unit_price
        ingredients_total = sum(
            item.ingredient.price * item.quantity
            for item in self.ingredient_selections.all()
        )
        return base_total + ingredients_total

class OrderItemIngredient(models.Model):
    order_item = models.ForeignKey(
        OrderItem,
        on_delete=models.CASCADE,
        related_name='ingredient_selections'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField('Cantidad', default=1)
    
    class Meta:
        verbose_name = 'Ingrediente de Item'
        verbose_name_plural = 'Ingredientes de Items'
        unique_together = ['order_item', 'ingredient']
    
    def __str__(self):
        return f"{self.order_item.product.name} - {self.ingredient.name} x{self.quantity}" 