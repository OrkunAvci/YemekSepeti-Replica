from django.core.management.base import BaseCommand
from master.models import Order, OrderItem, OrderCustomization, Ingredient, MenuItem, Store
import random
from datetime import datetime, timedelta

class Command(BaseCommand):
	help = 'Populates orders for user ID 1 with random order items and customizations'

	def handle(self, *args, **kwargs):
		user_id = 1
		store = random.choice(Store.objects.all())
		menu_items = MenuItem.objects.filter(store=store)
		ingredients = Ingredient.objects.filter(store=store)
		
		if not menu_items:
			self.stdout.write(self.style.ERROR('No menu items available to add to orders.'))
			return
		
		# Generate random number of orders (between 3 and 5)
		num_orders = random.randint(3, 5)

		for _ in range(num_orders):
			# Create an order for user ID 1
			order_date = datetime.now() - timedelta(days=random.randint(1, 30))
			total_price = 0
			order = Order.objects.create(
				user_id=user_id,
				store_id=store.id,
				order_date=order_date,
				total_price=0  # Will calculate below
			)

			# Random number of order items (between 1 and 3 items)
			num_items = random.randint(1, 3)

			for _ in range(num_items):
				menu_item = random.choice(menu_items)
				quantity = random.randint(1, 3)
				total_price += (menu_item.price * quantity)

				order_item = OrderItem.objects.create(
					order=order,
					menu_item=menu_item,
					quantity=quantity,
					base_price=menu_item.price * quantity
				)

				# Random customizations for this order item (between 0 and 2)
				num_customizations = random.randint(0, 2)
				extra_costs = 0

				for _ in range(num_customizations):
					# Pick a random ingredient
					ingredient = random.choice(ingredients)
					action = random.choice([0, 1])  # 0 for remove, 1 for add
					cost = ingredient.price if action == 1 else 0
					extra_costs += (cost * quantity)
					
					# Create customization for this order item
					OrderCustomization.objects.create(
						order_item=order_item,
						ingredient=ingredient,
						action=action,
						extra_cost=cost
					)
				total_price += extra_costs

			# Update the order's total price
			order.total_price = total_price
			order.save()

		self.stdout.write(self.style.SUCCESS(f'Successfully populated {num_orders} orders for user ID {user_id}.'))
