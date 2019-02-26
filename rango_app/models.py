# -*- coding: utf-8 -*-
#whenever you change this file, run manage.py makemigrations and migrate
from __future__ import unicode_literals

from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

from datetime import datetime

class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)
    views = models.IntegerField(default=0)
    slug = models.SlugField(unique=True, null=True)
    
    def save(self, *args, **kwargs):
        if self.id == None:
            self.slug = slugify(self.name)
        if self.views < 0:
            self.views = 0
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
    
    def save(self, *args, **kwargs):
        if self.date == None:
            self.date = datetime.now()
        super(Page, self).save(*args, **kwargs)
    
    def __unicode__(self):
        return self.title

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    website = models.URLField(blank=True, null=True)
    avatar = models.ImageField(upload_to='profile_images', blank=True)
    birth_date = models.DateField(blank=True)
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('trap', 'Trap'),
        ('wizard', 'Wizard')
    )
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    
    def __unicode__(self):
        return self.user.username