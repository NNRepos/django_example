# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.core.urlresolvers import reverse

from rango_app.models import Page,Category

from datetime import datetime
#tests
class CategoryMethodTests(TestCase):
    def test_ensure_views_are_positive(self):
        """
            ensure_views_are_positive should results True for categories where views are zero or positive
        """
        cat = Category(name='test',views=-1)
        cat.save()
        self.assertEqual((cat.views >= 0), True)

    def test_slug_line_creation(self):
        """
        slug_line_creation checks to make sure that when we add a category an appropriate slug line is created
        i.e. "Random Category String" -> "random-category-string"
        """
        cat = Category(name='Random Category String')
        cat.save()
        self.assertEqual(cat.slug, 'random-category-string')


class IndexViewTests(TestCase):
    def test_index_view_with_no_categories(self):
        """
        If no cats exist, an appropriate message should be displayed.
        """
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "There are currently no categories; I must have deleted them ;/")
        self.assertQuerysetEqual(response.context['categories'], [])

    def test_index_view_with_categories(self):
        """
        If no cats exist, an appropriate message should be displayed.
        """
        add_cat('test',1)
        add_cat('temp',1)
        add_cat('tmp',1)
        add_cat('tmp test temp',1)
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "tmp test temp")
        num_cats = len(response.context['categories'])
        self.assertEqual(num_cats , 4)


class PageTests(TestCase):
    def test_page_date_integrity(self):
        """
        Test whether the date the page was created on is after the current date
        """
        c = add_cat('test_cat',1)
        p=add_page(c, 'test_page', "http://someniceurl.com")
        page_time = p.date
        now = datetime.now()
        self.assertGreaterEqual(now, page_time)


#helpers
def add_cat(name, views):
    c = Category.objects.get_or_create(name=name)[0]
    c.views = views
    c.save()
    return c

def add_page(category, title, url):
    p = Page.objects.get_or_create(category=category, title=title, url=url)[0]
    p.save()
    return p