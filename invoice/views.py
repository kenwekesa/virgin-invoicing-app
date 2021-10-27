from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string

#from virginafrica.invoice.models import Settings
from .forms import InvoiceForm, ProductForm, ClientForm,ClientSelectForm
from django.contrib import messages
from invoice.models import Invoice,Product,Client
from WeasyPrint import HTML


import tempfile

from django.core.files.storage import FileSystemStorage

from weasyprint import HTML




def main(request):
	return render(request, 'invoice/main.html')

def create_invoice(request):
	if request.method == 'POST':
		form = InvoiceForm(request.POST)
		client_form = ClientForm(request.POST)
		prod_form = ProductForm(request.POST)
		if form.is_valid and client_form.is_valid and prod_form.is_valid:
			client=client_form.save()
			form = form.save(commit=False)
			product = prod_form.save(commit=False)
			form.client = client
			product.invoice =form
			form.save()
			messages.success(request, f'Invoice created successfully')
			return redirect('view-invoices')
	
	else:
		form = InvoiceForm()
		client_form=ClientForm()
		prod_form= ProductForm()
	
	return render(request=request, template_name="invoice/create_invoice.html", context={"form":form, "client_form": client_form,"prod_form":prod_form})

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


def pdfview(request):
	paragraphs = ['first paragraph', 'second paragraph', 'third paragraph']
	html_string = render_to_string('invoice/pdf.html', {'paragraphs': paragraphs})

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

"""def emailDocumentInvoice(request, slug):
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
	html = template.render(context)
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
	config = pdfkit.configuration(wkhtmltopdf='/usr/bin/wkhtmltopdf')
	#Saving the File
	filepath = os.path.join(settings.MEDIA_ROOT, 'client_invoices')
	os.makedirs(filepath, exist_ok=True)
	pdf_save_path = filepath+filename
	#Save the PDF
	pdfkit.from_string(html, pdf_save_path, configuration=config, options=options)
	#send the emails to client
	to_email = invoice.client.emailAddress
	from_client = p_settings.clientName
	emailInvoiceClient(to_email, from_client, pdf_save_path)
	invoice.status = 'EMAIL_SENT'
	invoice.save()
	#Email was send, redirect back to view - invoice
	messages.success(request, "Email sent to the client succesfully")
	return redirect('create-build-invoice', slug=slug)
	#view invoices here
	
# Create your views here.
"""