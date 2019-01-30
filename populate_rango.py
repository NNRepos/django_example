#the links are different from the ones in the site because I've updated them.
import os,datetime
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Rango.settings')

import django
django.setup()

from rango_app.models import Category, Page


def populate():
    python_cat = add_cat(name='Python', views=128)

    add_page(cat=python_cat,
        title="Official Python Tutorial",
        url="https://docs.python.org/2/tutorial/")

    add_page(cat=python_cat,
        title="How to Think like a Computer Scientist",
        url="https://greenteapress.com/wp/think-python/")

    add_page(cat=python_cat,
        title="Learn Python in 10 Minutes",
        url="https://www.stavros.io/tutorials/python/")

    django_cat = add_cat(name="Django", views=64)

    add_page(cat=django_cat,
        title="Official Django Tutorial",
        url="https://www.djangoproject.com/start/")

    add_page(cat=django_cat,
        title="Django Rocks",
        url="https://www.djangorocks.com/")

    add_page(cat=django_cat,
        title="How to Tango with Django",
        url="http://www.tangowithdjango.com/")

    frame_cat = add_cat(name="Other Frameworks", views=32)

    add_page(cat=frame_cat,
        title="Bottle",
        url="http://bottlepy.org/docs/dev/")

    add_page(cat=frame_cat,
        title="Flask",
        url="http://flask.pocoo.org")

    games_cat = add_cat(name="Games", views=16)
    
    add_page(cat=games_cat,
        title="Undertale",
        url="https://undertale.com/")
    
    add_page(cat=games_cat,
        title="Maple",
        url="http://maplestory.nexon.net/landing/")
    
    food_cat = add_cat(name="Food", views=8)
    
    add_page(cat=food_cat,
        title="Curry",
        url="https://www.google.com/search?q=chicken+with+curry+sauce&tbm=isch")
    
    add_page(cat=food_cat,
        title="Meatballs",
        url="https://www.google.com/search?q=meatballs&tbm=isch")
    
    empty_cat = add_cat(name="Empty")
    
    # Print out what we have added to the user.
    # for c in Category.objects.all():
        # for p in Page.objects.filter(category=c):
            # print "- {0} - {1}".format(str(c), str(p))

def add_page(cat, title, url, views=0, date=datetime.datetime.now()):
    p, created = Page.objects.get_or_create(category=cat, title=title, date=date)
    if not created:
        print "page",title,"already exists."
        return p
    p.url=url
    p.views=views
    p.date=date
    p.save()
    return p

def add_cat(name, views=0):
    c, created = Category.objects.get_or_create(name=name)
    if not created:
        print "category",name,"already exists."
        return c
    c.views=views
    c.save()
    return c

# Start execution here!
if __name__ == '__main__':
    print "Starting Rango population script..."
    populate()