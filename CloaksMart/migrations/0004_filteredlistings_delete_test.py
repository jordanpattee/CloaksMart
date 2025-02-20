# Generated by Django 4.2.15 on 2024-08-31 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("CloaksMart", "0003_delete_cloakslistings"),
    ]

    operations = [
        migrations.CreateModel(
            name="FilteredListings",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("token_id", models.IntegerField()),
                ("price_eth", models.FloatField()),
                ("price_usd", models.FloatField()),
                (
                    "marketplace",
                    models.CharField(
                        choices=[("os", "OpenSea"), ("blur", "Blur")], max_length=200
                    ),
                ),
                ("marketplace_icon", models.CharField(max_length=200)),
                ("url", models.CharField(max_length=200)),
                ("royalty", models.CharField(max_length=200)),
                ("seller", models.CharField(max_length=200)),
                ("image", models.CharField(max_length=200)),
                ("power", models.IntegerField()),
                ("magic", models.IntegerField()),
                ("agility", models.IntegerField()),
                ("statsAvg", models.FloatField()),
                ("collection_rank", models.IntegerField()),
                ("percentile", models.FloatField()),
                ("accessory", models.CharField(max_length=200)),
                ("clan", models.CharField(max_length=200)),
                ("form", models.CharField(max_length=200)),
                ("clan_type", models.CharField(max_length=200)),
            ],
        ),
        migrations.DeleteModel(
            name="test",
        ),
    ]
