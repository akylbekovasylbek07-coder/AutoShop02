from django.views.generic import TemplateView

from apps.blog.models import Post


class BlogPageView(TemplateView):
    template_name = 'pages/blog.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.all().order_by('-created_at')[:12]
        return context
