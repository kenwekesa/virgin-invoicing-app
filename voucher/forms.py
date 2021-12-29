from crispy_forms.layout import Column, Layout, Row, Submit
from django import forms
from django.forms.widgets import DateInput

from invoice.models import Invoice
from crispy_forms.helper import FormHelper


class VoucherForm(forms.ModelForm):
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
        model = Voucher
        fields = ['number', 'facility_name', 'number_of_adults',
                  'number_of_children', 'children_age', 'infants', 'baby_cot', 'accomodation', 'meal_plan', 'extras_to', 'special_instructions',
                  'reserver_name', 'reservation_date', 'client_name', 'client_email'
                  ]

    def clean(self, *args, **kwargs):
        super(InvoiceForm, self).clean()

        # getting username and password from cleaned_data
        number = self.cleaned_data.get('number')
        dueDate = self.cleaned_data.get('password')

        # validating the username and password
        if 'VRG' not in number:
            self._errors['number'] = self.error_class(
                ['Invalid invoice number'])