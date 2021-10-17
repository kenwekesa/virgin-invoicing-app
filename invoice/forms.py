from django import forms
from django.contrib.auth.models import User
from django.forms import widgets
from .models import *
from crispy_forms.helper import FormHelper

from crispy_forms.layout import Column, Div, Field, Layout, Row, Submit

import json



class DateInput(forms.DateInput):
    input_type = 'date'


class InvoiceForm(forms.ModelForm):
    THE_OPTIONS = [
    ('14 days', '14 days'),
    ('30 days', '30 days'),
    ('60 days', '60 days'),
    ]
    STATUS_OPTIONS = [
    ('CURRENT', 'CURRENT'),
    ('OVERDUE', 'OVERDUE'),
    ('PAID', 'PAID'),
    ]

    quantity = forms.CharField(
                    required = True,
                    label='Quantity(packs)',
                    widget=forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Enter quantity in packs'}),)
    
    unit_price = forms.CharField(
                    required = True,
                    label='Unit price(Ksh)',
                    widget=forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Enter the unit price in Ksh'}),)

    paymentTerms = forms.ChoiceField(
                    choices = THE_OPTIONS,
                    required = True,
                    label='Select Payment Terms',
                    widget=forms.Select(attrs={'class': 'form-control mb-3'}),)
    status = forms.ChoiceField(
                    choices = STATUS_OPTIONS,
                    required = True,
                    label='Change Invoice Status',
                    widget=forms.Select(attrs={'class': 'form-control mb-3'}),)
    description = forms.CharField(
                    required = True,
                    label='Service Description: ',
                    widget=forms.Textarea(attrs={'class': 'form-control mb-3'}))

    dueDate = forms.DateField(
                        required = True,
                        label='Invoice Due',
                        widget=DateInput(attrs={'class': 'form-control mb-3'}),)


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('quantity', css_class='form-group col-md-4'),
                Column('unit-price', css_class='form-group col-md-4'),
                Column('dueDate', css_class='form-group col-md-6'),
                css_class='form-row'),
            Row(
                Column('paymentTerms', css_class='form-group col-md-4'),
                Column('status', css_class='form-group col-md-6'),
                css_class='form-row'),
            'description',

            Submit('submit', ' EDIT INVOICE '))

    class Meta:
        model = Invoice
        fields = ['dueDate', 'quantity', 'unit_price', 'paymentTerms', 'status', 'description']


    
       
    

    class Meta:
        model = Invoice
        fields = ['number','quantity','unit_price', 'dueDate', 'paymentTerms', 'status', 'description', 'client']

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['clientName', 'addressLine1', 'city', 'postalCode', 'phoneNumber', 'emailAddress']



class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'description', 'quantity', 'price', 'currency']



class ClientSelectForm(forms.ModelForm):

    def __init__(self,*args,**kwargs):
        self.initial_client = kwargs.pop('initial_client')
        self.CLIENT_LIST = Client.objects.all()
        self.CLIENT_CHOICES = [('-----', '--Select a Client--')]


        for client in self.CLIENT_LIST:
            d_t = (client.uniqueId, client.clientName)
            self.CLIENT_CHOICES.append(d_t)


        super(ClientSelectForm,self).__init__(*args,**kwargs)

        self.fields['client'] = forms.ChoiceField(
                                        label='Choose a related client',
                                        choices = self.CLIENT_CHOICES,
                                        widget=forms.Select(attrs={'class': 'form-control mb-3'}),)

    class Meta:
        model = Invoice
        fields = ['client']


    def clean_client(self):
        c_client = self.cleaned_data['client']
        if c_client == '-----':
            return self.initial_client
        else:
            return Client.objects.get(uniqueId=c_client)