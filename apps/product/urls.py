from django.urls import path

from apps.product import views
app_name = "product/"

urlpatterns = [

    path('detail/<slug:slug>', views.product_detail, name="product-detail"),
    path('category/<slug:slug>', views.product_category_list, name="product-category-list"),
    path('search/', views.product_search, name="product-search"),
    path('add/comment/', views.product_add_comment, name="product-add-comment"),
    path('add/request/list/', views.product_add_request_list, name="add-to-request-list"),
    path('add/favorite/list/', views.product_add_favorite_list, name="add-to-favorite-list"),

]