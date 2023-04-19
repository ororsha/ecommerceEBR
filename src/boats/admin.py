from django.contrib import admin

# Register your models here.
from .models import Boat


class BoatAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'slug']
    class Meta:
        model = Boat


admin.site.register(Boat, BoatAdmin)