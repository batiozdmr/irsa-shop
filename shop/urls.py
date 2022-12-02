from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

admin.site.site_header = 'IRSA Mağaza Yönetimi'
admin.site.index_title = 'IRSA Mağaza Yönetimi'
admin.site.site_title = 'IRSA Mağaza Yönetim Paneli'

from apps.main.views import main, about_page, privacy_page, faq_page, legal_2_page, legal_3_page, \
    maintenance, legal_4_page
from shop import settings
from django.utils.translation import gettext_lazy as _
from django.conf.urls.i18n import i18n_patterns

urlpatterns = i18n_patterns(

    path('super/user/admin/', admin.site.urls),
    path(_('account/'), include("allauth.urls")),
    path(_('accounts/'), include("apps.accounts.urls")),
    path('', main, name='mainPage'),
    path(_('product/'), include("apps.product.urls")),
    path(_('content/'), include("apps.main.urls")),
    path(_('checkout/'), include("apps.checkout.urls")),

    path(_('about/'), about_page, name='about-page'),
    path(_('privacy/'), privacy_page, name='privacy-page'),
    path(_('usage-agreement/'), legal_4_page, name='legal_4_page'),
    path(_('faq/'), faq_page, name='faq-page'),
    path(_('legal2/'), legal_2_page, name='legal-2-page'),
    path(_('legal3/'), legal_3_page, name='leagel-3-page'),
    path(_('basket/'), include("apps.basket.urls")),

    path(_('rosetta/'), include("rosetta.urls")),
    path('ckeditor/', include('ckeditor_uploader.urls')),

) + static(settings.STATIC_URL, document_root=settings.STATIC_URL) + static(settings.MEDIA_URL,
                                                                            document_root=settings.MEDIA_ROOT)
