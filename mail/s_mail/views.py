from django.conf.global_settings import EMAIL_HOST_USER
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.views.generic import FormView, ListView
from .forms import GenerateRandomUserForm
from . import forms
from .tasks import create_random_user_accounts

# Create your views here.


class UsersListView(ListView):
    template_name = 's_mail/users_list.html'
    model = User


class GenerateRandomUserView(FormView):
    template_name = 's_mail/generate_random_users.html'
    form_class = GenerateRandomUserForm

    def form_valid(self, form):
        total = form.cleaned_data.get('total')
        create_random_user_accounts.delay(total)
        messages.success(self.request, 'We are generating your random users!'
                                       'Wait a moment and refresh this page')
        return redirect('users_list')


def subscribe(request):
    sub = forms.Subscribe()
    if request.method == 'POST':
        sub = forms.Subscribe(request.POST)
        subject = 'Welcome to Grand Zone'
        message = 'We are here to serve you better!'
        recipient = str(sub['email'].value())
        send_mail(subject, message, EMAIL_HOST_USER, [recipient], fail_silently=False)
        return render(request, 's_mail/success.html', {'recipient': recipient})
    return render(request, 's_mail/index.html', {'form': sub})
