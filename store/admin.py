from django.contrib import admin,messages
from django.contrib.contenttypes.admin import GenericTabularInline
from .models import *
from django.db.models import Count
from django.utils.html import format_html,urlencode
from django.urls import reverse




# Register your models here.


class InventoryFilter(admin.SimpleListFilter):
    title = 'inventory'
    parameter_name = 'inventory'

    def lookups(self, request, model_admin):
        return [
            ('<10', 'Low'),
            ('>=10', 'OK')
        ]

    def queryset(self, request, queryset):
        if self.value() == '<10':
            return queryset.filter(inventory__lt=10)
        if self.value() == '>=10':
            return queryset.filter(inventory__gte=10)
        return queryset




@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # fields=['title','slug']
    # exclude =['promotion']
    # readonly_fields = ['last_update']
    prepopulated_fields = {'slug': ['title']} # auto generate slug from title
    actions = ['clear_inventory']
    autocomplete_fields = ['collection'] # enable autocomplete for collection field
    list_display = ['title',  'price',  'inventory_status', 'collection_title']
    list_editable = ['price']
    list_per_page = 50
    list_select_related = ['collection'] #prefetch related collection to reduce queries
    list_filter = ['collection', 'last_update',InventoryFilter]
    search_fields = ['title__istartswith', 'collection__title__istartswith'] #lookup type uppercase and lowercase and starts with
    
    @admin.display(ordering = 'inventory') # implement sorting by inventory
    def inventory_status(self,product):
        if product.inventory < 10:
            return 'LOW'
        return 'OK'
    
    @admin.display(ordering = 'collection__title') # implement sorting by collection title
    def collection_title(self,product):
        return product.collection.title
    
    @admin.action(description='Clear Inventory')
    def clear_inventory(self, request, queryset):
        updated_count = queryset.update(inventory=0)
        self.message_user(request,f'{updated_count} products were updated successfully.',
                         messages.SUCCESS )



# customize the list display for customer model
@admin.register(Customer)
class CustomerAdmin (admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'membership','orders_count']
    list_editable = ['membership']
    search_fields = ['first_name__istartswith', 'last_name__istartswith']#lookup type uppercase and lowercase and starts with
    list_filter = ['membership']
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

#stacked inline shows the form fields in a vertical layout
#tabular inline shows the form fields in a horizontal layout
#inline allows you to edit related models in the same page as the parent model
class OrderItemInline(admin.StackedInline):
    model = OrderItem
    autocomplete_fields = ['product']  # enable autocomplete for product field
    min_num = 1  # at least one order item is required
    max_num = 10  # maximum of 10 order items
    extra = 0  # no extra empty forms


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'placed_at', 'customer', 'payment_status']
    list_filter = ['payment_status']
    autocomplete_fields = ['customer']  # enable autocomplete for customer field
    search_fields = ['customer__first_name__istartswith', 'customer__last_name__istartswith']
    list_per_page = 20
    inlines = [OrderItemInline]  # inline for order items


# admin.site.register(Collection)

@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'products_count']
    list_per_page = 20
    search_fields = ['title__istartswith']

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
