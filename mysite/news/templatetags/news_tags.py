from django import template
from django.db.models import Count, Q
from django.core.cache import cache

from news.models import Category

register = template.Library()


@register.simple_tag()
def get_categories():
    return Category.objects.all()


@register.inclusion_tag('news/list_categories.html')
def show_list_categories(current_cat=False):
    categories = Category.objects.annotate(news_count=Count('news', filter=Q(news__is_published=True))).filter(news_count__gt=0)
    # categories = cache.get('categories')
    # if not categories:
    #     categories = Category.objects.annotate(news_count=Count('news', filter=Q(news__is_published=True))).filter(news_count__gt=0)
    #     cache.set('categories', tuple(categories), 30)
    return {'categories': categories, 'current_cat': current_cat}
