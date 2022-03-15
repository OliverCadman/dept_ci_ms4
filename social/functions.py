from django.utils.http import urlencode
from django.urls import reverse


def reverse_querystring(view, urlconf=None, args=None, kwargs=None, current_app=None, query_kwargs=None):
    '''Custom reverse to handle query strings.
    Usage:
        reverse('app.views.my_view', kwargs={'pk': 123}, query_kwargs={'search': 'Bob'})
    '''
    base_url = reverse(view, urlconf=urlconf, args=args, kwargs=kwargs, current_app=current_app)
    if query_kwargs:
        return '{}?{}'.format(base_url, urlencode(query_kwargs))
    return base_url

def get_referral_path(request, split_index1, split_index2, slice_index1, slice_index2):
    referer_url = request.META.get("HTTP_REFERER")
    referer_path = "".join(referer_url.split("/")[5])
    referer_path = "".join(referer_path.split("&")[1])

    return referer_path