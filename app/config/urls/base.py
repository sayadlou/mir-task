from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path("", TemplateView.as_view(template_name="home.html"), name="home"),
    path("blog/", include("mir.blog.urls")),
    path("contact_us/", include("mir.contact.urls")),
]
