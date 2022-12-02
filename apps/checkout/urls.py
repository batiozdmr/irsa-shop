from django.urls import path

from apps.checkout import views

app_name = "checkout/"

urlpatterns = [

    path('add-to-cart/', views.add_to_cart, name="add-to-cart"),
    path('', views.view_checkout, name="checkout"),
    path('payment/', views.payment, name='payment'),

]
