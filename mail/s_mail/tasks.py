import string

from celery import shared_task
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.template.loader import get_template
from django.utils.crypto import get_random_string

# from .mail import settings


@shared_task
def create_random_user_accounts(total):
    for i in range(total):
        username = 'user_{}'.format(get_random_string(10, string.ascii_letters))
        email = '{}@example.com'.format(username)
        password = get_random_string(50)
        User.objects.create_user(username=username, email=email, password=password)
    return '{} random users created with success!'.format(total)

#
# @shared_task
# def send_message(subject, context, recipient_list, html_path, text_path):
#     text_ = get_template(text_path).render(context)
#     html_ = get_template(html_path).render(context)
#     from_email = settings.DEFAULT_FROM_EMAIL
#     sent = send_mail(
#         subject, text_, from_email, recipient_list,
#         html_message=html_, fail_silently=False,
#     )
#     return sent
