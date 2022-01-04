from crispy_forms.layout import Column, Layout, Row, Submit
from django import forms
from django.db.models.enums import Choices
from django.forms.widgets import DateInput

from voucher.models import Voucher
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

    types = [
        ('RESIDENT', 'RESIDENT'),
        ('NON RESIDENT', 'NON RESIDENT'),
        
    ]

    ai = forms.BooleanField(label='', required=False)
    hb = forms.BooleanField(label='', required=False)
    bb = forms.BooleanField(label='', required=False)
    fb = forms.BooleanField(label='', required=False)
    single = forms.BooleanField(label='', required=False)
    double = forms.BooleanField(label='', required=False)
    twin = forms.BooleanField(label='', required=False)
    triple = forms.BooleanField(label='', required=False)

    arrival = forms.DateTimeField(required=False, label='')
    departure = forms.DateTimeField(required=False, label='')
    number_of_nights = forms.CharField(required=False, label='')

   

    reservation_date = forms.DateField(
        required=True,
        label='Reservation Date',
        widget=DateInput(attrs={'class': 'form-control mb-3'}),)

    accommodation_type = forms.ChoiceField(

                        label='Accommodation for:',
                        widget=forms.RadioSelect,
                        choices=types
                    )

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
                  'number_of_children', 'children_age', 'infants', 'baby_cot', 'extras_to', 'special_instructions',
                  'reserver_name', 'reservation_date', 'client', 'double', 'single', 'twin', 'triple', 'hb', 'fb', 'bb', 'ai',
                  'departure', 'arrival', 'number_of_nights','accommodation_type','voucher_status'
                  ]

    def clean(self, *args, **kwargs):
        super(VoucherForm, self).clean()

        # getting username and password from cleaned_data
        number = self.cleaned_data.get('number')
        dueDate = self.cleaned_data.get('password')

        # validating the username and password
        if 'VCH' not in number:
            self._errors['number'] = self.error_class(
                ['Invalid voucher number'])
