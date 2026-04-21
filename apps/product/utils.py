from apps.product.models import Wislist



def get_wislist(request):
    if request.user.is_authenticated:
        wislist, _ = Wislist.objects.get_or_create(user=request.user)
    else:
        if not request.session.session_key:
            request.session.create()
        wislist, _ = Wislist.objects.get_or_create(
            session_key = request.session.session_key
        )    
    return wislist    
