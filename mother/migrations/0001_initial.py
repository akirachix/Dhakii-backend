

import django.utils.timezone
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
                ('date_of_reg', models.DateField(default=django.utils.timezone.now)),
                ('no_of_children', models.PositiveIntegerField()),
                ('registered_date', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('tel_no', models.CharField(max_length=15)),
                ('marital_status', models.CharField(max_length=20)),
                ('sub_location', models.CharField(max_length=100)),
                ('village', models.CharField(max_length=100)),
                ('status', models.IntegerField(choices=[(1, 'Due Visit'), (0, 'Visited'), (-1, 'Missed Visit')], default=1, help_text='1: Due Visit, 0: Visited, -1: Missed Visit')),
            ],
        ),
    ]
