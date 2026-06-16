import jdatetime

from django import template


register = template.Library()


@register.filter
def to_jalali(value):

    if not value:
        return ''

    return jdatetime.date.fromgregorian(
        date=value,
    ).strftime(
        '%Y/%m/%d'
    )
