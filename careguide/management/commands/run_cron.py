

from django.core.management.base import BaseCommand
from careguide.my_cron_job import CareGuideUpdateCronJob

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        cron_job = CareGuideUpdateCronJob()
        cron_job.do()
