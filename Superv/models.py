from django.db import models

# Create your models here.


class Salerep(models.Model):
    numdepot = models.IntegerField(primary_key=True)
    total = models.IntegerField()
    nbrarticle = models.IntegerField()
    serveur = models.CharField(max_length=20, blank=True, null=True)
    datedepot = models.DateField()
    timedepot = models.TimeField(null=True, blank=True)

    class Meta:
        managed = True
        db_table = 'salerep'

class Sales(models.Model):
    numdepot = models.IntegerField()
    item = models.CharField(max_length=255, blank=True, null=True)
    unitprice = models.IntegerField()
    quantity = models.IntegerField()
    pricet = models.IntegerField(db_column='priceT')  # Field name made lowercase.
    date = models.DateField()
    saler = models.CharField(max_length=255, blank=True, null=True)
    tt = models.TimeField()
    id = models.IntegerField(primary_key=True)

    class Meta:
        managed = True
        db_table = 'sales'        