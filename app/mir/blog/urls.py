from django.urls import path

from .views import ArticleListView, ArticleDetailView

urlpatterns = [
    path("articles", ArticleListView.as_view(), name="article_list"),
    path("article/<int:id>/<str:slug>", ArticleDetailView.as_view(), name="article"),

]
