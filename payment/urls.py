from django.urls import path
from .import views

urlpatterns = [
    path('home/',views.home,name='home'),
    path('payment_page/', views.payment_page, name='payment'),
    path('',views.index,name='index'),
    path('success/', views.success_page, name='success'),
    path('create-checkout-session/', views.create_checkout_session, name='create_checkout_session'),
]
