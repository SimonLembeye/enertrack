# Generated by Django 3.1 on 2020-08-27 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("enertrack", "0004_date_forecast"),
    ]

    operations = [
        migrations.AlterField(
            model_name="forecast", name="start_date", field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name="forecast", name="updated_date", field=models.DateTimeField(),
        ),
    ]
