# Generated by Django 5.1.1 on 2024-09-17 13:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('screeningtestscore', '0004_alter_screeningtestscore_total_score'),
    ]

    operations = [
        migrations.RenameField(
            model_name='screeningtestscore',
            old_name='chp',
            new_name='chp_id',
        ),
        migrations.RenameField(
            model_name='screeningtestscore',
            old_name='mother',
            new_name='mothe_id',
        ),
    ]