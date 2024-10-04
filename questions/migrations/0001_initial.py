
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
                ('question', models.TextField(unique=True)),
                ('option_1', models.TextField()),
                ('first_score', models.IntegerField()),
                ('option_2', models.TextField()),
                ('second_score', models.IntegerField()),
                ('option_3', models.TextField()),
                ('third_score', models.IntegerField()),
                ('option_4', models.TextField()),
                ('forth_score', models.IntegerField()),
            ],
        ),
    ]
