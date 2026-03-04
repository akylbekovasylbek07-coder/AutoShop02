from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from django.views.generic import TemplateView

from apps.abuot.forms import SliderForm
from apps.abuot.models import Slider


@staff_member_required
def slider_manage(request):
    if request.method == "POST":
        form = SliderForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("slider_manage")
    else:
        form = SliderForm()

    sliders = Slider.objects.all().order_by("order", "-created_at")
    return render(
        request,
        "abuot/slider_manage.html",
        {
            "form": form,
            "sliders": sliders,
        },
    )


@staff_member_required
@require_POST
def slider_delete(request, pk):
    slider = get_object_or_404(Slider, pk=pk)
    slider.delete()
    return redirect("slider_manage")





class AboutView(TemplateView):
    template_name = "pages/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
