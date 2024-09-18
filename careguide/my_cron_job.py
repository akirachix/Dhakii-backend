
import requests
from bs4 import BeautifulSoup
from django_cron import CronJobBase, Schedule
import datetime

class CareGuideUpdateCronJob(CronJobBase):

    # Specify the schedule: run daily at midnight
    
    RUN_AT_TIMES = ['00:00']  
    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = 'care_guide.CareGuideUpdateCronJob'  

    def scrape_article(self, url):
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
       

    def do(self):
        from careguide.models import Careguide

        # Check if today is the first day of the month
        if datetime.datetime.now().day == 1:
            urls_scrape = [
                'https://magazine.medlineplus.gov/article/getting-help-for-mental-health/',
                'https://www.medicalnewstoday.com/articles/160774#micronutrients',
                'https://www.healthline.com/nutrition/10-reasons-why-good-sleep-is-important#2.-Can-improve-concentration-and-productivity',
                'https://www.betterhealth.vic.gov.au/health/healthyliving/postnatal-exercise',
            ]

            for url in urls_scrape:
                article_data = self.scrape_article(url)
                if article_data:
                    Careguide.objects.update_or_create(
                        title=article_data.get('Title', ''),
                        defaults={
                            'author': article_data.get('Author', ''),
                            'content': article_data.get('Content', '')
                        }
                    )
                    print(f'Successfully updated: {url}')
                else:
                    print(f'Failed to update data for {url}')
        else:
            print("Today is not the first day of the month. Skipping job.")
    
    



