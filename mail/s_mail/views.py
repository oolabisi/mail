from django.conf.global_settings import EMAIL_HOST_USER
from django.core.mail import send_mail
from django.shortcuts import render


# Create your views here.
from . import forms


def subscribe(request):
    sub = forms.Subscribe()
    if request.method == 'POST':
        sub = forms.Subscribe(request.POST)
        subject = 'Welcome to Grand Zone'
        message = 'We are here to serve you better!'
        recipient = str(sub['Email'].value())
        send_mail(subject,
                  message, EMAIL_HOST_USER, [recipient], fail_silently=False)
        return render(request, 's_mail/success.html', {'recipient': recipient})
    return render(request, 's_mail/index.html', {'form': sub})
