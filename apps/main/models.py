from ckeditor.fields import RichTextField
from django.contrib.sites.models import Site
from django.db import models
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _


from apps.common.mixins.audit import AuditMixin
from apps.common.oneTextField.oneField import OneTextField


# Create your models here.

class SiteSettings(AuditMixin):
    site = models.OneToOneField(Site, related_name="settings", verbose_name=_('Firma'), on_delete=models.CASCADE)
    header_text = models.CharField(max_length=400, verbose_name=_('Firma Adı'), blank=True)
    header_sort_text = models.CharField(max_length=400, verbose_name=_('Başlık Metin'), blank=True)
    description = models.TextField(null=True, verbose_name=_('Firma Açıklaması'), blank=True)
    tag = models.TextField(null=True, verbose_name=_('Head Tag'), blank=True)
    footer_text = models.TextField(null=True, verbose_name=_('Footer Metni'), blank=True)
    company_logo = models.FileField(upload_to='images/contents/', null=True, verbose_name=_('Firma Logosu'),
                                       blank=True)
    company_logo_footer = models.FileField(upload_to='images/contents/', null=True,
                                              verbose_name=_('Firma Logosu Footer'),
                                              blank=True)
    keywords = models.TextField(null=True, verbose_name=_('Etiketler'), blank=True)
    bank_logo = models.FileField(upload_to='images/contents/', null=True,
                                    verbose_name=_('Banka Logosu'),
                                    blank=True)
    bank_name = models.TextField(null=True, verbose_name=_('Banka Adı'), blank=True)
    bank_iban = models.TextField(null=True, verbose_name=_('IBAN'), blank=True)
    bank_account_name = models.TextField(null=True, verbose_name=_('Hesap Unvanı'), blank=True)
    bank_info_message = models.TextField(null=True, verbose_name=_('Ödeme Uyarı Metni'), blank=True)
    phone = models.CharField(max_length=200, blank=True, verbose_name=_('Telefon'))
    address = models.CharField(max_length=200, blank=True, verbose_name=_('Adres'))
    email = models.EmailField(blank=True, verbose_name=_('E-Posta'))

    company_about = RichTextField(blank=True, verbose_name="Hakkımızda")
    company_legal = RichTextField(blank=True, verbose_name="Gizlilik Politikası")
    company_faq = RichTextField(blank=True, verbose_name="Sıkça Sorulan Sorular")
    company_contact = RichTextField(blank=True, verbose_name="İletişim")
    company_legal_2 = RichTextField(blank=True, verbose_name="Teslimat ve İade")
    company_legal_3 = RichTextField(blank=True, verbose_name="Mesafeli Satış Sözleşmesi")
    company_legal_4 = RichTextField(blank=True, verbose_name="Kullanım Koşullarımız")

    kvkk = RichTextField(blank=True, verbose_name="Kişisel Verileri Koruma Kanunu (KVKK)")

    footer_banner = models.FileField(upload_to='images/contents/', null=True, verbose_name=_('Footer Banner'),
                                        blank=True)

    @property
    def image_url(self):
        if self.company_logo and hasattr(self.company_logo, 'url'):
            return self.company_logo.url

    @property
    def keywords_list(self):
        my_string = self.keywords
        keywords_list = [x.strip() for x in my_string.split(',')]
        return keywords_list

    def __str__(self) -> str:
        return self.header_text

    def save(self, *args, **kwargs):
        self.slug = slugify(self.header_text)
        super(SiteSettings, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _('Site Ayarları')
        verbose_name_plural = _('Site Ayarları Listesi')
        default_permissions = ()
        permissions = ((_('liste'), _('Listeleme Yetkisi')),
                       (_('sil'), _('Silme Yetkisi')),
                       (_('ekle'), _('Ekleme Yetkisi')),
                       (_('guncelle'), _('Güncelleme Yetkisi')))
