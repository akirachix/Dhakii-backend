# Generated by Django 5.1.1 on 2024-09-22 12:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('community_health_promoter', '0005_alter_chp_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chp',
            name='email',
            field=models.EmailField(max_length=255),
        ),
    ]
