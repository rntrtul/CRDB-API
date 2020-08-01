from django import template
import time
import logging
logger = logging.getLogger(__name__)
register = template.Library()

@register.simple_tag
def format_time(toFormat):
  return time.strftime("%-H:%M:%S", time.gmtime(toFormat))

@register.simple_tag
def format_duration(start, end):
  start = format_time(start)
  end = format_time(end)
  durration = start + " - " + end
  return durration

@register.filter('startswith')
def startswith(text, starts):
    if isinstance(text, str):
        return text.startswith(starts)
    return False