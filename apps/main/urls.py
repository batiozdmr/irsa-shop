from django.urls import path

from apps.main import views
app_name = "content/"

urlpatterns = [

    path('kvkk/', views.kvkk_page, name="kvkk-detail"),


]