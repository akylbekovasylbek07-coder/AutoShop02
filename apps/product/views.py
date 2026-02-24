from django.views.generic import TemplateView, ListView
from apps.product.models import Category, Product 
from apps.blog.models import Post
from apps.partners.models import Partners


class HomeView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(
            is_active=True, parent__isnull=True
        )[:6]
        context['products'] = Product.objects.filter(
            is_available=True, 
            category__is_active=True 
        )[:8]
        context['partners'] = Partners.objects.all()
        return context
    


class CategoryListView(ListView):
    model = Category
    template_name = 'product/category_list.html'
    context_object_name = 'categories'

    def get_queryset(self):
        return Category.objects.filter(is_active=True, parent__isnull=True)    
