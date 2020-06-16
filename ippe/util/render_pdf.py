# encoding: utf-8
import io
from django.http import HttpResponse
from django.template.loader import get_template

from xhtml2pdf import pisa

def render_pdf(url_template,context={}):
    template = get_template(url_template)
    html = template.render(context)
    result = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type="application/pdf")
    return None