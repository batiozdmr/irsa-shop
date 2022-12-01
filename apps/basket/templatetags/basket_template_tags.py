from django import template

from apps.product.models import Attributes

register = template.Library()


@register.simple_tag()
def multiply(qty, item_price, *args, **kwargs):
    # you would need to do any localization of the result here

    if type(qty) == int:
        sonuc = qty * item_price
    else:
        sonuc = ""

    return sonuc


@register.simple_tag()
def variant_option(pk):
    return Attributes.objects.get(pk=pk).text
