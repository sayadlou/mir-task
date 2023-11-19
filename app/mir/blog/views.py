from django.views.generic import ListView, DetailView

from .models import Post


class ArticleListView(ListView):
    """
    List View for Articles of blog
    """
    model = Post
    paginate_by = 5

    def get_queryset(self):
        # override default queryset for show only online post
        return self.model.get_online_posts()


class ArticleDetailView(DetailView):

    model = Post
