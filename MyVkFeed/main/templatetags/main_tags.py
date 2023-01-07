# -*- coding: utf-8 -*-

from django import template
from django.db.models import QuerySet

from main.models import *
from django.db import connection

register = template.Library()


@register.simple_tag(name='getpostphotos')
def get_post_photos(post_obj: Post) -> QuerySet:
    return post_obj.photos.prefetch_related().all()


@register.simple_tag(name='countposts')
def count_posts(title: str) -> str:
    count = Post.objects.values('title').filter(title=title).count()
    return f'Постов: {count}'


@register.simple_tag(name='clearerrors')
def clear_filter_errors(context: dict):
    if 'errors' in context:
        context.pop(errors, None)
    else:
        context = None
