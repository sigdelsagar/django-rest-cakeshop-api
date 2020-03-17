from django.contrib import admin
from .models import *
from django.utils.translation import gettext_lazy as _


class QuantityListFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = _('Quantity')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'decade'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            ('80s', _('Highest no of Quantity')),
            ('90s', _('Lowest no of Quantity')),
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value (either '80s' or '90s')
        # to decide how to filter the queryset.
        if self.value() == '80s':
            return queryset.order_by('-quantity')
        if self.value() == '90s':
            return queryset.order_by('quantity')


class CakeListAdmin(admin.ModelAdmin):
    list_display = ['id', 'cake', 'filling', 'frosting', 'flavor',
                    'category', 'base_cost']
    search_fields = ['cake']
    list_filter = ['category', 'flavor_type']
    list_per_page = 5

    def flavor(self, obj):
        # return obj.flavor_type.all()
        return ", ".join([str(p) for p in obj.flavor_type.all()])


class OrderListAdmin(admin.ModelAdmin):
    list_display = ['cakeId', 'pickupdate',
                    'contactno', 'quantity', 'flavor_type', 'category', 'status']
    search_fields = ['deliverylocation']
    list_filter = ['category', 'flavor_type', 'status', QuantityListFilter]
    list_per_page = 5

    # def flavor(self, obj):
    #     return ", ".join([str(p) for p in obj.flavor_type.all()])


# class FlavourListAdmin(admin.ModelAdmin):
#     list_display = ['id', 'cake', 'filling', 'frosting',
#                     'category', 'base_cost']
#     search_fields = ['cake']
#     list_filter = ['category', 'flavor_type']
#     list_per_page = 5


admin.site.register(Cake, CakeListAdmin)
admin.site.register(Order, OrderListAdmin)
admin.site.register(FlavorType)
admin.site.register(Category)
