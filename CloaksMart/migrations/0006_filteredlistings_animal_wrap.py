# Generated by Django 4.2.15 on 2024-09-17 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("CloaksMart", "0005_filteredlistings_amulet"),
    ]

    operations = [
        migrations.AddField(
            model_name="filteredlistings",
            name="animal_wrap",
            field=models.CharField(default=None, max_length=200),
            preserve_default=False,
        ),
    ]
