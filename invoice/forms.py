from django import forms
from django.contrib.auth.models import User
from django.forms import widgets, modelformset_factory
from django.forms.formsets import formset_factory
from django.forms.models import inlineformset_factory
from .models import *
from crispy_forms.helper import FormHelper

from crispy_forms.layout import Column, Div, Field, Layout, Row, Submit

import json


class DateInput(forms.DateInput):
    input_type = 'date'


class InvoiceForm(forms.ModelForm):
    THE_OPTIONS = [
        ('Immediate', 'Immediate'),
        ('15 days', '15 days'),
        ('30 days', '30 days'),
        ('60 days', '60 days'),
    ]
    STATUS_OPTIONS = [
        ('CURRENT', 'CURRENT'),
        ('OVERDUE', 'OVERDUE'),
        ('PAID', 'PAID'),
    ]

    istaxable = forms.BooleanField(label="Taxable", required=False)
    paymentTerms = forms.ChoiceField(
        choices=THE_OPTIONS,
        required=True,
        label='Payment Terms',
        widget=forms.Select(attrs={'class': 'form-control mb-3'}),)
    status = forms.ChoiceField(
        choices=STATUS_OPTIONS,
        required=True,
        label='Invoice Status',
        widget=forms.Select(attrs={'class': 'form-control mb-3'}),)

    dueDate = forms.DateField(
        required=True,
        label='Invoice Due',
        widget=DateInput(attrs={'class': 'form-control mb-3'}),)

    discont = forms.CharField(required=False, label='')

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

        self.fields['number'].widget.attrs['readonly'] = True

    class Meta:
        model = Invoice
        fields = ['number', 'dueDate', 'paymentTerms', 'status',
                  'description', 'client', 'istaxable', 'apply_discount', 'discount']

    def clean(self, *args, **kwargs):
        super(InvoiceForm, self).clean()

        # getting username and password from cleaned_data
        number = self.cleaned_data.get('number')
        dueDate = self.cleaned_data.get('password')

        # validating the username and password
        if 'VRG' not in number:
            self._errors['number'] = self.error_class(
                ['Invalid invoice number'])


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['clientName', 'address',
                  'postalCode', 'phoneNumber', 'emailAddress']


class InvoiceProductForm(forms.ModelForm):

    class Meta:
        model = InvoiceProduct
        fields = ['product', 'quantity', 'price', 'prod_description']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False


ProductFormSet = formset_factory(
    InvoiceProductForm, extra=1
)

ProductEditFormSet = modelformset_factory(
    InvoiceProduct, form=InvoiceProductForm, extra=0
)


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['description', 'currency']


class ClientSelectForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.initial_client = kwargs.pop('initial_client')
        self.CLIENT_LIST = Client.objects.all()
        self.CLIENT_CHOICES = [('-----', '--Select a Client--')]

        for client in self.CLIENT_LIST:
            d_t = (client.uniqueId, client.clientName)
            self.CLIENT_CHOICES.append(d_t)

        super(ClientSelectForm, self).__init__(*args, **kwargs)

        self.fields['client'] = forms.ChoiceField(
            label='Choose a related client',
            choices=self.CLIENT_CHOICES,
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
