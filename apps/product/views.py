from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.db.models import Count, F, Q
from django.utils.translation import gettext_lazy as _

# Create your views here.

from apps.product.models import Product, Category, ProductComment, ProductRequestList, ProductFavoriteList


def product_detail(request, slug):
    product_detail = get_object_or_404(Product, slug=slug, active=True)

    return render(request, 'product/product.html',{"product_detail": product_detail})


def product_category_list(request, slug):
    category = get_object_or_404(Category, slug=slug)
    if category.level == 0:
        categories_sub_list = Category.objects.filter(parent__slug=slug)
        if categories_sub_list:
            product_list = Product.objects.filter(category__in=categories_sub_list, active=True)
        else:
            categories_sub = Category.objects.filter(slug=slug)
            product_list = Product.objects.filter(category__in=categories_sub, active=True)

        return render(request, 'product/product_sub_category_list.html',
                      {"product_list": product_list, 'categories_sub_list': categories_sub_list, 'category': category})
    else:
        product_list = Product.objects.filter(category__slug=slug, active=True)
        return render(request, 'product/product_category_list.html',
                      {"product_list": product_list, 'category': category})


def product_search(request):
    search_query = request.GET.get('q')
    if search_query:
        product_list = Product.objects.filter(Q(name__icontains=search_query) |
                                              Q(description__icontains=search_query) |
                                              Q(product_type_select__name__icontains=search_query) |
                                              Q(category__name__icontains=search_query)
                                              ).distinct().order_by('-id')
    else:
        product_list = Product.objects.filter(active=True).order_by('-id')

    return render(request, 'product/product_search.html', {"product_list": product_list})


@login_required
def product_add_comment(request):
    comment_user = request.user
    comment_product = request.POST.get('product_id')
    comment_title = request.POST.get('comment_title')
    comment_comment = request.POST.get('comment')
    if comment_user and comment_product and comment_title and comment_comment:
        p = ProductComment(product_id=comment_product, user=comment_user, title=comment_title, comment=comment_comment)
        p.save()
        messages.success(request, _("Kayıt Başarılı"))

    else:

        messages.warning(request, _("Kayıt Başarısız"))

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def product_add_request_list(request):
    comment_user = request.user
    comment_product = request.POST.get('product_id')
    check = ProductRequestList.objects.filter(product_id=comment_product, user=comment_user).first()
    if check:
        messages.warning(request, _("Ürün İstek Listenizde Mevcut"))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    if comment_user and comment_product:
        p = ProductRequestList(product_id=comment_product, user=comment_user, )
        p.save()
        messages.success(request, _("Ürün İstek Listesine Başarıyla Eklenmiştir."))

    else:

        messages.warning(request, _("Bir Sorun İle Karşılaşıldı."))

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def product_add_favorite_list(request):
    comment_user = request.user
    comment_product = request.POST.get('product_id')
    check = ProductFavoriteList.objects.filter(product_id=comment_product, user=comment_user)
    if check:
        messages.warning(request, _("Ürün Favori Listenizde Mevcut"))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    if comment_user and comment_product:
        p = ProductFavoriteList(product_id=comment_product, user=comment_user, )
        p.save()
        messages.success(request, _("Ürün Favori Listesine Başarıyla Eklenmiştir."))

    else:

        messages.warning(request, _("Bir Sorun İle Karşılaşıldı."))

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
