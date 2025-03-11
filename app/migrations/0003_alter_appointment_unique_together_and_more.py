# Generated by Django 5.1.7 on 2025-03-11 05:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0002_alter_appointment_phone"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="appointment",
            unique_together=set(),
        ),
        migrations.AlterField(
            model_name="appointment",
            name="phone",
            field=models.PositiveBigIntegerField(),
        ),
        migrations.AddConstraint(
            model_name="appointment",
            constraint=models.UniqueConstraint(
                fields=("date", "time"), name="unique_appointment_slot"
            ),
        ),
    ]
