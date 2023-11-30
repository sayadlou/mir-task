from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .models import ContactRequest


class ContactRequestCreateView(CreateView):
    """
    create view class for contact us app
    """
    model = ContactRequest  # model for save messages
    fields = (
        'email',
        'name',
        'content',
    )
    success_url = reverse_lazy('success-url')  # url for redirect in successful message page

    def form_valid(self, form):
        """
        validate email and send contact message to company email

        :param form:
        :return:
        """
        self.object = form.save()
        self._send_contact_info_as_email()
        return HttpResponseRedirect(self.get_success_url())

    def _send_contact_info_as_email(self):
        # send contact message to company email
        email_message = (f"Reply-to : {self.object.email}\r\n"
                         f"name : {self.object.name} \r\n"
                         f"content{self.object.content}")
        email_subject = f"Reply-to{self.object.email}"
        send_mail(subject=email_subject,
                  from_email="debug@mir.de",
                  message=email_message,
                  recipient_list=['debug@mir.de', ]
                  )
