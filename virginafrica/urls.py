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
from django.contrib import admin
from django.urls import path
from accounts import views
from invoice import views as invoice_views
from . import views as mainviews

from django.contrib.auth import views as auth_views

admin.site.site_header  =  "Virgin Safaris admin"  
admin.site.site_title  =  "Virgin Safaris admin site"
admin.site.index_title  =  "Virgin Safaris Admin"
urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
   
        path("userlogin/", views.login_request, name="login"),
        path("", mainviews.home, name="homepage"),

        path('logout/', auth_views.LogoutView.as_view(template_name = 'forms/logoutpage.html'), name='logout'),
        path("invoicemain/", invoice_views.main, name="invoice-main"),
        path("createinvoice/", invoice_views.create_invoice, name="create-invoice"),
        path("invoices/", invoice_views.view_invoices, name="view-invoices" ),
        path('invoices/create-build/<slug:slug>',invoice_views.createBuildInvoice, name='create-build-invoice'),

        #Invoice documents pdf and email
        path('invoices/view-pdf/<slug:slug>',invoice_views.viewPDFInvoice, name='view-pdf-invoice'),
        #path('invoices/view-document/<slug:slug>',views.viewDocumentInvoice, name='view-document-invoice'),
       
       #path('invoices/email-document/<slug:slug>',views.emailDocumentInvoice, name='email-document-invoice'),


        path('clients/',invoice_views.view_clients, name='clients'),
        path('create-client/',invoice_views.clients, name='create-client'),
        

        url(r'^generate/pdf/$', invoice_views.generate_pdf, name='generate-pdf'),

         

]
