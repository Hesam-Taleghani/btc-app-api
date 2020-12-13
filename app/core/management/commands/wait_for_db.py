import time

from django.db import connections
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Pausing Django until the database is available"""

    def handle(self, *args, **options):
        """Try to make a connection to database every second until it's available."""
        self.stdout.write('Waiting for database...')
        db_conn = None
        while not db_conn:
            try:
                db_conn = connections['default']
            except OperationalError:
                self.stdout.write('Database Unavailable now, try again after 1 second...')
                time.sleep(1)
        
        self.stdout.write(self.style.SUCCESS('DataBase Available!'))
            