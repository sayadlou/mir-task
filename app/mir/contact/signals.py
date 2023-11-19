from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import ContactRequest


def send_contact_info_as_email(email_message, email_subject):
    """
    a method to send message as email to be able to mock sending the email during test,
    it has been defined in a separate function

    it would be better to use celery for sending email as a background task
    :param email_message:
    :param email_subject:
    :return:
    """
    send_mail(subject=email_subject,
              from_email="debug@mir.de",
              message=email_message,
              recipient_list=['debug@mir.de', ]
              )


@receiver(post_save, sender=ContactRequest)
def contact_request_post_save(sender, instance: ContactRequest, created, **kwargs):
    """
    a signal which triggers  after saving the post instance
    :param sender:
    :param instance:
    :param created:
    :param kwargs:
    :return:
    """
    if created:
        email_message = (f"Replay-to{instance.email}\r\n"
                         f"name : {instance.name} \r\n"
                         f"content{instance.content}")
        email_subject = f"Replay-to{instance.email}"
        send_contact_info_as_email(email_message, email_subject)
