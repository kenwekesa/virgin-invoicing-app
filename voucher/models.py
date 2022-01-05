from django.db import models

from django.core import validators
from django.db import models
from django.template.defaultfilters import slugify
from django.urls.base import reverse
from django.utils import timezone
from uuid import uuid4
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

from invoice.models import Client

# Create your models here.


def increment_voucher_number():
    last_invoice = Voucher.objects.all().order_by('id').last()
    if not last_invoice:
        return 'VCH00001'
    invoice_no = last_invoice.number
    invoice_int = int(invoice_no.split('VCH')[-1])
    new_invoice_int = invoice_int + 1
    new_invoice_no = 'VCH' + "%05d" % (new_invoice_int, )
    return new_invoice_no


class Voucher(models.Model):
    TERMS = [
        ('Immediate', 'Immediate'),
        ('15 days', '15 days'),
        ('30 days', '30 days'),

    ]

    STATUS = [
        ('CANCELLED', 'CANCELLED'),
        ('EMAIL_SENT', 'EMAIL_SENT'),
        ('MODIFIED', 'MODIFIED'),
        ('NEW','NEW')
        
    ]
    types = [
        ('RESIDENT', 'RESIDENT'),
        ('NON RESIDENT', 'NON RESIDENT'),
        
    ]

    number = models.CharField(
        null=False, default=increment_voucher_number, blank=False, max_length=100, unique=True)
    facility_name = models.CharField(null=True, blank=True, max_length=500)
    number_of_adults = models.CharField(
        default='0', max_length=100)
    number_of_children = models.CharField(
        default='0', max_length=100)
    children_age = models.CharField(null=True, blank=True, max_length=500)
    infants = models.CharField(null=True, blank=True, max_length=500)
    baby_cot = models.CharField(null=True, blank=True, max_length=500)

    extras_to = models.CharField(null=True, blank=True, max_length=500)
    special_instructions = models.CharField(
        null=True, blank=True, max_length=500)
    reserver_name = models.CharField(null=True, blank=True, max_length=500)
    reservation_date = models.DateField(null=True, blank=True, max_length=500)

    arrival = models.DateTimeField(blank=True, null=True)
    departure = models.DateTimeField(blank=True, null=True)
    number_of_nights = models.CharField(blank=True, null=True, max_length=12)

    accommodation_type = models.CharField(
        choices=types, default='RESIDENT', max_length=19)
    voucher_status = models.CharField(
        choices=STATUS, default='NEW', null = True, blank=True, max_length=19)

    

    # Accomodation
    single = models.BooleanField()
    double = models.BooleanField()
    triple = models.BooleanField()
    twin = models.BooleanField()

    # Food plan
    hb = models.BooleanField()
    fb = models.BooleanField()
    bb = models.BooleanField()
    ai = models.BooleanField()

    # RELATED fields
    client = models.ForeignKey(
        Client, blank=True, null=True, on_delete=models.SET_NULL)

    # Utility fields
    uniqueId = models.CharField(null=True, blank=True, max_length=100)
    slug = models.SlugField(max_length=500, unique=True, blank=True, null=True)
    date_created = models.DateTimeField(blank=True, null=True)
    last_updated = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return '{} {}'.format(self.number, self.uniqueId)

    def get_absolute_url(self):
        return reverse('invoice-detail', kwargs={'slug': self.slug})

    # def total_price(self):
    #	return float(100)
    def total_price(self):
        temp_values = [int(product.price) * int(product.quantity)
                       for product in InvoiceProduct.objects.filter(invoice_id=self.id)]
        return sum(temp_values)

    def grand_total(self):
        temp_values = 0.00
        for product in InvoiceProduct.objects.filter(invoice_id=self.id):
            if product.price and product.quantity:
                temp_values = temp_values + \
                    (int(product.price) * int(product.quantity))

        return temp_values

    def save(self, *args, **kwargs):
        if self.date_created is None:
            self.date_created = timezone.localtime(timezone.now())
        if self.uniqueId is None:
            self.uniqueId = str(uuid4()).split('-')[4]
            self.slug = slugify('{} {}'.format(self.number, self.uniqueId))

        self.slug = slugify('{} {}'.format(self.number, self.uniqueId))
        self.last_updated = timezone.localtime(timezone.now())

        super(Voucher, self).save(*args, **kwargs)
