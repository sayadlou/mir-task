from django.http import Http404
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

    def get_object(self, queryset=None):
        # raise 404 error in case of offline post request
        obj: Post = super().get_object(queryset)
        if obj.is_post_offline():
            raise Http404()
        return obj
