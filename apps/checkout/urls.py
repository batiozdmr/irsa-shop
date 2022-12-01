from django.urls import path

from apps.checkout import views

app_name = "checkout/"

urlpatterns = [

    path('add-to-cart/', views.add_to_cart, name="add-to-cart"),
    path('', views.view_checkout, name="checkout"),
    path('payment/', views.payment, name='payment'),
    path('callback/', views.callback, name='callback'),
    path('success/', views.success, name='success'),
    path('fail/', views.fail, name='failure'),


]
