from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string

from dateutil import parser as date_parser


#from virginafrica.invoice.models import Settings
from django.contrib import messages
from invoice.models import Invoice, Product, Client, InvoiceProduct
from voucher.models import Voucher

from django.core.files.storage import FileSystemStorage

from weasyprint import HTML, css

from voucher.forms import VoucherForm
from invoice.forms import ClientForm


from virginafrica.functions import emailVoucher




from re import template
from django.conf import settings
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect

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


from django.core.files.storage import FileSystemStorage

from weasyprint import HTML
import os

def create_voucher(request):
	slug=''
	if request.method == 'POST':
		slug = ''
		form = VoucherForm(request.POST)
		client_form = ClientForm(request.POST)
		
		if form.is_valid() and client_form.is_valid():
			client=client_form.save()	
			
			#quantity = inv_prod.quantity
			form = form.save(commit=False)
			form.client = client
			
			
			#for inv_prod in invoice_product_form:
			form.save()
			client.save()
			slug=form.slug
			
			#InvoiceProduct.objects.create(product=product, order=form,quantity=quantity)
			messages.success(request, f'Voucher created successfully')
			return redirect('view-voucher',slug)
		
	
	else:
		form = VoucherForm()
		client_form = ClientForm()

	return render(request, 'voucher/create_voucher.html', context={"form": form, "client_form": client_form})




@login_required
def edit_voucher(request, slug):
	voucher = Voucher.objects.filter(slug=slug).first()
	clients = Client.objects.filter(voucher=voucher).first()
	form = VoucherForm(instance=voucher)
	client_form = ClientForm(instance=clients)
	
	


	if request.method == 'POST':
		slug = ''
		form = VoucherForm(request.POST,instance=voucher)
		client_form = ClientForm(request.POST, instance=clients)
		
		if form.is_valid() and client_form.is_valid():
			client=client_form.save()	
			
			#quantity = inv_prod.quantity
			form = form.save(commit=False)
			form.client = client
			
			
			#for inv_prod in invoice_product_form:
			form.save()
			client.save()
			slug=form.slug
			
			#InvoiceProduct.objects.create(product=product, order=form,quantity=quantity)
			messages.success(request, f'Voucher updated successfully')
			return redirect('view-voucher',slug)
		
	
	
	return render(request, 'voucher/edit_voucher.html', context={"form": form, "client_form": client_form})

@login_required
def view_voucher(request,slug):

	# fetch all the products - related to this invoice

	#fetch that invoice
	try:
		voucher = Voucher.objects.get(slug=slug)
		pass
	except:
		messages.error(request, 'Something went wrong')
		return redirect('view-voucher', slug=slug)

	#fetch all the products - related to this invoice
	

	
			



	context = {}
	context['voucher'] = voucher
	

	return render(request, 'voucher/created_voucher.html', context)


def viewPDFInvoice(request, slug):
	# fetch that invoice
	try:
		invoice = Invoice.objects.get(slug=slug)
		pass
	except:
		messages.error(request, 'Something went wrong')
		return redirect('invoices')

	# fetch all the products - related to this invoice
	#products = Product.objects.filter(invoice=invoice)

	# Get Client Settings

	# Calculate the Invoice Total
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


def voucher_template(request):
	paragraphs = ['first paragraph', 'second paragraph', 'third paragraph']

	context = {}
	if request.method == 'POST':

		context['noofadults'] = request.POST.get('noofadults')
		context['noofchildren'] = request.POST.get('noofchildren')
		context['infants'] = request.POST.get('infants')
		context['age'] = request.POST.get('age')
		context['babycot'] = request.POST.get('babycot')
		context['date'] = date_parser.parse(request.POST.get('date'))
		context['name'] = request.POST.get('name')
		context['packs'] = request.POST.getlist('pack')
		context['lodgename'] = request.POST.get('lodgename')

	html_string = render_to_string('voucher/voucher_template.html', context)
	html = HTML(string=html_string, base_url=request.build_absolute_uri())
	doc = html.render()
	pdf = doc.write_pdf()

	response = HttpResponse(pdf, content_type='application/pdf')
	#response['Content-Disposition'] = 'attachment; filename="mypdf.pdf"'
	return response




@login_required 
def list_vouchers(request):
	context = {}
	vouchers = Voucher.objects.all()
	context['vouchers'] = vouchers

	return render(request, 'voucher/vouchers.html', context)




def pdfview(request,slug):

	try:
		voucher = Voucher.objects.get(slug=slug)
		pass
	except:
		messages.error(request, 'Something went wrong')
		return redirect('vouchers')

	



	context = {}
	context['voucher'] = voucher
	
	
	

	
	html_string = render_to_string('voucher/voucher_template.html', context)

	html = HTML(string=html_string, base_url=request.build_absolute_uri())
	doc = html.render()
	pdf =doc.write_pdf()


	response = HttpResponse(pdf, content_type='application/pdf')
	#response['Content-Disposition'] = 'attachment; filename="mypdf.pdf"'
	return response
	
	



def cancel_voucher(request, slug):
	#fetch that invoice
	try:
		voucher = Voucher.objects.get(slug=slug)
		pass
	except:
		messages.error(request, 'Something went wrong')
		return redirect('vouchers')

	
			

	voucher.status = 'CANCELLED'
	voucher.save()

	context = {}
	context['voucher'] = voucher
	
	
	#The name of your PDF file
	filename = '{}.pdf'.format(voucher.uniqueId)
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
	filepath = os.path.join(settings.MEDIA_ROOT, 'client_vouchers')
	os.makedirs(filepath, exist_ok=True)
	
	#Save the PDF
	html_string = render_to_string('voucher/voucher_template.html', context)

	html = HTML(string=html_string, base_url=request.build_absolute_uri())
	doc = html.render()
	pdf =doc.write_pdf()
	pdf_save_path = filepath+filename


	#pdfkit.from_string(html, pdf_save_path, configuration=config, options=options)
	#send the emails to client
	to_email = voucher.client.emailAddress
	from_client = voucher.client.clientName
	emailVoucher(pdf,to_email, from_client, filename)
	
	#Email was send, redirect back to view - invoice
	messages.success(request, "Cancel mail sent to the client succesfully")
	return redirect('view-voucher', slug=slug)
	#view invoices here


def email_voucher(request, slug):
	#fetch that invoice
	try:
		voucher = Voucher.objects.get(slug=slug)
		pass
	except:
		messages.error(request, 'Something went wrong')
		return redirect('vouchers')

	
			



	context = {}
	context['voucher'] = voucher
	
	
	#The name of your PDF file
	filename = '{}.pdf'.format(voucher.uniqueId)
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
	filepath = os.path.join(settings.MEDIA_ROOT, 'client_vouchers')
	os.makedirs(filepath, exist_ok=True)
	
	#Save the PDF
	html_string = render_to_string('voucher/voucher_template.html', context)

	html = HTML(string=html_string, base_url=request.build_absolute_uri())
	doc = html.render()
	pdf =doc.write_pdf()
	pdf_save_path = filepath+filename


	#pdfkit.from_string(html, pdf_save_path, configuration=config, options=options)
	#send the emails to client
	to_email = voucher.client.emailAddress
	from_client = voucher.client.clientName
	emailVoucher(pdf,to_email, from_client, filename)
	#invoice.status = 'EMAIL_SENT'
	#invoice.save()
	#Email was send, redirect back to view - invoice
	messages.success(request, "Email sent to the client succesfully")
	return redirect('view-voucher', slug=slug)
	#view invoices here

	
def amend_voucher(request, slug):
	#fetch that invoice
	try:
		voucher = Voucher.objects.get(slug=slug)
		pass
	except:
		messages.error(request, 'Something went wrong')
		return redirect('vouchers')

	
			
	voucher.status = 'MODIFIED'
	voucher.save()


	context = {}
	context['voucher'] = voucher
	
	
	#The name of your PDF file
	filename = '{}.pdf'.format(voucher.uniqueId)
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
	filepath = os.path.join(settings.MEDIA_ROOT, 'client_vouchers')
	os.makedirs(filepath, exist_ok=True)
	
	#Save the PDF
	html_string = render_to_string('voucher/voucher_template.html', context)

	html = HTML(string=html_string, base_url=request.build_absolute_uri())
	doc = html.render()
	pdf =doc.write_pdf()
	pdf_save_path = filepath+filename


	#pdfkit.from_string(html, pdf_save_path, configuration=config, options=options)
	#send the emails to client
	to_email = voucher.client.emailAddress
	from_client = voucher.client.clientName
	emailVoucher(pdf,to_email, from_client, filename)
	#invoice.status = 'EMAIL_SENT'
	#invoice.save()
	#Email was send, redirect back to view - invoice
	messages.success(request, "Amend mail sent to the client succesfully")
	return redirect('view-voucher', slug=slug)
	#view invoices here
   