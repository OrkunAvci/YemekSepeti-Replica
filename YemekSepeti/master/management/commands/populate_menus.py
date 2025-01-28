import random
from faker import Faker
from django.core.management.base import BaseCommand
from master.models import Store, MenuItem, Ingredient, DefaultIngredient

class Command(BaseCommand):
	help = 'Populate the database with random menu items and ingredients for each store'

	def handle(self, *args, **kwargs):
		fake = Faker()
		stores = Store.objects.all()
		ingredient_names = [
			"Lettuce", "Tomato", "Cheese", "Bacon", "Onions", "Pickles", 
			"Olives", "Mushrooms", "Egg", "Chicken", "Beef", "Ketchup", 
			"Mustard", "Mayo", "Sauce"
		]

		for store in stores:
			# Random number of menu items per store
			num_items = random.randint(3, 7)  # Random between 3 to 7 items

			for _ in range(num_items):
				# Generate random menu item details
				item_name = fake.word().capitalize() + " " + fake.word().capitalize()  # e.g., "Burger Fries"
				item_description = fake.sentence()
				item_price = round(random.uniform(5.00, 20.00), 2)  # Random price between 5.00 to 20.00

				# Create a menu item for the store
				menu_item = MenuItem(
					name=item_name,
					description=item_description,
					price=item_price,
					store=store,
					is_customizable=random.choice([True, False])  # Randomly set whether item is customizable
				)
				menu_item.save()

				if menu_item.is_customizable:
					# Random number of ingredients per menu item
					num_ingredients = random.randint(2, 5)  # Random between 2 to 5 ingredients
					for _ in range(num_ingredients):
						ingredient_name = random.choice(ingredient_names)
						ingredient_price = round(random.uniform(0.5, 2.00), 2)  # Random extra price for the ingredient

						# Create the ingredient
						ingredient = Ingredient(
							name=ingredient_name,
							description=f"A tasty {ingredient_name}",
							price=ingredient_price,
							store=store
						)
						ingredient.save()

						# Add the ingredient to the menu item's default ingredients
						DefaultIngredient.objects.create(
							menu_item=menu_item,
							ingredient=ingredient
						)

			self.stdout.write(self.style.SUCCESS(f'Successfully created {num_items} items for store: {store.name}'))
