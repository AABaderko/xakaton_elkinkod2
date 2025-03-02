from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.simple_tag
def get_date_msg(datetime):
    return datetime.strftime('%H:%M')