import base64
import hashlib
import hmac
import json
from decimal import Decimal

import requests
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
# Create your views here.
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render, HttpResponse
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_exempt

from apps.accounts.models import Address
from apps.basket.basket import Basket
from apps.checkout.models import CouponCodeList
from apps.order.models import Order, OrderProducts
from apps.product.models import Product, ShippingMethod


def add_to_cart(request):
    product_id = request.POST.get('product_id', None)
    product_quantity = request.POST.get('product_quantity', 1)
    product_attributes = request.POST.get('select_attributes', "")
    product_explanation = request.POST.get('product_explanation', "")

    if product_id and product_quantity:
        basket = Basket(request)
        product = get_object_or_404(Product, id=product_id)
        basket.add(product=product, qty=int(product_quantity), variant_option=product_attributes,
                   variant_explanation=product_explanation)
    else:
        messages.success(request, _("Beklenmedik Bir Hata Oluştu"))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    messages.success(request, _("Ürün Başarıyla Sepete Eklendi"))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def view_checkout(request):
    basket = Basket(request)
    if basket:
        user_obj = User.objects.get(id=request.user.id)
        billing_address_obj = Address.objects.filter(user=user_obj, billing_address=True).last()
        shipping_address_obj = Address.objects.filter(user=user_obj, shipping_address=True).last()

        basket = Basket(request)
        context = {"basket": basket, 'billing_address_obj': billing_address_obj,
                   'shipping_address_obj': shipping_address_obj}

        return render(request, 'checkout/view_checkout.html', context)
    else:
        return HttpResponseRedirect("https://www.teknofestmagaza.com")


def cart_count(request):
    cart = request.session.get('cart', {})
    cart_count = len(cart)
    return {'cart_count': cart_count}


def cart_delete(request, pk):
    """
    TODO: The function will be deleted
    :param request:
    :param pk:
    :return:
    """
    basket = Basket(request)
    basket.delete(product=pk)

    return HttpResponseRedirect(reverse('basket:basket_view'))


@login_required
def payment(request):
    Sonuc = 'Siparişiniz Başarılı Bir Şekilde Oluşturuldu'
    return render(request, 'checkout/payment_ok.html', {'Sonuc': Sonuc})
