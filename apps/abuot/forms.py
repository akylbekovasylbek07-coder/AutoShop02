from django import forms

from apps.abuot.models import Slider


class SliderForm(forms.ModelForm):
    class Meta:
        model = Slider
        fields = [
            "title",
            "subtitle",
            "description",
            "button_text",
            "button_link",
            "image",
            "is_active",
            "order",
            "text_align",
        ]
