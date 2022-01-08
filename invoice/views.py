from re import template
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls.base import reverse, reverse_lazy
from django.views.generic import TemplateView
import json
from django.http import HttpResponse, JsonResponse
from django.conf import settings

from django.forms.formsets import formset_factory

import weasyprint

from virginafrica.functions import emailInvoiceClient



#from virginafrica.invoice.models import Settings
from .forms import InvoiceForm, InvoiceProductForm, ProductEditFormSet, ProductForm, ClientForm,ClientSelectForm, ProductFormSet
from django.contrib import messages
from invoice.models import Invoice,Product,Client,InvoiceProduct

from django.core.files.storage import FileSystemStorage

from weasyprint import HTML
import os




def main(request):
	return render(request, 'invoice/main.html')

@login_required
def create_invoice(request):
	slug=''
	if request.method == 'POST':
		slug = ''
		form = InvoiceForm(request.POST)
		client_form = ClientForm(request.POST)
		product_form = ProductForm()
		product_formset = ProductFormSet(request.POST)
		invoice_product_form = InvoiceProductForm()
		if form.is_valid() and client_form.is_valid() and product_formset.is_valid():
			client=client_form.save()
			inv_prod = invoice_product_form.save(commit=False)
			
			
			#quantity = inv_prod.quantity
			form = form.save(commit=False)
			form.client = client
			
			
			#for inv_prod in invoice_product_form:
			form.save()
			client.save()
			slug=form.slug
			
			for f in product_formset: 
				cd = f.cleaned_data
				quantity = cd.get('quantity')
				description = cd.get('prod_description')
				price = cd.get('price')
				product= cd.get('product')
				invoice = form
				slug = invoice.slug
				inv_prodd = InvoiceProduct(product=product,invoice = invoice,price=price, quantity=quantity,prod_description=description)
				inv_prodd.save()

			
				#f.save()
				"""
				invoiceproduct = InvoiceProduct(product_id = Product.objects.get(description=cd.get('product')), quantity = quantity, price = price, 
				invoice_id=form.pk)
				invoiceproduct.save()"""
				
			"""inv_prod = invoice_product_form.save(commit=False)
			inv_prod.invoice_id = form.pk
			inv_prod.product_id = product.pk
			inv_prod.save()"""
			
			
		
			
			#InvoiceProduct.objects.create(product=product, order=form,quantity=quantity)
			messages.success(request, f'Invoice created successfully')
			return redirect('create-build-invoice',slug)
		
	
	else:
		form = InvoiceForm()
		client_form=ClientForm()
		product_formset = ProductFormSet()
		product_form = ProductForm()

	
	return render(request=request, template_name="invoice/create_invoice.html", context={"form":form, "client_form": client_form,"prod_form": product_form,"prod_formset":product_formset})

@login_required 
def view_invoices(request):
	context = {}
	invoices = Invoice.objects.all()
	context['invoices'] = invoices

	return render(request, 'invoice/invoices.html', context)
def search_invoices(request):

	if request.method == "GET":
		search_text = request.GET['search_text']
		if search_text is not None and search_text != u"":
			search_text = request.GET['search_text']
			invoices = Invoice.objects.filter(number__icontains = search_text)
		else:
			invoices = []


		data = invoices.values()
	

		return render(request, 'invoice/search_results.html', {"invoices": invoices})


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

@login_required
def products(request):
	context = {}
	products = Product.objects.all()
	context['products'] = products

	return redirect("create-invoice")

def createBuildInvoice(request, slug):
	#fetch that invoice
	try:
		invoice = Invoice.objects.get(slug=slug)
		pass
	except:
		messages.error(request, 'Something went wrong')
		return redirect('create-build-invoice', slug=slug)

	#fetch all the products - related to this invoice
	products = Product.objects.filter(invoice=invoice)
	invoiceproduct  = InvoiceProduct.objects.filter(invoice_id=invoice.id)

	invoiceCurrency = ''
	invoiceTotal = 0.0
	itemtotals = []
	tax=0
	if len(products) > 0:
		for x in invoiceproduct:
			y = float(x.quantity) * float(x.price)
			invoiceTotal += y
			itemtotals.append(y)
	if(invoice.istaxable):
		tax = 0.16*invoiceTotal
	sub_total = invoiceTotal+tax
	discount=(float(invoice.discount))*0.01*sub_total
	grand_total = sub_total
	discounted_grand_total = sub_total-discount
			



	context = {}
	context['invoice'] = invoice
	context['products'] = products
	context['itemtotals']= itemtotals
	context['discount']= "{:.2f}".format(discount)
	context['discounted_grand_total']= "{:.2f}".format(discounted_grand_total)
	context['discount_percentage']= invoice.discount
	context['invoiceGrandTotal'] = "{:.2f}".format(grand_total)
	context['invoiceTotal'] = "{:.2f}".format(invoiceTotal)
	context['tax'] =  "{:.2f}".format(tax)
	context['invoiceCurrency'] = invoiceCurrency
	context['invoiceproduct'] = invoiceproduct

	if request.method == 'GET':
		inv_form = InvoiceForm(instance=invoice)
		client_form = ClientSelectForm(initial_client=invoice.client)
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
	products = InvoiceProduct.objects.filter(invoice=invoice)

	#Get Client Settings
   

	#Calculate the Invoice Total
	invoiceCurrency = ''
	invoiceTotal = 0.0
	if len(products) > 0:
		for x in products:
			y = float(x.quantity) * float(x.price)
			invoiceTotal += y
	
	tax = 0.16*invoiceTotal
			



	context = {}
	context['invoice'] = invoice
	context['products'] = products
	context['invoiceTotal'] = "{:.2f}".format(invoiceTotal)
	context['tax'] =  "{:.2f}".format(tax)
	context['invoiceCurrency'] = invoiceCurrency


	return render(request, 'invoice/invoice-template.html',context)


def pdfview(request,slug):

	try:
		invoice = Invoice.objects.get(slug=slug)
		pass
	except:
		messages.error(request, 'Something went wrong')
		return redirect('invoices')

	#fetch all the products - related to this invoice
	products = Product.objects.filter(invoice=invoice)
	invoiceproduct  = InvoiceProduct.objects.filter(invoice_id=invoice.id)

	invoiceCurrency = ''
	invoiceTotal = 0.0
	itemtotals = []
	tax=0
	if len(products) > 0:
		for x in invoiceproduct:
			y = float(x.quantity) * float(x.price)
			invoiceTotal += y
			itemtotals.append(y)
	if(invoice.istaxable):
		tax = 0.16*invoiceTotal
	sub_total = invoiceTotal+tax
	discount=(float(invoice.discount))*0.01*sub_total
	grand_total = sub_total
	discounted_grand_total = sub_total-discount
			



	context = {}
	context['invoice'] = invoice
	context['products'] = products
	context['itemtotals']= itemtotals
	context['discount']= "{:.2f}".format(discount)
	context['discounted_grand_total']= discounted_grand_total
	context['discount_percentage']= invoice.discount
	context['invoiceGrandTotal'] = grand_total
	context['invoiceTotal'] = "{:.2f}".format(invoiceTotal)
	context['tax'] =  "{:.2f}".format(tax)
	context['invoiceCurrency'] = invoiceCurrency
	context['invoiceproduct'] = invoiceproduct
	

	paragraphs = ['first paragraph', 'second paragraph', 'third paragraph']
	html_string = render_to_string('invoice/pdf.html', context)

	html = HTML(string=html_string, base_url=request.build_absolute_uri())
	doc = html.render()
	pdf =doc.write_pdf()
	
	

	

	
   
	response = HttpResponse(pdf, content_type='application/pdf')
	#response['Content-Disposition'] = 'attachment; filename="mypdf.pdf"'
	return response

	

"""
def viewDocumentInvoice(request, slug):
	#fetch that invoice
	try:
		invoice = Invoice.objects.get(slug=slug)
		pass
	except:
		messages.error(request, 'Something went wrong')
		return redirect('invoices')
	#fetch all the products - related to this invoice
	products = Product.objects.filter(invoice=invoice)
	#Get Client Settings
	p_settings = Settings.objects.get(clientName='Skolo Online Learning')
	#Calculate the Invoice Total
	invoiceTotal = 0.0
	if len(products) > 0:
		for x in products:
			y = float(x.quantity) * float(x.price)
			invoiceTotal += y
	context = {}
	context['invoice'] = invoice
	context['products'] = products
	context['p_settings'] = p_settings
	context['invoiceTotal'] = "{:.2f}".format(invoiceTotal)
	#The name of your PDF file
	filename = '{}.pdf'.format(invoice.uniqueId)
	#HTML FIle to be converted to PDF - inside your Django directory
	#template = get_template('invoice/pdf-template.html')
	#Render the HTML
	#html = template.render(context)
	#Options - Very Important [Don't forget this]
	options = {
		  'encoding': 'UTF-8',
		  'javascript-delay':'10', #Optional
		  'enable-local-file-access': None, #To be able to access CSS
		  'page-size': 'A4',
		  'custom-header' : [
			  ('Accept-Encoding', 'gzip')
		  ],
	  }
	  #Javascript delay is optional
	#Remember that location to wkhtmltopdf
   # config = pdfkit.configuration(wkhtmltopdf='/usr/bin/wkhtmltopdf')
	#IF you have CSS to add to template
	#css1 = os.path.join(settings.CSS_LOCATION, 'assets', 'css', 'bootstrap.min.css')
	#css2 = os.path.join(settings.CSS_LOCATION, 'assets', 'css', 'dashboard.css')
	#Create the file
	#file_content = pdfkit.from_string(html, False, configuration=config, options=options)
	#Create the HTTP Response
	#response = HttpResponse(file_content, content_type='application/pdf')
	#response['Content-Disposition'] = 'inline; filename = {}'.format(filename)
	#Return
	#return response
"""

@login_required
def edit_invoice(request, slug):
	product=InvoiceProduct.objects.filter(id=id).first()
	product.delete()
@login_required
def edit_invoice(request, slug):
	invoice = Invoice.objects.filter(slug=slug).first()
	product = InvoiceProduct.objects.filter(invoice=invoice)
	clients = Client.objects.filter(invoice=invoice).first()
	products -
	form = InvoiceForm(instance=invoice)
	client_form = ClientForm(instance=clients)
	
	invoice_product_form = InvoiceProductForm()
	product_form = ProductForm()


	lists = InvoiceProduct.objects.filter(invoice_id=invoice.id)
	data = []
	for list in lists:
		lis_dict = {
			'product_id': list.product_id,
			'invoice_id': list.invoice_id,
			'product':Product.objects.get(id=list.product_id),
			'quantity': list.quantity,
			'price': list.price,
			'prod_description': list.prod_description,
			'id': list.id
		}
		data.append(lis_dict)
	
	
	EditFormset = formset_factory(InvoiceProductForm,
									 min_num=len(data), validate_min=True,
									 max_num=len(data), validate_max=True,
									 extra=0,can_delete=True)

	#product_formset = ProductEditFormSet(queryset=product)
	product_formset = DummyFormset(initial=data)
	product_formset_modal = EditFormset()

	if request.method == 'POST':
		slug = ''
		form = InvoiceForm(request.POST, instance=invoice)
		client_form = ClientForm(request.POST,instance=clients)
		product_formset = DummyFormset(request.POST,initial=data)
		invoice_product_form = InvoiceProductForm()

		
		if form.is_valid() and client_form.is_valid() and product_formset.is_valid():
			client=client_form.save(commit=False)
			
			
			#quantity = inv_prod.quantity
			form = form.save(commit=False)
			form.client = client
			
			
			#for inv_prod in invoice_product_form:
			form.save()
			client.save()

			slug = form.slug



			
			for f in product_formset: 
				cd = f.cleaned_data
				quantity = cd.get('quantity')
				price = cd.get('price')
				product= cd.get('product')
				description = cd.get('prod_description')
				
				invoice = form
				if f.cleaned_data["DELETE"]:
					pass
				else:
					InvoiceProduct.objects.update_or_create(product=product,invoice = invoice,defaults={"price":price, "quantity":quantity,"prod_description":description})
			
			
			
				#f.save()
			"""
				invoiceproduct = InvoiceProduct(product_id = Product.objects.get(description=cd.get('product')), quantity = quantity, price = price, 
				invoice_id=form.pk)
				invoiceproduct.save()"""
				
			"""inv_prod = invoice_product_form.save(commit=False)
			inv_prod.invoice_id = form.pk
			inv_prod.product_id = product.pk
			inv_prod.save()"""
			
			
		
			
			#InvoiceProduct.objects.create(product=product, order=form,quantity=quantity)
			messages.success(request, f'Invoice successfully updated.')
			return redirect('create-build-invoice',slug)
	
	return render(request=request, template_name="invoice/edit_invoice.html", context={"product_list":data,"form":form, "client_form": client_form,"product_formset_modal": product_formset,"prod_form": product_form,"prod_formset":product_formset})

def emailDocumentInvoice(request, slug):
	#fetch that invoice
	try:
		invoice = Invoice.objects.get(slug=slug)
		pass
	except:
		messages.error(request, 'Something went wrong')
		return redirect('invoices')

	#fetch all the products - related to this invoice
	products = Product.objects.filter(invoice=invoice)
	invoiceproduct  = InvoiceProduct.objects.filter(invoice_id=invoice.id)

	invoiceCurrency = ''
	invoiceTotal = 0.0
	itemtotals = []
	if len(products) > 0:
		for x in invoiceproduct:
			y = float(x.quantity) * float(x.price)
			invoiceTotal += y
			itemtotals.append(y)
	
	tax = 0.16*invoiceTotal
	grand_total = invoiceTotal+tax
			



	context = {}
	context['invoice'] = invoice
	context['products'] = products
	context['itemtotals']= itemtotals
	context['invoiceGrandTotal'] = grand_total
	context['invoiceTotal'] = "{:.2f}".format(invoiceTotal)
	context['tax'] =  "{:.2f}".format(tax)
	context['invoiceCurrency'] = invoiceCurrency
	context['invoiceproduct'] = invoiceproduct
	
	#The name of your PDF file
	filename = '{}.pdf'.format(invoice.uniqueId)
	#HTML FIle to be converted to PDF - inside your Django directory
	#template = get_template('invoice/pdf-template.html')
	#Render the HTML
	#html = template.render(context)
	#Options - Very Important [Don't forget this]
	options = {
		  'encoding': 'UTF-8',
		  'javascript-delay':'1000', #Optional
		  'enable-local-file-access': None, #To be able to access CSS
		  'page-size': 'A4',
		  'custom-header' : [
			  ('Accept-Encoding', 'gzip')
		  ],
	  }
	  #Javascript delay is optional
	#Remember that location to wkhtmltopdf
	#Saving the File
	filepath = os.path.join(settings.MEDIA_ROOT, 'client_invoices')
	os.makedirs(filepath, exist_ok=True)
	
	#Save the PDF
	html_string = render_to_string('invoice/pdf.html', context)

	html = HTML(string=html_string, base_url=request.build_absolute_uri())
	doc = html.render()
	pdf =doc.write_pdf()
	pdf_save_path = filepath+filename


	#pdfkit.from_string(html, pdf_save_path, configuration=config, options=options)
	#send the emails to client
	to_email = invoice.client.emailAddress
	from_client = invoice.client.clientName
	emailInvoiceClient(pdf,to_email, from_client, filename)
	invoice.status = 'EMAIL_SENT'
	invoice.save()
	#Email was send, redirect back to view - invoice
	messages.success(request, "Email sent to the client succesfully")
	return redirect('create-build-invoice', slug=slug)
	#view invoices here
	
# Create your views here.

class ProductAddView(TemplateView):
	template_name = "invoice/create_invoice.html"

	def get(self, *args, **kwargs):
		formset = ProductFormSet(queryset=InvoiceProduct.objects.none())
		return self.render_to_response({'product_formset': formset})

	# Define method to handle POST request
	def post(self, *args, **kwargs):

		formset = ProductFormSet(data=self.request.POST)

		# Check if submitted forms are valid
		if formset.is_valid():
			formset.save()
			return redirect(reverse_lazy("product_list"))

		return self.render_to_response({'product_formset': formset})