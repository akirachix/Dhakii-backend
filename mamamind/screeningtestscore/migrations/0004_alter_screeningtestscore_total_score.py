# Generated by Django 5.1.1 on 2024-09-15 20:55

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("screeningtestscore", "0003_alter_screeningtestscore_total_score"),
    ]

    operations = [
        migrations.AlterField(
            model_name="screeningtestscore",
            name="total_score",
            field=models.PositiveSmallIntegerField(),
        ),
    ]