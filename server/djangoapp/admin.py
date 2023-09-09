from django.contrib import admin
# from .models import related models
from .models import CarMake, CarModel

# Register your models here.
# CarModelInline class
class CarModelInline(admin.TabularInline):  # or admin.StackedInline if you prefer
    model = CarModel
    extra = 1  # Number of blank forms to display
    fields = ('car_make', 'dealer_id', 'car_type', 'year')  # Fields you want to display/edit in the inline form

# CarModelAdmin class
@admin.register(CarModel)
class CarModelAdmin(admin.ModelAdmin):
    list_display = ('car_make', 'dealer_id', 'car_type', 'year')  # Fields you want to display in the list view
    date_hierarchy = 'year'  # Create a date-based drilldown navigation by year

# CarMakeAdmin class with CarModelInline
@admin.register(CarMake)
class CarMakeAdmin(admin.ModelAdmin):
    inlines = [CarModelInline]
