from django.db import models

class Appointment(models.Model):
    name = models.CharField(max_length=100)
    phone = models.PositiveBigIntegerField()  # Removed `max_length`
    date = models.DateField()
    time = models.TimeField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['date', 'time'], name='unique_appointment_slot')
        ]  # Preferred way in Django ≥3.0

    def __str__(self):
        return f"{self.name} - {self.date} at {self.time}"


