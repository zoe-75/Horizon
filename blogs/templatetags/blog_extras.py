# blog/templatetags/blog_extras.py
from django import template
from django.utils.timezone import now, localtime

register = template.Library()

@register.filter
def smart_timesince(value):
    """Smart time display: 'just now', '5 minutes ago', '3 hours ago', or '9 November at 1:29 am'."""
    if not value:
        return ""

    delta = now() - value
    total_seconds = int(delta.total_seconds())

    if total_seconds < 60:
        return "just now"
    elif total_seconds < 3600:
        minutes = total_seconds // 60
        return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
    elif total_seconds < 86400:
        hours = total_seconds // 3600
        return f"{hours} hour{'s' if hours != 1 else ''} ago"
    else:
        local_time = localtime(value)
        return local_time.strftime('%d %B at %I:%M %p').lstrip("0").replace(" 0", " ").lower()

