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

# API Entegrasyon Bilgileri - Mağaza paneline giriş yaparak BİLGİ sayfasından alabilirsiniz.
merchant_id = '297637'
merchant_ok_url = 'https://teknofestmagaza.com/tr/checkout/success/'
merchant_fail_url = 'https://teknofestmagaza.com/tr/checkout/fail/'
timeout_limit = '30'
debug_on = '0'
test_mode = '0'
no_installment = '1'
max_installment = '0'
currency = 'TL'


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
    basket = Basket(request)
    if not basket.count() > 0:
        messages.warning(request, _("Sepet Boş"))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    billing_address_obj = Address.objects.filter(user=request.user, billing_address=True).last()
    shipping_address_obj = Address.objects.filter(user=request.user, shipping_address=True).last()
    basket = Basket(request)
    order_obj = Order.objects.create(buyer_id=request.user.id, status_id=2, coupon_code_id=1,
                                     billing_address_text=billing_address_obj.summary,
                                     shipping_address_text=shipping_address_obj.summary)

    PRIVATE_IPS_PREFIX = ('10.', '172.', '192.',)

    def get_client_ip(request):
        """get the client ip from the request
        """
        remote_address = request.META.get('REMOTE_ADDR')
        # set the default value of the ip to be the REMOTE_ADDR if available
        # else None
        ip = remote_address
        # try to get the first non-proxy ip (not a private ip) from the
        # HTTP_X_FORWARDED_FOR
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            proxies = x_forwarded_for.split(',')
            # remove the private ips from the beginning
            while (len(proxies) > 0 and
                   proxies[0].startswith(PRIVATE_IPS_PREFIX)):
                proxies.pop(0)
            # take the first ip which is not a private one (of a proxy)
            if len(proxies) > 0:
                ip = proxies[0]
        return ip

    basket = Basket(request)
    for item in basket:
        product = item["product"]
        price = item["product"].price
        quantity = item["qty"]

        if item["variant_option"] != "":
            option = item["variant_option"]
        else:
            option = None
        if item["variant_explanation"] != "":
            option_explanation = item["variant_explanation"]
        else:
            option_explanation = ""
        order_item_obj = OrderProducts.objects.create(order=order_obj, product=product, price=price, quantity=quantity,
                                                      option_id=option, explanation=option_explanation)
    order_obj.payment_amount = basket.get_total_price()
    oid = order_obj.id
    order_obj.save()

    shipping_methods = ShippingMethod.objects.filter(is_active=True).last()
    last_amount = order_obj.payment_amount - Decimal(shipping_methods.fee)
    offer_type = 1
    if offer_type == 1:
        if last_amount > 1000:
            last_amount = order_obj.payment_amount - Decimal(shipping_methods.fee)
        else:
            last_amount = order_obj.payment_amount

    email = request.user.email
    payment_amount = str(int(last_amount) * 100)
    merchant_oid = str(oid)
    user_name = str(shipping_address_obj.first_name) + " " + str(shipping_address_obj.last_name)
    user_address = str(shipping_address_obj.summary)
    user_phone = str(shipping_address_obj.phone)
    user_basket_list = []
    for item in basket:
        product_list = []
        product_name = str(item["product"])
        product_list.append(product_name)
        product_list.append(int(item["price"]))
        product_list.append(item["qty"])
        user_basket_list += [product_list]

    if basket.get_total_price() <= 0:
        p = Order.objects.get(id=oid)
        or_id = p.id
        cash_coupon_code = p.coupon_code.id
        p.status_id = 35
        p.payment_status = True
        p.save()
        op = OrderProducts.objects.filter(order_id=or_id)
        for pro in op:
            get_pro = Product.objects.get(id=pro.product.id)
            get_pro.stock = get_pro.stock - pro.quantity
            get_pro.save()
        cash_coupon_code_list = CouponCodeList.objects.get(id=cash_coupon_code)
        cash_coupon_code_list.status = False
        cash_coupon_code_list.save()
        basket.clear()

    user_basket = base64.b64encode(json.dumps(user_basket_list).encode())
    ip_address = get_client_ip(request)  # ip adresini okuyor
    user_ip = str(ip_address)
    merchant_key = b'dh4nLR7ehMKZZ4i2'
    merchant_salt = b'yW3MPWohcMWaUjEE'
    hash_str = merchant_id + user_ip + merchant_oid + email + payment_amount + user_basket.decode() + no_installment + max_installment + currency + test_mode
    paytr_token = base64.b64encode(hmac.new(merchant_key, hash_str.encode() + merchant_salt, hashlib.sha256).digest())

    params = {
        'merchant_id': merchant_id,
        'user_ip': user_ip,
        'merchant_oid': merchant_oid,
        'email': email,
        'payment_amount': payment_amount,
        'paytr_token': paytr_token,
        'user_basket': user_basket,
        'debug_on': debug_on,
        'no_installment': no_installment,
        'max_installment': max_installment,
        'user_name': user_name,
        'user_address': user_address,
        'user_phone': user_phone,
        'merchant_ok_url': merchant_ok_url,
        'merchant_fail_url': merchant_fail_url,
        'timeout_limit': timeout_limit,
        'currency': currency,
        'test_mode': test_mode
    }
    result = requests.post('https://www.paytr.com/odeme/api/get-token', params)
    res = json.loads(result.text)

    if res['status'] == 'success':
        print(res['token'])
        basket.clear()
        context = {
            'token': res['token'],
            'hash': paytr_token
        }
        return render(request, 'checkout/payment.html', context)
    else:
        print(result.text)
        context = {
            'token': "Beklenmedik Bir Hata Oluştu."
        }
        return render(request, 'checkout/payment_fail.html', context)


@csrf_exempt
def callback(request):
    if request.method != 'POST':
        return HttpResponse(str('Post Gelmedi'))
    post = request.POST
    merchant_key = b'dh4nLR7ehMKZZ4i2'
    merchant_salt = 'yW3MPWohcMWaUjEE'
    hash_str = post['merchant_oid'] + merchant_salt + post['status'] + post['total_amount']
    hash = base64.b64encode(hmac.new(merchant_key, hash_str.encode(), hashlib.sha256).digest()).decode()
    if hash != post['hash']:
        return HttpResponse(str('PAYTR notification failed: bad hash'))
    if post['status'] == 'success':  # Ödeme Onaylandı
        order_obj = Order.objects.filter(id=int(post['merchant_oid'])).update(
            status_id=1,
            payment_status=True
        )
        print(request)
    else:  # Ödemeye Onay Verilmedi
        order_obj = Order.objects.filter(id=int(post['merchant_oid'])).update(
            status_id=67,
            payment_status=False
        )
        print(request)
    return HttpResponse(str('OK'))


@login_required
def success(request):
    Sonuc = 'Siparişiniz Başarılı Bir Şekilde Oluşturuldu'
    return render(request, 'checkout/payment_ok.html', {'Sonuc': Sonuc})


@login_required
def fail(request):
    Sonuc = 'Beklenmedik bir hata oluştu lütfen daha sonra tekrar deneyiniz.'
    return render(request, 'checkout/payment_fail.html', {'Sonuc': Sonuc})
