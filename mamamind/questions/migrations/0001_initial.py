# Generated by Django 5.1.1 on 2024-09-11 09:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EPDSQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.TextField()),
                ('option_1', models.CharField(max_length=255)),
                ('first_score', models.IntegerField()),
                ('option_2', models.CharField(max_length=255)),
                ('second_score', models.IntegerField()),
                ('option_3', models.CharField(max_length=255)),
                ('third_score', models.IntegerField()),
                ('option_4', models.CharField(max_length=255)),
                ('forth_score', models.IntegerField()),
            ],
        ),
    ]