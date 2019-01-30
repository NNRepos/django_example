# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import render
from rango_app.models import Category, Page

def index(request):
    category_list = Category.objects.order_by('-views')[:5]
    context_dict = {'boldmessage': "You better believe it",
                    'categories':category_list}
    return render(request, 'rango/index.html', context_dict)


def about(request):
    return render(request, 'rango/about.html')


def category(request, category_name_slug):
    context_dict = {}
    try:
        category = Category.objects.get(slug=category_name_slug)
        pages = Page.objects.filter(category=category)
        context_dict['category_name'] = category.name
        context_dict['category_name_short'] = category.name.split(' ')[0]
        context_dict['category'] = category
        context_dict['pages'] = pages
    except Category.DoesNotExist:
        pass
    return render(request, 'rango/category.html', context_dict)