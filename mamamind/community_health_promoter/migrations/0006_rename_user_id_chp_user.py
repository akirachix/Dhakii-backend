# Generated by Django 5.1.1 on 2024-09-15 12:40

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("community_health_promoter", "0005_alter_chp_id"),
    ]

    operations = [
        migrations.RenameField(
            model_name="chp",
            old_name="user_id",
            new_name="user",
        ),
    ]