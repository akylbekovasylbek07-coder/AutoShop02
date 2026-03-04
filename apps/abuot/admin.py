from django.contrib import admin
from apps.abuot.models import *
from apps.abuot.models import Slider


admin.site.register(AboutContent)
admin.site.register(PlusAbout)
admin.site.register(BlogAbout)
admin.site.register(Fag)
admin.site.register(Testimonials)





@admin.register(Slider)
class SliderAdmin(admin.ModelAdmin):
    list_display = ("title", "is_active", "order", "text_align", "created_at")
    list_filter = ("is_active", "text_align")
    search_fields = ("title", "subtitle")
    ordering = ("order", "-created_at")
