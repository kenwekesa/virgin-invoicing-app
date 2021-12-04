from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string

from dateutil import parser as date_parser




#from virginafrica.invoice.models import Settings
from django.contrib import messages
from invoice.models import Invoice,Product,Client,InvoiceProduct

from django.core.files.storage import FileSystemStorage

from weasyprint import HTML, css





def view_voucher(request):
    
    #fetch all the products - related to this invoice
    


    context = {}
    '''context['invoice'] = invoice
    context['products'] = products
    context['invoiceproduct'] = invoiceproduct'''

    

    return render(request, 'voucher/created_voucher.html', context)


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


def voucher_template(request):
    paragraphs = ['first paragraph', 'second paragraph', 'third paragraph']
    


    context = {}
    if request.method == 'POST':
        
   
        context['noofadults']=request.POST.get('noofadults')
        context['noofchildren'] = request.POST.get('noofchildren')
        context['infants']= request.POST.get('infants')
        context['age']= request.POST.get('age')
        context['babycot']= request.POST.get('babycot')
        context['date']= date_parser.parse(request.POST.get('date'))
        context['name']= request.POST.get('name')
        context['packs']=request.POST.getlist('pack')
        context['lodgename']= request.POST.get('lodgename')

        
       
      

    html_string = render_to_string('voucher/voucher_template.html', context)
    html = HTML(string=html_string, base_url=request.build_absolute_uri())
    doc = html.render()
    pdf =doc.write_pdf()
    

    
   
    response = HttpResponse(pdf, content_type='application/pdf')
    #response['Content-Disposition'] = 'attachment; filename="mypdf.pdf"'
    return response

    

