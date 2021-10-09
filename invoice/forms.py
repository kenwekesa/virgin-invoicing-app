from django import forms
from django.contrib.auth.models import User
from django.forms import widgets
from .models import *
from crispy_forms.helper import FormHelper

from crispy_forms.layout import Div, Field, Layout

import json



class DateInput(forms.DateInput):
    input_type = 'date'


class InvoiceForm(forms.ModelForm):
    dueDate = forms.DateField(
                        required = True,
                        label='Invoice Due',
                        widget=DateInput(attrs={'class': 'form-control'}),)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
             Div(
            Field('field1', css_class='col-md-3'),
            Field('field3', css_class='col-md-9'),  
        css_class='form-row') 
        )
    
       
    

    class Meta:
        model = Invoice
        fields = ['title', 'number', 'dueDate', 'paymentTerms', 'status', 'notes', 'client', 'product']