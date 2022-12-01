import uuid as uuid
from django.db import models
from ckeditor.fields import RichTextField

# Create your models here.
from apps.accounts.models import Address
from django.contrib.auth.models import Group, User
from apps.common.mixins import AuditMixin

from apps.product.models import Product, OrderStatus, Attributes, CargoCompany
from apps.checkout.models import CouponCodeList
from django.utils.translation import ugettext_lazy as _
import uuid
from apps.common.utils.generate_key import generate_key


class Order(AuditMixin):
    buyer = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name=_('Sipariş Sahibi'))
    order_id = models.CharField(blank=True, max_length=50, editable=False, unique=True, verbose_name=_('Sipariş No'))
    cargo_company = models.ForeignKey(to=CargoCompany, null=True, blank=True, on_delete=models.PROTECT,
                                      verbose_name=_('Kargo Firması'))
    cargo_no = models.CharField(blank=True, max_length=200, null=True, verbose_name=_('Kargo Takip No'))
    payment_status = models.BooleanField(null=True, default=False, verbose_name=_('Ödeme Durumu'))
    status = models.ForeignKey(to=OrderStatus, null=True, blank=True, on_delete=models.PROTECT,
                               verbose_name=_('Sipariş Durumu'))
    payment_amount = models.DecimalField(null=True, blank=True, max_digits=19, decimal_places=2,
                                         verbose_name=_("Toplam Ödeme"))
    coupon_code = models.ForeignKey(to=CouponCodeList, on_delete=models.CASCADE, null=True, blank=True,
                                    related_name="CouponCodeList",
                                    verbose_name=_('Kupon Kodu'))
    billing_address_text = RichTextField(blank=True, null=True, verbose_name=_('Fatura Adresi'))
    shipping_address_text = RichTextField(blank=True, null=True, verbose_name=_('Teslimat Adresi'))
    return_bank = models.TextField(blank=True, null=True, verbose_name=_('Banka Geri Dönüşü'))

    def __str__(self):
        return str(self.id)

    def orderProductList(self):
        list = OrderProducts.objects.filter(order_id=self.id)
        return list

    def ad_soyad(self):
        user_info = User.objects.get(id=self.buyer.id)
        return user_info.get_full_name()

    def save(self, *args, **kwargs):
        self.order_id = generate_key(9, 9, useupper=True)
        super(Order, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _('Sipariş')
        verbose_name_plural = _('Sipariş Listesi')
        default_permissions = ()
        permissions = ((_('liste'), _('Listeleme Yetkisi')),
                       (_('sil'), _('Silme Yetkisi')),
                       (_('ekle'), _('Ekleme Yetkisi')),
                       (_('guncelle'), _('Güncelleme Yetkisi')))


class OrderProducts(AuditMixin):
    order = models.ForeignKey(to=Order, on_delete=models.CASCADE, related_name="items", verbose_name=_('Sipariş'))
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE, verbose_name=_('Ürün'))
    price = models.DecimalField(verbose_name=_("Fiyat"), max_digits=19, decimal_places=2)
    quantity = models.PositiveIntegerField(verbose_name=_('Miktar'), default=1)
    explanation = models.CharField(blank=True, max_length=50, default="", verbose_name=_('Sipariş Açıklaması'))

    option = models.ForeignKey(to=Attributes, on_delete=models.CASCADE, null=True, blank=True, related_name="options",
                               verbose_name=_('Ürün Seçenek'))

    def __str__(self):
        return f"{self.product.name} | ${self.product.price * self.quantity}"

    class Meta:
        verbose_name = _('Sipariş Ürünü')
        verbose_name_plural = _('Sipariş Ürünleri')
        default_permissions = ()
        permissions = ((_('liste'), _('Listeleme Yetkisi')),
                       (_('sil'), _('Silme Yetkisi')),
                       (_('ekle'), _('Ekleme Yetkisi')),
                       (_('guncelle'), _('Güncelleme Yetkisi')))
