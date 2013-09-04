from lxml import etree
import autofixture
from django.test import TestCase
from feed.models import Feed, Category

class TestFeedViews(TestCase):
    pass

class TestFeedModels(TestCase):
    def test_feed_to_outline(self):
        feed = autofixture.create_one(Feed, generate_fk=True)
        element = etree.Element("outline", text=feed.name, title=feed.name,
                                xmlUrl=feed.xml_url, htmlUrl=feed.html_url, type="rss")
        self.assertXMLEqual(etree.tostring(feed.to_outline()), etree.tostring(element))

class TestFeedUtils(TestCase):
    pass
