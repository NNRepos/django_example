# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import render,redirect
from rango_app.models import Category, Page
from rango_app.forms import CategoryForm,PageForm
import datetime

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
        context_dict['category_name_slug'] = category.slug
        context_dict['category'] = category
        context_dict['pages'] = pages
    except Category.DoesNotExist:
        pass
    return render(request, 'rango/category.html', context_dict)


def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
    
        if form.is_valid():
            form.save(commit=True)
            return redirect('/rango/')
        else:
            print form.errors
    else:
        form = CategoryForm()
    return render(request, 'rango/add_category.html', {'form': form})


def add_page(request, category_name_slug):
    try:
        cat = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        cat = None
    
    if request.method == 'POST':
        form = PageForm(request.POST)
        
        if form.is_valid():
            if cat:
                page = form.save(commit=False)
                page.category = cat
                page.views = 0
                page.date = datetime.datetime.now()
                page.save()
                return redirect('/rango/')
        else:
            print form.errors
    else:
        form = PageForm()
    context_dict = {'form':form, 'category': category_name_slug}
    return render(request, 'rango/add_page.html', context_dict)