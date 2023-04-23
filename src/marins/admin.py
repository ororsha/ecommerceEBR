from django.contrib import admin

# Register your models here.
from .models import Marin


class MarinAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'slug']
    class Meta:
        model = Marin


admin.site.register(Marin, MarinAdmin)