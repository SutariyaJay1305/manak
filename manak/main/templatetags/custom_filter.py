from django import template

register = template.Library()

@register.filter() 
def date_format(value):
    date = value
    print(date)
    return data

# register.filter('update_variable', update_variable)