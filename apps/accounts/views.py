
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from allauth.account.views import SignupView, PasswordChangeView
from allauth.account.forms import LoginForm

from apps.accounts.forms import AddressForm, UserForm
from apps.accounts.models import Address, EmailPool
from django.contrib.auth.models import Group, User
from apps.order.models import Order
from apps.product.models import Category, ProductRequestList, ProductFavoriteList


class CustomSignupView(SignupView):
    # here we add some context to the already existing context
    def get_context_data(self, **kwargs):
        # we get context data from original view
        context = super(CustomSignupView,
                        self).get_context_data(**kwargs)
        context['login_form'] = LoginForm()  # add form to context
        return context


@login_required
def my_account(request):
    billing_address_obj = Address.objects.filter(user=request.user, billing_address=True).last()
    shipping_address_obj = Address.objects.filter(user=request.user, shipping_address=True).last()
    user_address_list=Address.objects.filter(user=request.user)
    product_request_list = ProductRequestList.objects.filter(user=request.user)
    product_favorite_list = ProductFavoriteList.objects.filter(user=request.user)
    categories = Category.objects.filter(level=0, )
    create_address_form = AddressForm()

    my_orders = Order.objects.filter(buyer=request.user).order_by('-id')

    addresses = Address.objects.filter(user=request.user)
    if request.method == 'POST':
        user_form = UserForm(request.POST or None, instance=request.user)

        if user_form.is_valid():
            user_form.save()
        else:
            messages.error(request, _('Kayıt formunu tekrar kontrol ediniz.'))
            return render(request, 'account/my_account.html',
                          {'user_detail': request.user, 'my_orders': my_orders, 'categories': categories, 'user_form': user_form,'addresses': addresses,
                           'product_request_list': product_request_list, 'product_favorite_list': product_favorite_list,
                           'create_address_form': create_address_form})

    else:

        user_form = UserForm(instance=request.user)
    return render(request, 'account/my_account.html',
                  {'user_detail': request.user,'my_orders': my_orders,'user_address_list': user_address_list, 'categories': categories, 'user_form': user_form,
                   'product_request_list': product_request_list, 'product_favorite_list': product_favorite_list,
                   'create_address_form': create_address_form, 'billing_address_obj': billing_address_obj,
                   'shipping_address_obj': shipping_address_obj})


@login_required
def my_account_detail(request):
    user_detail = get_object_or_404(User, pk=request.user.pk)
    user_details_2 = User.objects.get(pk=request.user.pk)

    return render(request, 'account/my_account.html', {'user_detail': user_detail})


@login_required
def update_address(request):
    user_detail = get_object_or_404(User, pk=request.user.pk)
    user_details_2 = User.objects.get(pk=request.user.pk)
    categories = Category.objects.filter(level=0, )

    return render(request, 'account/my_account.html', {'user_detail': user_detail, 'categories': categories})


@login_required
def my_orders(request):
    user_detail = get_object_or_404(User, pk=request.user.pk)

    my_orders = Order.objects.filter(buyer=user_detail)

    context = {'user_detail': user_detail, 'my_orders': my_orders}

    return render(request, 'account/my_orders.html', context)


@login_required
def view_address(request):
    addresses = Address.objects.filter(user=request.user)
    default_billing_address = Address.objects.filter(user=request.user, billing_address=True).first()
    default_shipping_address = Address.objects.filter(user=request.user, shipping_address=True).first()

    context = {'addresses': addresses, 'default_billing_address': default_billing_address,
               'default_shipping_address': default_shipping_address}
    return render(request, 'account/view_addresses.html', context)




@login_required
def add_address(request):
    if request.method == "POST":
        address_form = AddressForm(data=request.POST)
        if address_form.is_valid():
            address_form = address_form.save(commit=False)
            address_form.user = request.user
            address_form.save()
            messages.success(request, _('Kayıt Başarılı'))
            return HttpResponseRedirect(reverse("accounts/:my-account"))
        else:
            messages.warning(request, _('Kayıt formunu tekrar kontrol ediniz.'))
            return HttpResponseRedirect(reverse("accounts/:my-account"))

    else:
        address_form = AddressForm()
    return render(request, "account/edit_address.html", {"address_form": address_form})


@login_required
def edit_address(request, id):
    if request.method == "POST":
        address = Address.objects.get(pk=id, user=request.user)
        address_form = AddressForm(instance=address, data=request.POST)
        if address_form.is_valid():
            address_form.save()
            return HttpResponseRedirect(reverse("accounts/:my-account"))
    else:
        address = Address.objects.get(pk=id, user=request.user)
        address_form = AddressForm(instance=address)
    return render(request, "account/edit_address.html", {"address_form": address_form})


@login_required
def delete_address(request, id):
    Address.objects.filter(id=id, user=request.user).delete()
    return redirect("accounts/:view-address")

@login_required
def email_add_pool(request):
    email_get = request.POST.get('email')

    if email_get:
        p = EmailPool(text=email_get,)
        p.save()
        messages.success(request, _("Email Başarıyla Kaydedilmiştir."))

    else:

        messages.warning(request, _("Bir Sorun İle Karşılaşıldı."))

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
