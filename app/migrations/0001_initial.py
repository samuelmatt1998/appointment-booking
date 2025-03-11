# Generated by Django 5.1.7 on 2025-03-11 04:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Appointment",
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
                ("name", models.CharField(max_length=100)),
                ("phone", models.CharField(max_length=15)),
                ("date", models.DateField()),
                ("time", models.TimeField()),
            ],
            options={
                "unique_together": {("date", "time")},
            },
        ),
    ]
