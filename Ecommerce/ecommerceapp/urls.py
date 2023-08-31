from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('contacts', views.contact, name="contact"),
    path('profile',views.profile,name="profile"),
    path('about', views.about, name="about"),
    path('handlerequest/',views.handlerequest,name="handlerequest"),
    path('checkout',views.checkout.as_view(),name="checkout"),
]
