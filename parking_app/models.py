from django.db import models

from datetime import datetime

class Category(models.Model):
    cat_id = models.AutoField(primary_key=True)
    parking_area_no = models.IntegerField(default=0)
    vehicle_type = models.CharField(max_length=100)
    parking_charge = models.FloatField(max_length=100)
    vehicle_limit = models.IntegerField()
    status = models.CharField(max_length=10, editable=True,default='activated')
    doc = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.vehicle_type
    def vehicle_count(self):
        parked_vehicles = Vehicle.objects.filter(vehicle_type=self.vehicle_type, status='parked').count()
        return parked_vehicles, self.vehicle_limit

class Vehicle(models.Model):
    id = models.AutoField(primary_key=True)
    vehicle_no = models.CharField(max_length=200)
    parking_area_no = models.IntegerField()
    vehicle_type = models.CharField(max_length=100)
    parking_charge = models.FloatField()
    arrival_time = models.DateTimeField(default=datetime.now, editable=True)
    status = models.CharField(max_length=10, editable=True,default='parked')

    def __str__(self):
        return self.vehicle_no

    def save(self, *args, **kwargs):
        category = Category.objects.get(vehicle_type=self.vehicle_type)
        parked_vehicles = Vehicle.objects.filter(vehicle_type=self.vehicle_type, status='parked').count()
        if parked_vehicles >= category.vehicle_limit:
            raise ValueError(f"Vehicle limit reached for {self.vehicle_type}")
        super().save(*args, **kwargs)