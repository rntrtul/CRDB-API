import logging
import platform
import time

from django import template

logger = logging.getLogger(__name__)
register = template.Library()


@register.simple_tag
def format_time(to_format):
    if platform.system() == 'Linux':
        return time.strftime("%-H:%M:%S", time.gmtime(to_format))
    else:
        return time.strftime("%#H:%M:%S", time.gmtime(to_format))


@register.simple_tag
def format_duration(start, end):
    start = format_time(start)
    end = format_time(end)
    duration = start + " - " + end
    return duration


@register.filter('startswith')
def startswith(text, starts):
    if isinstance(text, str):
        return text.startswith(starts)
    return False
