from django.shortcuts import render
from django.core.mail import send_mail

from .forms import ContactForm


def index(request):
    context = { }

    return render(request,'inicio.html',context)

def about(request):

    context = { }

    return render(request, 'acerca_de.html',context)



def contact(request):

    form = ContactForm(request.POST or None)

    if form.is_valid():

        form_issue = form.cleaned_data.get('issue')
        form_email = form.cleaned_data.get('email')
        form_message = form.cleaned_data.get('message')
        form_name = form.cleaned_data.get('name')

        email_issue = 'Form de contacto'
        email_from = form_email
        email_to = ['pedroesparzaaa@gmail.com']
        email_message = '%s: %s enviado por %s' %(form_name, form_message, form_email)

        send_mail(
            email_issue,
            email_message,
            email_from,
            email_to,
            fail_silently=False,
        )

    context = { 'form' : form}

    return render(request, 'contact.html',context)