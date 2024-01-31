from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter() 
def date_format(value):
    date = value
    print(date)
    return data

@register.filter() 
def para(description):
    text = ''
    for i in description.split('\n'):
        text += ('<p class="description">' + i + '</p>')
    return mark_safe(text)



register.filter('para', para)