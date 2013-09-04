from lxml import etree
from django.db import models
from django.contrib.auth.models import User

class Feed(models.Model):
    name = models.CharField("Feed title", max_length=200)
    xml_url = models.URLField("URL")
    html_url = models.URLField("Homepage")
    category = models.ForeignKey("Category")
    owner = models.ForeignKey(User)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name

    def to_outline(self):
        """
        Return an <outline> element with this Feed's information.
        """
        return etree.Element("outline", text=self.name, title=self.name,
                             xmlUrl=self.xml_url, htmlUrl=self.html_url)

class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField()
    description = models.TextField(blank=True)
    owner = models.ForeignKey(User)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name
