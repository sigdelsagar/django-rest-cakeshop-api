from django.contrib import admin
from .models import *


class CakeListAdmin(admin.ModelAdmin):
	list_display = ['id','cake','filling','frosting','flavour','weight','cost']
	search_fields = ['cake']
	list_per_page = 5

class OrderListAdmin(admin.ModelAdmin):
	list_display = ['timetodeliver','pickupdate','deliverylocation','mobileno','quantity','user_ins']
	search_fields = ['deliverylocation']
	list_per_page = 5

admin.site.register(Cake,CakeListAdmin)
admin.site.register(Order,OrderListAdmin)

