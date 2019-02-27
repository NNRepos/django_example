# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.template.defaultfilters import slugify

from datetime import datetime

from rango_app.models import Category,Page,UserProfile
from rango_app.forms import CategoryForm,PageForm,UserForm,UserProfileForm

# from Rango.settings import MEDIA_URL removed because I used context_processor instead

def go2index(request):
    return redirect('/rango/')


def index(request):
    category_list = Category.objects.order_by('-views')[:5]
    context_dict = {'boldmessage': "You better believe it",
                    'categories':category_list}
    #cookies part
    # request.session.set_test_cookie()
    cookies = request.session #get session cookies as dictionary - use request.COOKIES for client-side cookies
    visits = int(cookies.get('visits', '1')) #Actually hourly visits
    #real last visit part
    if 'last_visit' in cookies:
        last_visit = cookies['last_visit']
        context_dict['last_visit'] = datetime.strptime(last_visit[:-7], "%Y-%m-%d %H:%M:%S")
    else:
        context_dict['last_visit'] = 'never!'
    #hourly last visit part
    reset_last_visit_time = False #reset hourly visit time
    if 'last_hourly_visit' in cookies:
        last_hourly_visit = cookies['last_hourly_visit']
        last_hourly_visit_time = datetime.strptime(last_hourly_visit[:-7], "%Y-%m-%d %H:%M:%S")
        if (datetime.now() - last_hourly_visit_time).seconds > 3600:
            visits = visits + 1
            reset_last_visit_time = True
    else:
        reset_last_visit_time = True
    context_dict['visits'] = visits
    #updating cookies part
    if reset_last_visit_time: #we use str() because that's what request.session can handle. for lists and such, import pickle
        request.session['last_hourly_visit'] = str(datetime.now()) #set last hourly visit
        request.session['visits'] = visits #set number of hourly visits
    request.session['last_visit'] = str(datetime.now()) #set real last visit
    return render(request, 'rango/index.html', context_dict)


def about(request):
    return render(request, 'rango/about.html')


def category(request, category_name_slug):
    context_dict = {}
    try:
        category = Category.objects.get(slug=category_name_slug)
        pages = Page.objects.filter(category=category).order_by('-views')
        context_dict['category_name'] = category.name
        context_dict['category_name_short'] = category.name.split(' ')[0]
        context_dict['category_name_slug'] = category.slug
        context_dict['category'] = category
        context_dict['pages'] = pages
        context_dict['method'] = request.method
        if request.method == 'GET':
            category.views+=1
            category.save()
        elif request.method == 'POST':
            search_query = request.POST.get('search_query')
            context_dict['search'] = search_query
            results = Page.objects.filter(category__slug=category.slug).filter(title__icontains=search_query)
            context_dict['results'] = results
    except Category.DoesNotExist:
        pass
    return render(request, 'rango/category.html', context_dict)

@login_required
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            newslug = slugify(form.cleaned_data['name'])
            print Category.objects.filter(slug=newslug)
            if not Category.objects.filter(slug=newslug).exists():
                form.save(commit=True)
                return redirect('/rango/')
            else:
                messages.info(request,'Category with similar name already exists')
        else:
            print form.errors
    else:
        form = CategoryForm()
    return render(request, 'rango/add_category.html', {'form': form})

@login_required
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
                page.date = datetime.now()
                page.save()
                return redirect('/rango/')
        else:
            print form.errors
    else:
        form = PageForm()
    context_dict = {'form':form, 'category': cat}
    return render(request, 'rango/add_page.html', context_dict)


#unused - redux
def register(request):
    # if request.session.test_cookie_worked():
        # print ">>>> TEST COOKIE WORKED!"
        # request.session.delete_test_cookie()
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            if 'avatar' in request.FILES:
                profile.avatar = request.FILES['avatar']
            profile.save()
            registered = True
        else:
            print user_form.errors, profile_form.errors
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    return render(request,
        'rango/register.html',
        {'user_form': user_form, 'profile_form': profile_form, 'registered': registered} )


#unused - redux
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return redirect('/rango/')
            else:
                return HttpResponse("Your Rango account is disabled.")
        else:
            print "Invalid login details: {0}, {1}".format(username, password)
            messages.error(request,'username or password incorrect')
            return redirect('/rango/login')
    else:
        return render(request, 'rango/login.html', {})


#unused - redux
@login_required
def user_logout(request):
    logout(request)
    return redirect('/rango/')


def search(request):
    context_dict = {}
    if request.method == 'POST':
        search_query = request.POST.get('search_query')
        cats = Category.objects.filter(name__icontains=search_query)
        pages = Page.objects.filter(title__icontains=search_query)
        context_dict = {'cats':cats, 'pages':pages, 'search':search_query}
    context_dict['method'] = request.method
    return render(request, 'rango/search.html', context_dict)


def track_url(request):
    try:
        if request.method == 'GET':
            if 'page_id' in request.GET:
                page_id = request.GET['page_id']
                page = Page.objects.get(pk=page_id)
                page.views+=1
                page.save()
                return redirect(page.url)
            else: #illegal page_id
                return redirect('/rango/')
        else: #not GET
            return redirect('/rango/')
    except Page.DoesNotExist: #wrong page_id
        return redirect('/rango/')


@login_required
def register_profile(request):
    registered = False
    if request.method == 'POST':
        user = User.objects.get(username=request.user)
        profile_form = UserProfileForm(data=request.POST)
        if profile_form.is_valid():
            profile = UserProfile.objects.filter(user=user)
            if profile.exists(): #update existing UserProfile
                profile = profile.get()
                profile.website = profile_form.cleaned_data['website']
                profile.birth_date = profile_form.cleaned_data['birth_date']
                profile.gender = profile_form.cleaned_data['gender']
            else: #create new UserProfile
                profile = profile_form.save(commit=False)
                profile.user = user
            if 'avatar' in request.FILES:
                profile.avatar = request.FILES['avatar']
            #TODO: else: profile.avatar = None, do this when the registration already loads the old settings
            profile.save()
            registered = True
        else:
            print profile_form.errors
    else:
        profile_form = UserProfileForm()
    return render(request,
        'rango/profile_registration.html',
        {'profile_form': profile_form, 'registered': registered} )


#TODO maybe add option to see other ppl's profiles
@login_required
def profile(request):
    user = User.objects.get(username=request.user)
    profile = UserProfile.objects.get(user=user)
    context_dict = {'user':user, 'profile':profile}
    return render (request, 'rango/profile.html', context_dict)


#fuction for suggest_category
def get_category_list(max_results=0, starts_with=''):
    cat_list = []
    if starts_with:
        cat_list = Category.objects.filter(name__istartswith=starts_with)
        if cat_list and max_results > 0 and cat_list.count() > max_results:
            cat_list = cat_list[:max_results]
    return cat_list


def suggest_category(request):
    cat_list = []
    max_res, starts_with = 8, ''
    if request.method == 'GET':
        starts_with = request.GET['suggestion']
    cat_list = get_category_list(max_res, starts_with)
    return render(request, 'rango/cats.html', {'cats': cat_list })