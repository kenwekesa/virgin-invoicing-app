from django.core.mail import EmailMessage
from django.conf import settings



def emailInvoiceClient(file,to_email, from_client, filename):
    from_email = settings.EMAIL_HOST_USER
    subject = 'Payment Invoice'
    body = 'Good day, Please find attached invoice for your immediate action. Regards, Virgin Africa Safaris Limited'

    message = EmailMessage(subject, body, from_email, [to_email])
   # message.attach_file(filepath)
    message.attach(filename+".pdf", file, "application/pdf")
    message.send()


def emailVoucher(file,to_email, from_client, filename):
    from_email = settings.EMAIL_HOST_USER
    subject = 'Voucher'
    body = 'Good day, Please find attached voucher for your immediate action. Regards, Virgin Africa Safaris Limited'

    message = EmailMessage(subject, body, from_email, [to_email])
   # message.attach_file(filepath)
    message.attach(filename+".pdf", file, "application/pdf")
    message.send()