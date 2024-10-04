

import tinymce.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Careguide',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('category', models.CharField(max_length=200)),

                ('title', models.CharField(max_length=255)),
                ('image', models.URLField(blank=True, max_length=255)),
                ('subtitle', models.CharField(max_length=255)),
                ('content', tinymce.models.HTMLField()),
                ('author', models.CharField(max_length=100)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
    ]
