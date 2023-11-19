from django.views.generic import ListView, DetailView

from .models import Post


class ArticleListView(ListView):
    model = Post
    # template_name = 'blog/index.html'
    paginate_by = 5

    def get_queryset(self):
        return self.model.get_online_posts()


class ArticleDetailView(DetailView):
    model = Post

