from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils.text import slugify
from model_bakery import baker

from .models import Post

User = get_user_model()


# Create your tests here.


class PostModelTest(TestCase):

    def setUp(self):
        # Create a user for testing
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Create a sample posts
        self.post_online_1 = baker.make(Post, owner=self.user, status=Post.PostStatus.ONLINE)
        self.post_online_2 = Post.objects.create(
            title='Test Post',
            slug='test-post',
            content='This is a test post content.',
            owner=self.user,
            status=Post.PostStatus.ONLINE,
        )
        self.post_offline_1 = baker.make(Post, owner=self.user, status=Post.PostStatus.OFFLINE)
        self.post_offline_2 = baker.make(Post, owner=self.user, status=Post.PostStatus.OFFLINE)

    def test_post_creation(self):
        # test the creation of a post
        self.assertEqual(self.post_online_2.title, 'Test Post')
        self.assertEqual(self.post_online_2.content, 'This is a test post content.')
        self.assertEqual(self.post_online_2.owner, self.user)
        self.assertEqual(self.post_online_2.status, Post.PostStatus.ONLINE)
        self.assertIsNotNone(self.post_online_2.publication_datetime)
        self.assertEqual(str(self.post_online_2), 'Test Post')
        self.assertEqual(self.post_online_2.slug, 'test-post')

    def test_get_online_post(self):
        # test for get_online_posts class method
        online_posts = Post.get_online_posts()
        self.assertIn(self.post_online_2, online_posts)
        self.assertEqual(len(online_posts), 2)

    def test_get_absolute_url(self):
        url = self.post_online_2.get_absolute_url()
        expected_url = reverse('article', kwargs={'slug': self.post_online_2.slug, 'id': self.post_online_2.id})
        self.assertEqual(url, expected_url)

    def test_is_post_offline(self):
        self.assertFalse(self.post_online_1.is_post_offline())
        self.assertTrue(self.post_offline_1.is_post_offline())


class ArticleListViewTest(TestCase):

    def setUp(self):
        # Create a user for testing
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Create online and offline posts for testing
        self.online_post = Post.objects.create(
            title='Online Test Post',
            slug=slugify('Online Test Post'),
            content='This is an online test post content.',
            owner=self.user,
            status=Post.PostStatus.ONLINE,
        )
        self.offline_post = Post.objects.create(
            title='Offline Test Post',
            slug=slugify('Offline Test Post'),
            content='This is an offline test post content.',
            owner=self.user,
            status=Post.PostStatus.OFFLINE,
        )

    def test_article_list_view(self):
        url = reverse('article_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Online Test Post')
        self.assertNotContains(response, 'Offline Test Post')
        self.assertTemplateUsed(response, 'blog/post_list.html')

    def test_pagination(self):
        # Create additional online posts to exceed paginate_by value
        for i in range(8):
            Post.objects.create(
                title=f'Post {i}',
                slug=slugify(f'Post {i}'),
                content=f'This is test post content {i}.',
                owner=self.user,
                status=Post.PostStatus.ONLINE,
            )

        url = reverse('article_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post_list.html')
        self.assertEqual(len(response.context['post_list']), 5)


class ArticleDetailViewTest(TestCase):

    def setUp(self):
        # Create a user for testing
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Create a sample post for testing
        self.post = Post.objects.create(
            title='Test Post',
            slug=slugify('Test Post'),
            content='This is a test post content.',
            owner=self.user,
            status=Post.PostStatus.ONLINE,
        )

    def test_article_detail_view(self):
        url = reverse('article', kwargs={'slug': self.post.slug, 'id': self.post.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Post')
        self.assertContains(response, 'This is a test post content.')
        self.assertTemplateUsed(response, 'blog/post_detail.html')
