# Generated by Django 5.1.1 on 2024-09-12 06:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('community_health_promoter', '0002_remove_chp_bio_description_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='chp',
            name='email',
            field=models.EmailField(default=1, max_length=255, unique=True),
            preserve_default=False,
        ),
    ]
