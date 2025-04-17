from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Category, Car, CarImage, Contact

class CarImageInline(admin.TabularInline):
    model = CarImage
    extra = 1

class CarAdmin(admin.ModelAdmin):
    inlines = [CarImageInline]
    list_display = ['make', 'model', 'year', 'price']
    search_fields = ['make', 'model']

class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'car', 'timestamp', 'status']
    list_editable = ['status']
    search_fields = ['name', 'email']

admin.site.register(Category)
admin.site.register(Car, CarAdmin)
admin.site.register(Contact, ContactAdmin)