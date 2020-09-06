from django import template
import datetime
from django.utils import formats

register = template.Library()

# @register.simple_tag(name='get_total_time')
# def get_total_time(start_time, end_time):
#     hours_count = ''
#     if start_time > end_time:
#         return
#     working_hour = (end_time - start_time)
#     return working_hour



@register.filter(expects_localtime=True, is_safe=False)
def custom_date(value, arg=None):
    if value in (None, ''):
        return ''

    if isinstance(value, str):
        api_date_format = '%Y-%m-%dT%H:%M:%S'
        value = datetime.datetime.strptime(value, api_date_format)

    try:
        return formats.date_format(value, arg)
    except AttributeError:
        try:
            return format(value, arg)
        except AttributeError:
            return ''