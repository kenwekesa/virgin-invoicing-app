from django.db import models
from django.template.defaultfilters import slugify
from django.urls.base import reverse
from django.utils import timezone
from uuid import uuid4
from django.contrib.auth.models import User




class Client(models.Model):



  
	#Basic Fields.
	clientName = models.CharField(null=True, blank=True, max_length=200)
	address = models.CharField(null=True, blank=True, max_length=200)
	postalCode = models.CharField(null=True, blank=True, max_length=10)
	phoneNumber = models.CharField(null=True, blank=True, max_length=100)
	emailAddress = models.CharField(null=True, blank=True, max_length=100)
	


	#Utility fields
	uniqueId = models.CharField(null=True, blank=True, max_length=100)
	slug = models.SlugField(max_length=500, unique=True, blank=True, null=True)
	date_created = models.DateTimeField(blank=True, null=True)
	last_updated = models.DateTimeField(blank=True, null=True)


	def __str__(self):
		return '{} {}'.format(self.clientName, self.uniqueId)


	def get_absolute_url(self):
		return reverse('client-detail', kwargs={'slug': self.slug})


	def save(self, *args, **kwargs):
		if self.date_created is None:
			self.date_created = timezone.localtime(timezone.now())
		if self.uniqueId is None:
			self.uniqueId = str(uuid4()).split('-')[4]
			self.slug = slugify('{} {} {}'.format(self.clientName, self.city, self.uniqueId))

		self.slug = slugify('{} {} {}'.format(self.clientName, self.city, self.uniqueId))
		self.last_updated = timezone.localtime(timezone.now())

		super(Client, self).save(*args, **kwargs)


def increment_invoice_number():
		last_invoice = Invoice.objects.all().order_by('id').last()
		if not last_invoice:
			return 'VRG00001'
		invoice_no = last_invoice.number
		invoice_int = int(invoice_no.split('VRG')[-1])
		new_invoice_int = invoice_int + 1
		new_invoice_no = 'VRG' +  "%05d" % ( new_invoice_int, )
		return new_invoice_no

class Invoice(models.Model):
	TERMS = [
	('Immediate','Immediate'),
	('15 days', '15 days'),
	('30 days', '30 days'),
	
	]

	STATUS = [
	('CURRENT', 'CURRENT'),
	('EMAIL_SENT', 'EMAIL_SENT'),
	('OVERDUE', 'OVERDUE'),
	('PAID', 'PAID'),
	]
    
	



	number = models.CharField(null=False,default=increment_invoice_number, blank=False, max_length=100, unique=True)
	dueDate = models.DateField(null=True, blank=True)
	paymentTerms = models.CharField(choices=TERMS, default='15 days', max_length=100)
	status = models.CharField(choices=STATUS, default='CURRENT', max_length=100)
	description = models.TextField(null=True, blank=True,max_length=500)
	istaxable = models.BooleanField()

	#RELATED fields
	client = models.ForeignKey(Client, blank=True, null=True, on_delete=models.SET_NULL)
	

	#Utility fields
	uniqueId = models.CharField(null=True, blank=True, max_length=100)
	slug = models.SlugField(max_length=500, unique=True, blank=True, null=True)
	date_created = models.DateTimeField(blank=True, null=True)
	last_updated = models.DateTimeField(blank=True, null=True)


	def __str__(self):
		return '{} {}'.format(self.number, self.uniqueId)


	def get_absolute_url(self):
		return reverse('invoice-detail', kwargs={'slug': self.slug})

	#def total_price(self):
	#	return float(100)
	def total_price(self):
		temp_values = [int(product.price)* int(product.quantity) for product in InvoiceProduct.objects.filter(invoice_id=self.id)]
		return sum(temp_values)

	def grand_total(self):
		temp_values = [int(product.price)* int(product.quantity) for product in InvoiceProduct.objects.filter(invoice_id=self.id)]
		return sum(temp_values)



	def save(self, *args, **kwargs):
		if self.date_created is None:
			self.date_created = timezone.localtime(timezone.now())
		if self.uniqueId is None:
			self.uniqueId = str(uuid4()).split('-')[4]
			self.slug = slugify('{} {}'.format(self.number, self.uniqueId))

		self.slug = slugify('{} {}'.format(self.number, self.uniqueId))
		self.last_updated = timezone.localtime(timezone.now())

		super(Invoice, self).save(*args, **kwargs)

	



class Product(models.Model):
	CURRENCY = [
	('Ksh', 'KES'),
	('Ksh', 'KES'),
	]
	PRODUCTS = [
		('Accommodation/Hotel','Accommodation/Hotel'),
                ('Conference', 'Conference'),
		('Excursions','Excursions'),
		('Air Ticket',"Air Ticket"),
		('Others','Others')
	]
	description = models.CharField(null=False, blank=False, max_length=200)
	currency = models.CharField(blank=True, null=True,default='Kshs', max_length=100)

	#Related Fields
	invoice = models.ManyToManyField(Invoice, through='InvoiceProduct')

	#Utility fields
	uniqueId = models.CharField(null=True, blank=True, max_length=100)
	slug = models.SlugField(max_length=500, unique=True, blank=True, null=True)
	date_created = models.DateTimeField(blank=True, null=True)
	last_updated = models.DateTimeField(blank=True, null=True)


	def __str__(self):
		return '{}'.format(self.description)


	def get_absolute_url(self):
		return reverse('product-detail', kwargs={'slug': self.slug})


	def save(self, *args, **kwargs):
		if self.date_created is None:
			self.date_created = timezone.localtime(timezone.now())
		if self.uniqueId is None:
			self.uniqueId = str(uuid4()).split('-')[4]
			self.slug = slugify('{} {}'.format(self.description, self.uniqueId))

		self.slug = slugify('{} {}'.format(self.description, self.uniqueId))
		self.last_updated = timezone.localtime(timezone.now())

		super(Product, self).save(*args, **kwargs)
		
class InvoiceProduct(models.Model):
	invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	prod_description = models.TextField(null=True, blank=True, max_length=150)
	quantity = models.IntegerField(default=1)
	price = models.CharField(null=True, blank=True, max_length=10)

	class Meta:
		unique_together = [['invoice','product']]



	def total_price(self):
		total_price = int(self.quantity)*int(self.price)
		return total_price

class Settings(models.Model):

	CITIES = [
	('Gauteng', 'Gauteng'),
	('Free State', 'Free State'),
	('Limpopo', 'Limpopo'),
	]

	#Basic Fields
	clientName = models.CharField(null=True, blank=True, max_length=200)
	addressLine1 = models.CharField(null=True, blank=True, max_length=200)
	city = models.CharField(choices=CITIES, blank=True, max_length=100)
	postalCode = models.CharField(null=True, blank=True, max_length=10)
	phoneNumber = models.CharField(null=True, blank=True, max_length=100)
	emailAddress = models.CharField(null=True, blank=True, max_length=100)
 


	#Utility fields
	uniqueId = models.CharField(null=True, blank=True, max_length=100)
	slug = models.SlugField(max_length=500, unique=True, blank=True, null=True)
	date_created = models.DateTimeField(blank=True, null=True)
	last_updated = models.DateTimeField(blank=True, null=True)


	def __str__(self):
		return '{} {} {}'.format(self.clientName, self.city, self.uniqueId)


	def get_absolute_url(self):
		return reverse('settings-detail', kwargs={'slug': self.slug})


	def save(self, *args, **kwargs):
		if self.date_created is None:
			self.date_created = timezone.localtime(timezone.now())
		if self.uniqueId is None:
			self.uniqueId = str(uuid4()).split('-')[4]
			self.slug = slugify('{} {} {}'.format(self.clientName, self.city, self.uniqueId))

		self.slug = slugify('{} {} {}'.format(self.clientName, self.city, self.uniqueId))
		self.last_updated = timezone.localtime(timezone.now())

		super(Settings, self).save(*args, **kwargs)
