from django.contrib import admin

from .models import Product,InvoiceProduct,Invoice, Client

# Register your models here.


admin.site.register(Product)
admin.site.register(Client)
admin.site.register(Invoice)
admin.site.register(InvoiceProduct)
