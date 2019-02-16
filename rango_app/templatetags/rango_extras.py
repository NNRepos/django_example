from django import template
from rango_app.models import Category

register = template.Library()

@register.inclusion_tag('rango/cats.html')
def get_category_list(curr_cat=None):
    return {'cats': Category.objects.all(), 'act_cat': curr_cat}