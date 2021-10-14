from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import InvoiceForm, ProductForm, ClientForm,ClientSelectForm
from django.contrib import messages
from invoice.models import Invoice,Product,Client


def main(request):
	return render(request, 'invoice/main.html')

def create_invoice(request):
	if request.method == 'POST':
		form = InvoiceForm(request.POST)
		if form.is_valid:
			form.save()
			messages.success(request, f'Invoice created successfully')
			return redirect('view-invoices')
	
	else:
		form = InvoiceForm()
	
	return render(request=request, template_name="invoice/create_invoice.html", context={"invoice_create_form":form})

@login_required 
def view_invoices(request):
	context = {}
	invoices = Invoice.objects.all()
	context['invoices'] = invoices

	return render(request, 'invoice/invoices.html', context)

@login_required 
def view_clients(request):
	context = {}
	clients = Client.objects.all()
	context['clients'] = clients

	return render(request, 'client/clients.html', context)

@login_required
def clients(request):
    context = {}
    clients = Client.objects.all()
    context['clients'] = clients

    if request.method == 'GET':
        form = ClientForm()
        context['form'] = form
        return render(request, 'client/create_client.html', context)

    if request.method == 'POST':
        form = ClientForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()

            messages.success(request, 'New Client Added')
            return redirect('clients')
        else:
            messages.error(request, 'Problem processing your request')
            return redirect('clients')


    return render(request, 'client/create_client.html', context)
def createBuildInvoice(request, slug):
	#fetch that invoice
	try:
		invoice = Invoice.objects.get(slug=slug)
		pass
	except:
		messages.error(request, 'Something went wrong')
		return redirect('invoices')

	#fetch all the products - related to this invoice
	products = Product.objects.filter(invoice=invoice)


	context = {}
	context['invoice'] = invoice
	context['products'] = products

	if request.method == 'GET':
		prod_form  = ProductForm()
		inv_form = InvoiceForm(instance=invoice)
		client_form = ClientSelectForm(initial_client=invoice.client)
		context['prod_form'] = prod_form
		context['inv_form'] = inv_form
		context['client_form'] = client_form
		return render(request, 'invoice/view_created_invoice.html', context)

	if request.method == 'POST':
		prod_form  = ProductForm(request.POST)
		inv_form = InvoiceForm(request.POST, instance=invoice)
		client_form = ClientSelectForm(request.POST, initial_client=invoice.client, instance=invoice)

		if prod_form.is_valid():
			obj = prod_form.save(commit=False)
			obj.invoice = invoice
			obj.save()

			messages.success(request, "Invoice product added succesfully")
			return redirect('create-build-invoice', slug=slug)
		elif inv_form.is_valid and 'paymentTerms' in request.POST:
			inv_form.save()

			messages.success(request, "Invoice updated succesfully")
			return redirect('create-build-invoice', slug=slug)
		elif client_form.is_valid() and 'client' in request.POST:

			client_form.save()
			messages.success(request, "Client added to invoice succesfully")
			return redirect('create-build-invoice', slug=slug)
		else:
			context['prod_form'] = prod_form
			context['inv_form'] = inv_form
			context['client_form'] = client_form
			messages.error(request,"Problem processing your request")
			return render(request, 'invoice/view_created_invoice.html', context)


	return render(request, 'invoice/view_created_invoice.html', context)

def viewPDFInvoice(request, slug):
	#fetch that invoice
	try:
		invoice = Invoice.objects.get(slug=slug)
		pass
	except:
		messages.error(request, 'Something went wrong')
		return redirect('invoices')

	#fetch all the products - related to this invoice
	#products = Product.objects.filter(invoice=invoice)

	#Get Client Settings
   

	#Calculate the Invoice Total
	invoiceCurrency = ''
	invoiceTotal = 0.0
	"""if len(products) > 0:
		for x in products:
			y = float(x.quantity) * float(x.price)
			invoiceTotal += y
			invoiceCurrency = x.currency
			"""



	"""context = {}
	context['invoice'] = invoice
	context['products'] = products
	context['invoiceTotal'] = "{:.2f}".format(invoiceTotal)
	context['invoiceCurrency'] = invoiceCurrency"""

	return render(request, 'invoice/invoice-template.html')

	#view invoices here
	
# Create your views here.
