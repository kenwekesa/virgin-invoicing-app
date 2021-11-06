from django.core.mail import EmailMessage
from django.conf import settings



def emailInvoiceClient(file,to_email, from_client, filename):
    from_email = settings.EMAIL_HOST_USER
    subject = 'Virgin Africa Safaris Ltd Notification'
    body = 'Good day, Please find attached invoice from {} for your immediate attention. regards, virgin Africa'.format(from_client)

    message = EmailMessage(subject, body, from_email, [to_email])
   # message.attach_file(filepath)
    message.attach(filename+".pdf", file, "application/pdf")
    message.send()