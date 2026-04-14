from django.views.generic import FormView
from django.urls import reverse_lazy
from apps.contact.forms import ContactForm
from apps.contact.models import ContactPage


class ContactView(FormView):
    template_name = 'pages/contact.html'
    form_class = ContactForm    
    success_url = reverse_lazy('contact')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Ачкыч сөздү HTMLдегидей кылып 'contactPage' деп өзгөртүңүз
        context['contactPage'] = ContactPage.objects.order_by('-id').first()
        return context
