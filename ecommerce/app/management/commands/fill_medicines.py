from django.core.management.base import BaseCommand
from app.models import Product, Category
import requests
import random


class Command(BaseCommand):
    help = "Fill database with medicines"

    def handle(self, *args, **kwargs):
        category, _ = Category.objects.get_or_create(name="Medicines")

        self.stdout.write("Fetching medicines...")

        url = "https://api.fda.gov/drug/label.json?limit=10"

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json().get("results", [])

            count = 0

            for item in data:
                openfda = item.get("openfda", {})

                name_list = openfda.get("brand_name") or openfda.get("generic_name") or ["Unknown"]
                name = name_list[0]

                desc_list = item.get("purpose") or item.get("indications_and_usage") or ["No description"]
                description = desc_list[0]

                price = round(random.uniform(10, 200), 2)
                stock = random.randint(10, 100)

                obj, created = Product.objects.get_or_create(
                    name=name,
                    defaults={
                        "description": description,
                        "price": price,
                        "stock": stock,
                        "category": category,
                    }
                )

                if created:
                    count += 1

            self.stdout.write(self.style.SUCCESS(f"Added {count} medicines"))

        except Exception as e:
            self.stderr.write(str(e))