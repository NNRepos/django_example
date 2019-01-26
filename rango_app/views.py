# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    return HttpResponse("hello world! <br/> <a href='/rango/about'>About</a>")

def about(request):
    return HttpResponse("<p>rango_app is an app which does whatver tangoWithDjango" + 
                        " says it does.\r\n Now go away~~~</p>") #\n doesn't work