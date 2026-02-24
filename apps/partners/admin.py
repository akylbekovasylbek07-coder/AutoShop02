from django.contrib import admin
from apps.partners.models import Partners


@admin.register(Partners)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ("title", "link")
# Register your models here.
