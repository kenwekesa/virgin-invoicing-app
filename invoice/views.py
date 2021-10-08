from django.shortcuts import render, redirect
from .forms import InvoiceForm


def main(request):
    return render(request, 'invoice/main.html')

def create_invoice(request):
	form = InvoiceForm()
	return render(request=request, template_name="invoice/create_invoice.html", context={"invoice_create_form":form})
   

# Create your views here.
