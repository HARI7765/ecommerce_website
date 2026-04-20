from django.core.management.base import BaseCommand
from app.views import fetch_medicines

class Command(BaseCommand):
    help = 'Fetch medicines from API'

    def handle(self, *args, **kwargs):
        fetch_medicines()
        self.stdout.write(self.style.SUCCESS('Products fetched!'))