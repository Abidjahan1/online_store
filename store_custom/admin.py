from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from store.admin import ProductAdmin
from store.models import Product
from tags.models import TaggedITem
# Register your models here.

#generic relation allows you to tag any model with a tag
#here we are using GenericTabularInline to show the tags for each product
class TagInline(GenericTabularInline):
    model = TaggedITem
    autocomplete_fields = ['tag']  # enable autocomplete for tag field
    extra = 1  # show one empty form by default


class CustomProductAdmin(ProductAdmin):
    inlines = [TagInline]  # inline for tags
    list_display = ProductAdmin.list_display + ['tag_count']  # add tag count to list display

    @admin.display(ordering='tag_count')
    def tag_count(self, product):
        return TaggedITem.objects.filter(content_type__model='product', object_id=product.id).count()

admin.site.unregister(Product)  # unregister the original ProductAdmin
admin.site.register(Product, CustomProductAdmin)  # register the custom ProductAdmin