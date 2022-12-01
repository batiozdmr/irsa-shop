from django.urls import path

from . import views
from django.utils.translation import gettext_lazy as _

app_name = "accounts/"

urlpatterns = [

    path('', views.my_account, name="my-account"),
    path('my-orders', views.my_orders, name="my-orders"),
    path('addresses', views.view_address, name="view-address"),
    path('add_address', views.add_address, name="add-address"),
    path('address/edit/<int:id>/', views.edit_address, name="edit-address"),
    path('address/delete/<int:id>/', views.delete_address, name="delete-address"),
    path('emaill/add/pool/', views.email_add_pool, name="email-add-pool"),

    # path('myaddresses/delete/<int:id>', views.adresSil, name="adresSil"),

]
