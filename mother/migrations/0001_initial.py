# Generated by Django 5.1.1 on 2024-09-13 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Mother',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('date_of_birth', models.DateField()),
                ('no_of_children', models.IntegerField()),
                ('date_of_reg', models.DateField()),
                ('tel_no', models.CharField(max_length=15)),
                ('marital_status', models.CharField(max_length=20)),
                ('sub_location', models.CharField(max_length=100)),
                ('village', models.CharField(max_length=100)),
            ],
        ),
    ]