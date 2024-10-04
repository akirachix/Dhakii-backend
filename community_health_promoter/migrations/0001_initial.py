

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CHP',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('registered_date', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('reg_no', models.CharField(max_length=255)),
                ('location', models.TextField()),
                ('sub_location', models.CharField(max_length=255)),
                ('village', models.CharField(max_length=255)),
            ],
        ),
    ]
