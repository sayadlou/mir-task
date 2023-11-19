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
