from django.contrib import admin
from .models import Tag
# Register your models here.

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['label']
    search_fields = ['label__istartswith']  # lookup type uppercase and lowercase and starts with
    list_per_page = 50
    