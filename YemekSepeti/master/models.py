from django.db import models
from django.contrib.auth.models import User as AuthUser

# User Model
class User(AuthUser):
    pass

# Store Model
class Store(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

# Manager model to link users to stores
class Manager(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='managed_stores')
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='managers')

# Product Models
class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    is_customizable = models.BooleanField(default=False)

    class Meta:
        abstract = True

class MenuItem(Product):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name="menu_items")
    pass

class Ingredient(Product):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name="ingredients")
    pass

# Tracking default ingredients for a menu item
class DefaultIngredient(models.Model):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE, related_name='default_ingredients')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, related_name='used_in_defaults')

# Customization Option Model (to allow additional ingredients)
class CustomizationOption(models.Model):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE, related_name='customization_options')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, related_name='linked_customizations')
    extra_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

# Fixed Menu (Composite Campaigns)
class FixedMenu(models.Model):
    name = models.CharField(max_length=255)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='fixed_menus')
    items = models.ManyToManyField(MenuItem, related_name='included_in_fixed_menus')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

# Order Models
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='orders')
    order_date = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE, related_name='order_items')
    quantity = models.IntegerField(default=1)
    base_price = models.DecimalField(max_digits=10, decimal_places=2)

class OrderCustomization(models.Model):
    order_item = models.ForeignKey(OrderItem, on_delete=models.CASCADE, related_name='customizations')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, related_name='order_customizations')
    action = models.BooleanField()  # 0 for remove, 1 for add
    extra_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)