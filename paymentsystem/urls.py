"""
URL configuration for paymentsystem project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.shortcuts import redirect
from payment.views import payment_page
from django.http import HttpResponse 

def index(request):
    return HttpResponse("hello world !")
def home(request):
    name = input('what is your name ?')
    return HttpResponse(f"this is my {name}")
def hello(request,name):
    return HttpResponse(f"hello ,{name}")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('payment/',include('payment.urls')),
    path('', lambda request: redirect('home')),
    path('<str:name>',hello),
    path('home/',home), 
]
