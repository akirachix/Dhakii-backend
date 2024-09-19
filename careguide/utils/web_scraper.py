
import os
import django
import requests
from bs4 import BeautifulSoup
import sys
from datetime import datetime, timedelta

sys.path.append('/home/student/Documents/holder/Dhakii-backend/mamamind')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mamamind.settings')
django.setup()

from careguide.models import Careguide

# Defining URLs for scraping and extraction
urls_scrape = [
    'https://magazine.medlineplus.gov/article/getting-help-for-mental-health/',
    'https://www.medicalnewstoday.com/articles/160774#micronutrients',
    'https://www.healthline.com/nutrition/10-reasons-why-good-sleep-is-important#2.-Can-improve-concentration-and-productivity',
    'https://www.betterhealth.vic.gov.au/health/healthyliving/postnatal-exercise',
]

urls_extract = [
    'https://www.mentalhealth.org.uk/explore-mental-health/publications/our-best-mental-health-tips',
    'https://www.whattoexpect.com/first-year/postpartum/postpartum-diet-nutrition-questions-answered/',
    'https://nichq.org/insight/better-sleep-breastfeeding-mothers-safer-sleep-babies',
    'https://www.betterhealth.vic.gov.au/health/healthyliving/postnatal-exercise',
]

def scrape_article(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        title = soup.find('title').get_text(strip=True)
        author = ''
        author_meta = soup.find('meta', {'name': 'author'})
        if author_meta:
            author = author_meta.get('content', '').strip()
        else:
            author_tag = soup.find('span', class_='author') or soup.find('a', class_='author')
            if author_tag:
                author = author_tag.get_text(strip=True)

        body_content = soup.find('div', class_='main-content') or soup.find('div', id='content')
        text = ''
        if body_content:
            for unwanted in body_content.find_all(['footer', 'nav', 'aside']):
                unwanted.decompose()
            text = ' '.join([p.get_text(strip=True) for p in body_content.find_all('p')])

        return {
            'Title': title,
            'Author': author,
            'Content': text
        }
    except Exception as e:
        print(f'Error scraping article from {url}: {e}')
        return None

def extract_text(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        title = soup.find('title').get_text(strip=True)

        for tag in soup(['script', 'style', 'footer', 'nav', 'header']):
            tag.decompose()

        text = soup.get_text(separator=' ', strip=True)

        return {
            'URL': url,
            'Title': title,
            'Text': text
        }
    except Exception as e:
        print(f'Error extracting text from {url}: {e}')
        return None

def update_or_create_careguide(title, defaults):
    try:
        careguide, created = Careguide.objects.get_or_create(title=title)
        if created or (datetime.now() - careguide.last_updated > timedelta(days=30)):
            for key, value in defaults.items():
                setattr(careguide, key, value)
            careguide.save()
            print(f'Successfully saved or updated: {title}')
        else:
            print(f'No update needed for: {title}')
    except Exception as e:
        print(f'Failed to save or update {title}: {e}')

for url in urls_scrape:
    article_data = scrape_article(url)
    if article_data:
        update_or_create_careguide(
            article_data.get('Title', ''),
            {
                'author': article_data.get('Author', ''),
                'content': article_data.get('Content', '')
            }
        )
    else:
        print(f'Failed to get data for {url}')

for url in urls_extract:
    text_data = extract_text(url)
    if text_data:
        update_or_create_careguide(
            text_data.get('Title', ''),
            {
                'content': text_data.get('Text', ''),
                'author': ''
            }
        )
    else:
        print(f'Failed to get text for {url}')
