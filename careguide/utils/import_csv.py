import csv
import os
import django
from datetime import datetime


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'careguide.settings')
django.setup()

from resources.models import Resources  

def read_csv(file_path):
    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        return list(reader)

def parse_date(date_str):
    try:
        return datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        return None  

def save_to_db(csv_data):
    for row in csv_data:
        try:
            title = row.get('title')
            content = row.get('content')
            author = row.get('author')
            published_date = row.get('published_date')
            
            if published_date:
                published_date = parse_date(published_date)
            
            
            print(f"Processing row: title={title}, content={content}, author={author}, published_date={published_date}")

            
            Resources.objects.create(
                title=title,
                content=content,
                author=author,
                published_date=published_date
            )
        except Exception as e:
            print(f"Error saving row with data {row}: {e}")

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        print("Usage: python import_csv.py /path/to/your/file.csv")
        sys.exit(1)

    csv_file_path = sys.argv[1]
    csv_data = read_csv(csv_file_path)
    save_to_db(csv_data)
    print("CSV import completed.")
