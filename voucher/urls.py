"""virginafrica URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from os import name
from django.contrib import admin
from django.urls import path
from voucher import views as voucher_views
from . import views as mainviews

from django.contrib.auth import views as auth_views

admin.site.site_header  =  "Virgin Safaris admin"  
admin.site.site_title  =  "Virgin Safaris admin site"
admin.site.index_title  =  "Virgin Safaris Admin"


from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns = [
 
   
        
        path("generatevoucher/", voucher_views.voucher_template, name="generate-voucher" ),
        path("view-voucher/<slug:slug>", voucher_views.view_voucher, name="view-voucher"),
        path("create-voucher/", voucher_views.create_voucher, name="create-voucher"),
        path("vouchers/", voucher_views.list_vouchers, name="list-vouchers" ),
         path('voucher-pdf/<slug:slug>',voucher_views.pdfview, name='view-pdf'),
         path('vouchers/edit-voucher/<slug:slug>',voucher_views.edit_voucher, name='edit-voucher'),


        

      
         

]


urlpatterns += staticfiles_urlpatterns()
