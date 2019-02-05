# -*- coding: utf-8 -*-
#whenever you change this file, run manage.py makemigrations and migrate
from __future__ import unicode_literals
from django.db import models
from django.template.defaultfilters import slugify

class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)
    views = models.IntegerField(default=0)
    slug = models.SlugField(unique=True, null=True)
    
    def save(self, *args, **kwargs):
        if self.id == None:
            self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Catergories"

class Page(models.Model):
    category = models.ForeignKey(Category)
    title = models.CharField(max_length=128)
    url = models.URLField(max_length=200)
    views = models.IntegerField(default=0)
    date = models.DateField()

    def __unicode__(self):
        return self.title