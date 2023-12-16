from django.db import models
import datetime
# Create your models here.
class PostModel(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    passenger_name = models.CharField(max_length=255)  # Changed field name to snake_case
    date_of_journey = models.DateField()
    gender = models.CharField(max_length=1)
    flight_number = models.CharField(max_length=20)  # Changed to CharField assuming it can contain non-numeric characters
    pnr_number = models.CharField(max_length=20)  # Changed to CharField assuming it can contain non-numeric characters
    source = models.CharField(max_length=255)
    destination = models.CharField(max_length=255)
    baggage_space = models.IntegerField()  # Changed field name to snake_case
    is_checked = models.BooleanField(default=False)


