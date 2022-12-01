from django.urls import path
from . import views

app_name = 'basket'

urlpatterns = [
    path('', views.basket_view, name='basket_view'),
    path('add/', views.basket_add, name='basket_add'),
    path('delete/<str:str>', views.basket_delete, name='basket_delete'),
    # path('update/', views.basket_update, name='basket_update'),
    path('update/note/', views.basket_note_update, name='basket_note_update'),
    path('coupon/add/', views.coupon_code_add, name='coupon_code'),
    path('coupon/delete/', views.coupon_code_delete, name='coupon_code_delete'),

]
