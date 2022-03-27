from io import BytesIO
from multiprocessing import context
from django.http import HttpResponse
from django.template.loader import get_template
from django.shortcuts import get_object_or_404

from profiles.models import AudioFile

from xhtml2pdf import pisa


def render_to_pdf(template_source, context_dict={}):
    """
    Renders Booking Detail HTML Template to PDF Format

    Arguments:

    Template Source - "booking_detail_display_pdf.html"
    Context Dict - Booking object (alias "event")

    https://www.codingforentrepreneurs.com/
    blog/html-template-to-pdf-in-django/
    """

    template = get_template(template_source)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)

    if not pdf.err:
        return HttpResponse(
            result.getvalue(), content_type="application/pdf")
    else:
        return None
