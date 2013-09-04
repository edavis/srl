from lxml import etree
from feed.models import Feed, Category

def add_from_opml(source, category, owner):
    """
    Parse an OPML file and create a Feed object for each subscription.
    """
    doc = etree.parse(source)
    outlines = doc.iterfind(".//outline[@xmlUrl]")
    for outline in outlines:
        kwargs = {
            "name": outline.get("text"),
            "xml_url": outline.get("xmlUrl"),
            "html_url": outline.get("htmlUrl"),
            "category": category,
            "owner": owner,
        }
        Feed.objects.get_or_create(**kwargs)
