# custom_filters.py
from django import template
import random

register = template.Library()

@register.filter(name='random_range')
def random_range(value):
    return random.randint(1, value)
