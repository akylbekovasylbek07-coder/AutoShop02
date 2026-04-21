from django.views.generic import TemplateView

from apps.partners.models import Partners


class PartnersPageView(TemplateView):
    template_name = 'pages/partners.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['partners'] = Partners.objects.all()
        return context
