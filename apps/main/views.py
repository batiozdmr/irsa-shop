from django.contrib.auth.models import User
from django.shortcuts import render

from apps.accounts.models import Address
from apps.basket.basket import Basket
from apps.main.models import SiteSettings
from apps.product.models import Product, ShippingMethod, Category


def main(request):
    products = Product.objects.filter(active=True).order_by('-id')
    return render(request, "index.html", {'products': products})


def maintenance(request):
    return render(request, "maintenance.html")


def getsepet(request):
    basket = Basket(request)
    context = {"basket": basket}
    return render(request, "apps/sepet/sepetheader.html", context)


def site_social_links(request):
    if not "coupon_code_price" in request.session:
        request.session['coupon_code_price'] = 0.00
        request.session['coupon_code_id'] = 1
    return {'site_social_links': site_social_links}


def site_settings(request):
    site_settings = SiteSettings.objects.all().first()
    shipping_methods = ShippingMethod.objects.filter(is_active=True).last()
    return {'site_settings': site_settings, 'shipping_methods': shipping_methods}


def categories_menu_list(request):
    categories_menu_list = Category.objects.filter(level=0, )

    return {'categories_menu_list': categories_menu_list}


def view_cart(request):
    pro_list = []
    cart_total_price = 0

    cart = request.session.get('cart', {})

    for key, value in cart.items():

        product = Product.objects.filter(id=key).first()
        if product and value:
            product_total_price = float(product.price) * float(value)
            cart_total_price += product_total_price
            pro_cart = {"product": product, "product_quantity": value, "product_total_price": product_total_price}
            pro_list.append(pro_cart)
        else:
            pass
    if request.session.get('coupon_code', {}):
        cart_total_price = cart_total_price - float(request.session.get('coupon_code', {}))
    else:
        cart_total_price = cart_total_price
    return {"cart_product_list": pro_list, "cart_total_price": cart_total_price}


def about_page(request):
    site_settings = SiteSettings.objects.first()
    bread_crumb = "Hakk??m??zda"
    context = {"content": site_settings.company_about, "bread_crumb": bread_crumb}
    return render(request, "apps/content/hakkimizda.html", context)


def privacy_page(request):
    site_settings = SiteSettings.objects.first()
    bread_crumb = "Gizlilik Politikas??"

    context = {"content": site_settings.company_legal, "bread_crumb": bread_crumb}
    return render(request, "apps/content/html_content.html", context)


def faq_page(request):
    site_settings = SiteSettings.objects.first()
    bread_crumb = "Yard??m ve S.S.S"

    context = {"content": site_settings.company_faq, "bread_crumb": bread_crumb}
    return render(request, "apps/content/html_content.html", context)


def legal_2_page(request):
    site_settings = SiteSettings.objects.first()
    bread_crumb = "Teslimat ve ??ade"

    context = {"content": site_settings.company_legal_2, "bread_crumb": bread_crumb}
    return render(request, "apps/content/html_content.html", context)


def legal_3_page(request):
    site_settings = SiteSettings.objects.first()
    bread_crumb = "Mesafeli Sat???? S??zle??mesi"

    context = {"content": site_settings.company_legal_3, "bread_crumb": bread_crumb}
    return render(request, "apps/content/html_content.html", context)


def legal_4_page(request):
    site_settings = SiteSettings.objects.first()
    bread_crumb = "Kullan??m Ko??ullar??m??z"

    context = {"content": site_settings.company_legal_4, "bread_crumb": bread_crumb}
    return render(request, "apps/content/html_content.html", context)


def kvkk_page(request):
    site_settings = SiteSettings.objects.first()
    bread_crumb = "Ki??isel Verilerin Korunmas?? Kanunu"

    context = {"content": site_settings.kvkk, "bread_crumb": bread_crumb}
    return render(request, "apps/content/html_content.html", context)
