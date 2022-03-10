from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def append_page_no_to_url_params(context, **kwargs):
    """
    Preserves current URL query parameters when 
    executing pagination of results in "Find a Dep" page.

    e.g. If current URL is "/find_a_dep?instrument=Vocals"

    and link is: 
    <a href={% url "find_a_dep" % }{% append_page_no_to_url_params page=3 %}></a>

    the returned URL will append "&page=2" to the end of the current URL,
    instead of replacing/forgetting about the already existing queries, resulting in:

    "/find_a_dep?instrument=Vocals&page=2"

    Referenced from:
    https://www.caktusgroup.com/blog/2018/10/18/filtering-and-pagination-django/
    """
    data = context["request"].GET.copy()

    for key, value in kwargs.items():
        data[key] = value

    for key in [key for key, value in data.items() if not value]:
        del data[key]
    return data.urlencode()