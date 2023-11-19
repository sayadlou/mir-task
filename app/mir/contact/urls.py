from django.urls import path
from django.views.generic import TemplateView

from .views import ContactRequestCreateView

urlpatterns = [
    path("", ContactRequestCreateView.as_view(), name="contact_us"),
    path("success", TemplateView.as_view(template_name="contact/success.html"), name="success-url"),

]
