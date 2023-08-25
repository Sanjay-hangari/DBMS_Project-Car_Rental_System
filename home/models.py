from django.db import models
from django.db import models
from django.db import connections

# Create your models here. 
class cardetails(models.Model):
    uid=models.IntegerField()
    carname = models.CharField(max_length = 20) 
    color = models.CharField(max_length = 10) 
    city = models.CharField(max_length = 20) 
    pincode=models.IntegerField()
    capacity=models.IntegerField()
    transmission=models.CharField(max_length=10)
    fuel=models.CharField(max_length=10)
    price=models.CharField(max_length=10)

    class Meta:
        db_table = "cdetails"
        
class bookingg(models.Model):
    cid=models.IntegerField()
    did=models.CharField(max_length=5)
    uid=models.IntegerField()
    uname=models.CharField(max_length=20)
    carname=models.CharField(max_length=20)
    pickup=models.DateField()
    dp=models.DateField()
    tot_days=models.CharField(max_length=3)
    tot_price=models.CharField(max_length=10)

    class Meta:
        db_table="booking"