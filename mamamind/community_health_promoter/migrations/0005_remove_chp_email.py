# Generated by Django 5.1.1 on 2024-09-12 07:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('community_health_promoter', '0004_alter_chp_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chp',
            name='email',
        ),
    ]
