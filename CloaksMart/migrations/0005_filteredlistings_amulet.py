# Generated by Django 4.2.15 on 2024-09-17 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("CloaksMart", "0004_filteredlistings_delete_test"),
    ]

    operations = [
        migrations.AddField(
            model_name="filteredlistings",
            name="amulet",
            field=models.CharField(default=None, max_length=200),
            preserve_default=False,
        ),
    ]