from django.contrib import admin
from .models import *
from django.db.models import Count
from django.utils.html import format_html,urlencode
from django.urls import reverse
# Register your models here.



@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title',  'price', 'inventory_status', 'collection_title']
    list_editable = ['price']
    list_per_page = 50
    list_select_related = ['collection'] #prefetch related collection to reduce queries

    @admin.display(ordering = 'inventory') # implement sorting by inventory
    def inventory_status(self,product):
        if product.inventory < 10:
            return 'LOW'
        return 'OK'
    
    @admin.display(ordering = 'collect ion__title') # implement sorting by collection title
    def collection_title(self,product):
        return product.collection.title



# customize the list display for customer model
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'membership','orders_count']
    list_editable = ['membership']
    search_fields = ['first_name__istartswith', 'last_name__istartswith']
    list_per_page = 12

    @admin.display(ordering='orders_count')
    def orders_count(self,customer):
        base_url =(
            reverse('admin:store_order_changelist')
            + '?' 
            + urlencode({
                'customer__id': str(customer.id)}
            ))
        return format_html('<a href ="{}">{}<a>',base_url,customer.orders_count)
    

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            orders_count=Count('order')
        )
        # return customer.order_set.count()


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'placed_at', 'customer', 'payment_status']
    list_filter = ['payment_status']
    search_fields = ['customer__first_name__istartswith', 'customer__last_name__istartswith']
    list_per_page = 20


# admin.site.register(Collection)

@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'products_count']
    list_per_page = 20

    @admin.display(ordering='products_count')
    def products_count(self,collection):
        base_url =( 
            reverse('admin:store_product_changelist') 
            + '?' 
            + urlencode({
                'collection__id': str(collection.id)
                }))
        return format_html('<a href ="{}">{}<a>',base_url,collection.products_count)
       
        # return collection.products_count

    #overriding the base query set for counting product in each collection
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            products_count=Count('product')
        )

# admin.site.register(models.Product, ProductAdmin)

#admin.site.register(models.Customer)
