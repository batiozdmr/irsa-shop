from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from apps.basket.basket import Basket
from apps.checkout.models import CouponCodeList
from apps.product.models import Product
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

def basket_add(request):
    basket = Basket(request)
    if request.POST.get("action") == "post":
        product_id = int(request.POST.get("productid"))
        # product_qty = int(request.POST.get("productqty"))
        product_qty = 1
        product = get_object_or_404(Product, id=product_id)
        basket.add(product=product, qty=product_qty)

        basketqty = basket.__len__()
        response = JsonResponse({"qty": basketqty})
        return response

@login_required
def coupon_code_add(request):
    if request.POST.get("coupon_code"):
        coupon_code_get = request.POST.get("coupon_code")
        coupon_code_list = CouponCodeList.objects.filter(code=coupon_code_get,status=True).last()
        if coupon_code_list:
            request.session['coupon_code_price'] = coupon_code_list.price
            request.session['coupon_code_id'] = coupon_code_list.id
            messages.success(request, _("Kupon başarıyla eklendi."))
        else:
            request.session['coupon_code_price'] = 0.00
            request.session['coupon_code_id'] = 1
            messages.success(request, _("Kupon kodu bulunamadı"))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def coupon_code_delete(request):
    request.session['coupon_code_price'] = 0.00
    request.session['coupon_code_id'] = 1
    messages.success(request, _("Kupon kodu kaldırıldı"))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def basket_view(request):
    basket = Basket(request)
    if basket.count()>0:
        return render(request, "checkout/view_cart.html", {"basket": basket})
    else:
        messages.warning(request, _("Sepet Boş"))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def basket_note_update(request):
    product_id = request.POST.get('product_id', False)
    product_note = request.POST.get('product_note', "")
    if product_id:
        basket = Basket(request)
        product = get_object_or_404(Product, id=product_id)
        basket.update_note(product=product, note=str(product_note))

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def basket_delete(request, str):
    basket = Basket(request)
    basket.delete(product=str)
    return redirect('/')
