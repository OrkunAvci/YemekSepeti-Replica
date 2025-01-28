from faker import Faker
from django.core.management.base import BaseCommand

from master.models import Store

class Command(BaseCommand):
    help = 'Populate the database with random store data'

    def handle(self, *args, **kwargs):
        fake = Faker()

        # Number of stores to generate
        num_stores = 10  # Change this as needed

        for _ in range(num_stores):
            # Generate random data using Faker
            name = fake.company()
            address = fake.address()
            
            # Create a new Store entry
            store = Store(
                name=name,
                address=address
            )
            store.save()

            self.stdout.write(self.style.SUCCESS(f'Successfully created store: {name}'))

