from django.urls import path

from apps.main.views import *
app_name = "content/"

urlpatterns = [

    path('kvkk/', kvkk_page, name="kvkk-detail"),
    path('getsepet/', getsepet, name="getsepet"),


]