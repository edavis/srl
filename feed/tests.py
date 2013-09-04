import autofixture
from lxml import etree
from pathlib import Path

from django.test import TestCase
from django.contrib.auth.models import User

from feed.models import Feed, Category
from feed.utils import add_from_opml

class TestFeedViews(TestCase):
    pass

class TestFeedModels(TestCase):
    def setUp(self):
        self.owner = autofixture.create_one(User)

    def elements_equal(self, e1, e2):
        self.assertXMLEqual(
            etree.tostring(e1), etree.tostring(e2))

    def test_feed_to_outline(self):
        feed = autofixture.create_one(Feed, generate_fk=True)
        element = etree.Element("outline", text=feed.name, title=feed.name,
                                xmlUrl=feed.xml_url, htmlUrl=feed.html_url, type="rss")
        self.elements_equal(feed.to_outline(), element)

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
        self.elements_equal(category.to_outline(), category_element)

class TestFeedUtils(TestCase):
    def setUp(self):
        self.test_data = Path(__file__).parent()["test_data"]
        self.owner = autofixture.create_one(User)

    def test_add_from_opml(self):
        category = autofixture.create_one(Category)
        nyt = str(self.test_data["nyt.opml"])
        with open(nyt) as fp:
            add_from_opml(fp, category, self.owner)
        self.assertEqual(category.feed_set.count(), 101)

        feed = Feed.objects.get(xml_url="http://www.nytimes.com/services/xml/rss/nyt/pop_top.xml")
        self.assertEqual(feed.name, "NYT > Most E-mailed Articles")
        self.assertEqual(feed.html_url, "http://www.nytimes.com/gst/mostemailed.html?partner=rssnyt")
