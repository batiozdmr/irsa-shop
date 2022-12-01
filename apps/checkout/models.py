from django.contrib.auth.models import Group, User
from apps.common.mixins import AuditMixin
from django.db import models

from apps.product.models import Product, OrderStatus
from django.utils.translation import ugettext_lazy as _
import uuid
from django.utils.crypto import get_random_string
from django.db.models.signals import m2m_changed
from django.db.models.signals import post_save
from django.dispatch import receiver



class CouponCodeCreate(AuditMixin):
    name = models.CharField(max_length=400, verbose_name=_('Kupon Liste Adı'))
    count = models.IntegerField(null=True, blank=True, verbose_name=_('Kupon Adet'))
    price = models.IntegerField(null=True, blank=True, verbose_name=_('Ücret'))

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        super(CouponCodeCreate, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _('Kupon')
        verbose_name_plural = _('Kupon Kod Oluştur')
        default_permissions = ()
        permissions = ((_('liste'), _('Listeleme Yetkisi')),
                       (_('sil'), _('Silme Yetkisi')),
                       (_('ekle'), _('Ekleme Yetkisi')),
                       (_('guncelle'), _('Güncelleme Yetkisi')))

@receiver(post_save, sender=CouponCodeCreate)
def CreateCouponCode(sender, instance, **kwargs):
    couponController = CouponCodeList.objects.filter(coupon_create=instance)
    if couponController:
        pass
    else:
        if instance.count == None:
            pass
        else:
            for i in range(instance.count):
                create_new_code=get_random_string(length=16)
                p = CouponCodeList(coupon_create_id=instance.id, price=instance.price, code=create_new_code)
                p.save()

class CouponCodeList(AuditMixin):
    coupon_create = models.ForeignKey(CouponCodeCreate, related_name="list", null=True, blank=True, on_delete=models.CASCADE,
                                     verbose_name=_('Kupon Listesi'))
    code = models.CharField(max_length=100,null=True, blank=True, verbose_name=_('Kupon Kodu'))
    price = models.IntegerField(null=True, blank=True, verbose_name=_('Ücret'))
    status = models.BooleanField(null=True, blank=True, default=True, verbose_name=_('Aktif'))

    def __str__(self) -> str:
        return self.code

    def save(self, *args, **kwargs):
        super(CouponCodeList, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _('Kupon Kodları')
        verbose_name_plural = _('Kupon Kodları Listesi')
        default_permissions = ()
        permissions = ((_('liste'), _('Listeleme Yetkisi')),
                       (_('sil'), _('Silme Yetkisi')),
                       (_('ekle'), _('Ekleme Yetkisi')),
                       (_('guncelle'), _('Güncelleme Yetkisi')))
