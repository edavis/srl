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

class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField()
    description = models.TextField(blank=True)
    owner = models.ForeignKey(User)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name
