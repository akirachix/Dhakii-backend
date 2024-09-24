# Generated by Django 5.1.1 on 2024-09-22 20:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('careguide', '0003_rename_careguide_id_careguide_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='careguide',
            name='author',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='careguide',
            name='image',
            field=models.URLField(blank=True, default=1, max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='careguide',
            name='subtitle',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
    ]
