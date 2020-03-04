from django.db import models
from django.conf import settings



class Cake(models.Model):
    
    cake = models.CharField(max_length=255)
    filling = models.CharField(max_length=255,null=True, blank=True)
    frosting = models.CharField(max_length=255,null=True, blank=True)
    flavour = models.CharField(max_length=255,null=True, blank=True)
    weight =  models.CharField(max_length=255,default='1 pound')
    cost = models.PositiveIntegerField(blank=True, null=True)
    

class Order(models.Model):
    CHOICES1 = [
        ('Rectangle', 'Rectangle'),
        ('Round', 'Round'),
    ]
    CHOICES2 = [
        ('Yes', 'Yes'),
        ('No', 'No'),
    ]
    cakeorder = models.ForeignKey(Cake , models.SET_NULL,related_name='order',null=True)
    text=models.CharField(max_length=255,default='Happy Birthday')
    Shape=models.CharField(choices=CHOICES1,max_length=255,default='Round')
    eggless=models.CharField(choices=CHOICES2,max_length=3,default='No')
    sugerless=models.CharField(choices=CHOICES2,max_length=3,default='No')
    pickupdate=models.DateField()
    timetodeliver=models.TimeField(auto_now=False, auto_now_add=False, null=False,blank=False)
    deliverylocation=models.CharField(max_length=255,null=False,blank=True)
    mobileno=models.PositiveIntegerField()
    quantity=models.PositiveIntegerField(default=1)
    user_ins = models.ForeignKey(settings.AUTH_USER_MODEL, default=1,
                                 null=True, on_delete=models.SET_NULL)