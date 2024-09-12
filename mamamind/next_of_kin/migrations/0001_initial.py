# Generated by Django 5.0.7 on 2024-09-11 08:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('mother', '0003_remove_mother_location_remove_mother_next_of_kin_id_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='NextOfKin',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('relationship', models.CharField(max_length=50)),
                ('phone_number', models.CharField(max_length=15)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('mother_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='next_of_kin', to='mother.mother')),
            ],
        ),
    ]
