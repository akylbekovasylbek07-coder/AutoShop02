from django import forms
from apps.contact.models import ContactRequest


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactRequest
        fields = ['name', 'email', 'subject', 'message']
        