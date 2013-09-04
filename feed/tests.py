from lxml import etree
import autofixture
from django.test import TestCase
from django.contrib.auth.models import User
from feed.models import Feed, Category

class TestFeedViews(TestCase):
    pass

class TestFeedModels(TestCase):
    def setUp(self):
        self.owner = autofixture.create_one(User)

    def test_feed_to_outline(self):
        feed = autofixture.create_one(Feed, generate_fk=True)
        element = etree.Element("outline", text=feed.name, title=feed.name,
                                xmlUrl=feed.xml_url, htmlUrl=feed.html_url, type="rss")
        self.assertXMLEqual(etree.tostring(feed.to_outline()), etree.tostring(element))

    def test_category_to_outline(self):
        category = autofixture.create_one(Category, field_values={
            "owner": self.owner,
            "name": "category",
        })
        feeds = autofixture.create(Feed, 10, field_values={
            "owner": self.owner,
            "category": category,
        })
        category_element = etree.Element("outline", text=category.name)
        for feed in Feed.objects.all():
            category_element.append(feed.to_outline())
        self.assertXMLEqual(etree.tostring(category.to_outline()), etree.tostring(category_element))

class TestFeedUtils(TestCase):
    pass
