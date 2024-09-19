from django.core.management.base import BaseCommand
import csv
from resources.models import Resources

class Command(BaseCommand):
    help = 'Import data from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str)

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']
        with open(csv_file, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
            
                Resources.objects.update_or_create(
                    title=row['Title'],
                    defaults={
                        'author': row.get('Author', ''),

                        'content': row.get('Content', '')
                    }
                )
        self.stdout.write(self.style.SUCCESS(f'Successfully imported data from {csv_file}'))
