from django.db import models
from django.conf import settings

# class Code(models.Model):
#     alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*-[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')
#     code_name = models.CharField(max_length=10,null=True,blank=True, validators=[alphanumeric])
   

#     def __str__(self):
#         return self.code_name

class Category(models.Model):
    category_name = models.CharField(max_length=150, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['-id']

    def __str__(self):
        return self.category_name

    def recent_last_five_by_category(self, category=None):
        return self.objects.get(category__category_name=category)


class FlavorType(models.Model):
    flavor_type = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.flavor_type


class Cake(models.Model):

    cake = models.CharField(max_length=255)
    filling = models.CharField(max_length=255, null=True, blank=True)
    frosting = models.CharField(max_length=255, null=True, blank=True)
    category = models.ForeignKey(
        Category,on_delete=models.CASCADE,related_name='category_cake')
    flavor_type = models.ManyToManyField(
        FlavorType,related_name='flavor_cake')
    image = models.FileField(null=True, blank=True, upload_to='cake/')
    base_cost = models.DecimalField(
        max_digits=10, decimal_places=2, help_text='per pound')

    def __str__(self):
        return self.cake


class Order(models.Model):
    CHOICES1 = [
        ('Rectangle', 'Rectangle'),
        ('Round', 'Round'),
    ]
    STATUS_CHOICES=[
        ('r','Received'),
        ('p','Processing'),
        ('d','delivery'),
        ('c','cancelled')
    ]
    cakeId = models.ForeignKey(
        Cake, models.SET_NULL, related_name='order', null=True)
    decoration = models.CharField(
        help_text='Eg:Happy Bithday', max_length=255,null=True, blank=True)
    Shape = models.CharField(choices=CHOICES1, max_length=255, default='Round')
    eggless = models.BooleanField()
    accessories = models.BooleanField()
    sugerless = models.BooleanField()
    pickupdate = models.DateField()
    timetodeliver = models.TimeField(
        auto_now=False, auto_now_add=False, null=False, blank=False)
    deliverylocation = models.CharField(max_length=255, null=False, blank=True)
    contactno = models.PositiveIntegerField(null=True, blank=True)
    no_of_pounds = models.DecimalField(max_digits=10, decimal_places=2,default=1)
    quantity = models.PositiveIntegerField(default=1)
    category = models.ForeignKey(
        Category, related_name='cake_category', on_delete=models.SET_NULL,null=True)
    flavor_type = models.ForeignKey(
        FlavorType, related_name='cake_flavor_type',on_delete=models.SET_NULL,null=True, blank=True)
    total_cost= models.DecimalField(help_text='[[base_cost * pounds] + flavor_name * pounds] + Eggless + Accessories + sugerless]*quantity',max_digits=10,decimal_places=2)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES,default='r')
    # user_ins = models.ForeignKey(settings.AUTH_USER_MODEL, default=1,
    #                              null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return "Order no "+str(self.cakeId)

    class Meta:
         ordering = ('-pickupdate', )
