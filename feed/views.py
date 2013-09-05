import re
import requests
from lxml import etree
from django.http import HttpResponse
from django.shortcuts import render

def view_rss(request):
    rss_url = request.GET.get("url")
    if rss_url is not None:
        try:
            doc = etree.parse(rss_url)
        except IOError:
            resp = requests.get(rss_url)
            doc = etree.fromstring(resp.content)
        output = etree.tostring(doc, pretty_print=True)
        output = re.sub(r'([<?xml-stylesheet].+?\?>)', '', output)
        content_type = request.GET["ct"]
        return HttpResponse(output, content_type=content_type)
    else:
        return render(request, "feed/view_rss.html")
