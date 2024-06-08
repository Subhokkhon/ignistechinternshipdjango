from django.core.management.base import BaseCommand
from celery import current_app

class Command(BaseCommand):
    help = 'Run the Celery worker'

    def handle(self, *args, **options):
        current_app.worker_main(['worker', '--loglevel=info'])
