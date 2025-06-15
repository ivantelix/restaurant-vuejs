from django.db import models

class Product(models.Model):
    name = models.CharField('Nombre', max_length=100)
    description = models.TextField('Descripción')
    base_price = models.DecimalField('Precio Base', max_digits=10, decimal_places=2)
    image = models.ImageField('Imagen', upload_to='products/', blank=True, null=True)
    is_active = models.BooleanField('Activo', default=True)
    created_at = models.DateTimeField('Fecha de Creación', auto_now_add=True)
    updated_at = models.DateTimeField('Fecha de Actualización', auto_now=True)
    
    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name

class Ingredient(models.Model):
    name = models.CharField('Nombre', max_length=100)
    description = models.TextField('Descripción', blank=True, null=True)
    price = models.DecimalField('Precio Adicional', max_digits=10, decimal_places=2)
    image = models.ImageField('Imagen', upload_to='ingredients/', blank=True, null=True)
    is_active = models.BooleanField('Activo', default=True)
    products = models.ManyToManyField(
        Product,
        through='ProductIngredient',
        related_name='available_ingredients'
    )
    created_at = models.DateTimeField('Fecha de Creación', auto_now_add=True)
    updated_at = models.DateTimeField('Fecha de Actualización', auto_now=True)
    
    class Meta:
        verbose_name = 'Ingrediente'
        verbose_name_plural = 'Ingredientes'
        ordering = ['name']
    
    def __str__(self):
        return self.name

class ProductIngredient(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    is_default = models.BooleanField('Ingrediente por Defecto', default=False)
    max_quantity = models.PositiveIntegerField('Cantidad Máxima', default=1)
    
    class Meta:
        verbose_name = 'Ingrediente del Producto'
        verbose_name_plural = 'Ingredientes del Producto'
        unique_together = ['product', 'ingredient']
    
    def __str__(self):
        return f"{self.product.name} - {self.ingredient.name}" 