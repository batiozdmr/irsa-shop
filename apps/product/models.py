import datetime
from django.utils.translation import gettext_lazy as _
from django.template.defaultfilters import slugify
from django.utils.safestring import mark_safe
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVectorField
from django.db import models
from decimal import Decimal
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.core.validators import MinValueValidator
from django.db.models import TextField
# from django.utils.encoding import smart_text
from mptt.managers import TreeManager
from mptt.models import MPTTModel


from django.contrib.auth.models import Group, User
from apps.common.fileUpload.userPath import userDirectoryPath
from apps.common.models import SeoModel, SortableModel
from django.urls import reverse

from django.db import models


from apps.common.mixins import AuditMixin
from apps.common.oneTextField import OneTextField
from django.utils.translation import gettext_lazy as _


class Attributes(OneTextField):
    default_value = models.CharField(max_length=256, blank=True, verbose_name=_('Standart Seçenek'))
    total = models.IntegerField(blank=True, null=True, verbose_name=_('Adet'))

    def __str__(self) -> str:
        return self.text

    def getPro(self):
        list_get=[i.name for i in Product.objects.filter(attributes=self)]

        return list_get
    class Meta:
        verbose_name = _('Bedenler')
        verbose_name_plural = _('Bedenler')
        default_permissions = ()
        permissions = ((_('liste'), _('Listeleme Yetkisi')),
                       (_('sil'), _('Silme Yetkisi')),
                       (_('ekle'), _('Ekleme Yetkisi')),
                       (_('guncelle'), _('Güncelleme Yetkisi')))


class ShippingMethod(AuditMixin):
    name = models.CharField(max_length=256, blank=True, verbose_name=_('İsim'))
    fee = models.DecimalField(max_digits=19, decimal_places=2, verbose_name=_("Ücret"))
    description = models.TextField(blank=True, default="", verbose_name=_('Açıklama'))
    is_active = models.BooleanField(default=True, verbose_name=_('Kayıt Aktif'))

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = _('Teslimat Seçenekleri')
        verbose_name_plural = _('Teslimat Seçenekleri Listesi')
        default_permissions = ()
        permissions = ((_('liste'), _('Listeleme Yetkisi')),
                       (_('sil'), _('Silme Yetkisi')),
                       (_('ekle'), _('Ekleme Yetkisi')),
                       (_('guncelle'), _('Güncelleme Yetkisi')))


class Category(MPTTModel, SeoModel):
    parent = models.ForeignKey("self", null=True, blank=True, related_name="children", on_delete=models.CASCADE,
                               verbose_name=_('Üst Kategori'))
    name = models.CharField(max_length=250, verbose_name=_('Başlık'))
    description_plaintext = TextField(blank=True, default="", verbose_name=_('Tanım'))

    class_tag = models.CharField(max_length=128, blank=True, null=True, verbose_name=_('İcon Tag'))
    objects = models.Manager()
    tree = TreeManager()
    slug = models.SlugField(max_length=1000, unique=True, editable=False)

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _('Kategoriler')
        verbose_name_plural = _('Kategoriler Liste')
        default_permissions = ()
        permissions = ((_('liste'), _('Listeleme Yetkisi')),
                       (_('sil'), _('Silme Yetkisi')),
                       (_('ekle'), _('Ekleme Yetkisi')),
                       (_('guncelle'), _('Güncelleme Yetkisi')))

    def get_absolute_url(self):
        return reverse('product/:product-category-list', args=[str(self.slug)])


class ProductType(models.Model):
    name = models.CharField(max_length=250, verbose_name=_('Ürün Tip Adı'))
    slug = models.SlugField(max_length=1000, unique=True, editable=False)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(ProductType, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = _('Ürün Tipi')
        verbose_name_plural = _('Ürün Tipi Liste')
        default_permissions = ()
        permissions = ((_('liste'), _('Listeleme Yetkisi')),
                       (_('sil'), _('Silme Yetkisi')),
                       (_('ekle'), _('Ekleme Yetkisi')),
                       (_('guncelle'), _('Güncelleme Yetkisi')))


class Product(SeoModel):
    product_type_select = models.ForeignKey(ProductType, related_name="products_type", null=True, blank=True,
                                            on_delete=models.CASCADE, verbose_name=_('Ürün Seçenek Tipi'))
    name = models.CharField(max_length=1000, verbose_name=_('Ürün Adı'))
    description = RichTextUploadingField(blank=True, verbose_name=_('Açıklama'))
    features = RichTextField(blank=True, verbose_name=_('Özellikler'))
    summary = models.TextField(max_length=700, blank=True, verbose_name=_('Ürün Özet'))
    category = models.ForeignKey(Category, related_name="products_category", null=True, on_delete=models.SET_NULL,
                                 verbose_name=_('Kategori'))
    slug = models.SlugField(max_length=1000, unique=True, editable=False)
    price = models.DecimalField(verbose_name=_("Fiyat"), help_text=_("Minimum 0.01"), max_digits=19, decimal_places=2,
                                validators=[MinValueValidator(Decimal('0.01'))], )
    best_product = models.BooleanField(default=False, verbose_name=_("En iyi ürünler"), )
    best_selling_product = models.BooleanField(default=False, verbose_name=_("En çok satan ürünler"), )
    latest_product = models.BooleanField(default=True, verbose_name=_("En son ürünler"), )
    images = models.ManyToManyField(to="ProductImage", verbose_name=_("Ürün Görselleri"))
    attributes = models.ManyToManyField(to="Attributes", blank=True, verbose_name=_("Ürün Bedenleri"))
    stock = models.IntegerField(default=1, blank=True, verbose_name=_("Ürün Stoğu"))
    active = models.BooleanField(default=True, verbose_name=_("Aktif"), )

    # is_active = models.BooleanField(default=True, verbose_name=_('Kayıt Aktif'))

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)

    def get_url(self):
        return '/product/detail/' + self.slug

    class Meta:
        verbose_name = _('Ürünler')
        verbose_name_plural = _('Ürünler Liste')
        default_permissions = ()
        permissions = ((_('liste'), _('Listeleme Yetkisi')),
                       (_('sil'), _('Silme Yetkisi')),
                       (_('ekle'), _('Ekleme Yetkisi')),
                       (_('guncelle'), _('Güncelleme Yetkisi')))

    def __str__(self) -> str:
        return self.name

    def get_first_image(self):
        images = list(self.images.all())
        return images[0] if images else None

    def get_absolute_url(self):
        return reverse('product/:product-detail', args=[str(self.slug)])


class ProductImage(OneTextField):
    alt = models.CharField(max_length=128, blank=True)
    image = models.ImageField(upload_to=userDirectoryPath, null=True, blank=True, verbose_name=_('Görsel'))

    @property
    def image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url

    class Meta:
        verbose_name = _('Ürün Resimleri')
        verbose_name_plural = _('Ürün Resimleri Liste')
        default_permissions = ()
        permissions = ((_('liste'), _('Listeleme Yetkisi')),
                       (_('sil'), _('Silme Yetkisi')),
                       (_('ekle'), _('Ekleme Yetkisi')),
                       (_('guncelle'), _('Güncelleme Yetkisi')))


class OrderStatus(AuditMixin):
    name = models.CharField(max_length=256, blank=True, verbose_name=_('İsim'))

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = _('Sipariş Durum')
        verbose_name_plural = _('Sipariş Durum Listesi')
        default_permissions = ()
        permissions = ((_('liste'), _('Listeleme Yetkisi')),
                       (_('sil'), _('Silme Yetkisi')),
                       (_('ekle'), _('Ekleme Yetkisi')),
                       (_('guncelle'), _('Güncelleme Yetkisi')))


class CargoCompany(OneTextField):
    cargo_link = models.CharField(max_length=500, blank=True, verbose_name=_('Link'))

    class Meta:
        verbose_name = _('Kargo Firması')
        verbose_name_plural = _('Kargo Firması Listesi')
        default_permissions = ()
        permissions = ((_('liste'), _('Listeleme Yetkisi')),
                       (_('sil'), _('Silme Yetkisi')),
                       (_('ekle'), _('Ekleme Yetkisi')),
                       (_('guncelle'), _('Güncelleme Yetkisi')))


class ProductComment(AuditMixin):
    product = models.ForeignKey(Product, related_name="comment_products", null=True, blank=True,
                                on_delete=models.CASCADE, verbose_name=_('Ürün'))
    user = models.ForeignKey(User, related_name="comment_user", null=True, blank=True,
                             on_delete=models.CASCADE, verbose_name=_('Kişi'))
    title = models.CharField(max_length=500, blank=True, verbose_name=_('Başlık'))
    comment = models.TextField(blank=True, null=True, verbose_name=_('Yorum'))

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = _('Ürün Yorumları')
        verbose_name_plural = _('Ürün Yorumları Listesi')
        default_permissions = ()
        permissions = ((_('liste'), _('Listeleme Yetkisi')),
                       (_('sil'), _('Silme Yetkisi')),
                       (_('ekle'), _('Ekleme Yetkisi')),
                       (_('guncelle'), _('Güncelleme Yetkisi')))


class ProductRequestList(AuditMixin):
    product = models.ForeignKey(Product, related_name="request_products", null=True, blank=True,
                                on_delete=models.CASCADE, verbose_name=_('Ürün'))
    user = models.ForeignKey(User, related_name="request_user", null=True, blank=True,
                             on_delete=models.CASCADE, verbose_name=_('Kişi'))

    def __str__(self) -> str:
        return self.product.name

    class Meta:
        verbose_name = _('Ürün İstek')
        verbose_name_plural = _('Ürün İstek Listesi')
        default_permissions = ()
        permissions = ((_('liste'), _('Listeleme Yetkisi')),
                       (_('sil'), _('Silme Yetkisi')),
                       (_('ekle'), _('Ekleme Yetkisi')),
                       (_('guncelle'), _('Güncelleme Yetkisi')))


class ProductFavoriteList(AuditMixin):
    product = models.ForeignKey(Product, related_name="favorite_products", null=True, blank=True,
                                on_delete=models.CASCADE, verbose_name=_('Ürün'))
    user = models.ForeignKey(User, related_name="favorite_user", null=True, blank=True,
                             on_delete=models.CASCADE, verbose_name=_('Kişi'))

    def __str__(self) -> str:
        return self.product.name

    class Meta:
        verbose_name = _('Ürün Favorileri')
        verbose_name_plural = _('Ürün Favori Listesi')
        default_permissions = ()
        permissions = ((_('liste'), _('Listeleme Yetkisi')),
                       (_('sil'), _('Silme Yetkisi')),
                       (_('ekle'), _('Ekleme Yetkisi')),
                       (_('guncelle'), _('Güncelleme Yetkisi')))
