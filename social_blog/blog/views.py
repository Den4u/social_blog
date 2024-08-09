from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView)
from django.db.models import Count
from django.urls import reverse_lazy, reverse

from .models import Category, Post, User, Comment
from .forms import PostForm, UserForm, CommentForm


class PostMixin:
    model = Post
    form_class = PostForm


class PostsListView(PostMixin, ListView):
    """Вью пост лист."""

    template_name = 'blog/index.html'
    context_object_name = 'page_obj'
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.filter(
            is_published=True,
            category__is_published=True,
            pub_date__lte=timezone.now(),
        ).annotate(comment_count=Count('comments')).order_by('-pub_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_obj'] = context['paginator'].get_page(
            self.request.GET.get('page')
        )
        return context


class PostsDetailView(PostMixin, DetailView):
    """Вью пост инфо."""

    template_name = 'blog/detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        context['form'] = CommentForm()
        comment = Comment.objects.filter(post=post)
        context['comments'] = comment
        return context


class PostsCreateView(LoginRequiredMixin, PostMixin, CreateView):
    """Вью создания поста."""

    template_name = 'blog/create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            'blog:profile',
            kwargs={'username': self.request.user}
        )


class PostUpdateView(LoginRequiredMixin, PostMixin, UpdateView):
    """Вью обновления поста."""

    template_name = 'blog/create.html'
    pk_url_kwarg = 'post_id'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = self.kwargs['post_id']
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        instance = get_object_or_404(Post, pk=kwargs['post_id'])
        if instance.author != request.user:
            return redirect('blog:post_detail', self.kwargs['post_id'])
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.object.id})


class PostDeleteView(DeleteView, PostMixin):
    """Вью удаления поста."""

    model = Post
    pk_url_kwarg = 'post_id'
    template_name = 'blog/create.html'

    def dispatch(self, request, *args, **kwargs):
        post_object = super().get_object()
        if request.user != post_object.author:
            return redirect(to='blog:index')
        self.success_url = reverse_lazy(
            viewname='blog:profile',
            kwargs={'username': request.user.username})
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(**kwargs)
        form = PostForm(instance=context_data.get('post'))
        context_data.update({'form': form})
        return context_data


class CategoryListView(ListView):
    """Вью категорий."""

    model = Category
    template_name = 'blog/category.html'
    context_object_name = 'page_obj'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = get_object_or_404(
            Category,
            slug=self.kwargs['category_slug'],
            is_published=True,
        )
        context['page_obj'] = context['paginator'].get_page(
            self.request.GET.get('page')
        )
        return context

    def get_queryset(self):
        category_slug = self.kwargs.get('category_slug')
        category = get_object_or_404(
            Category,
            slug=category_slug,
            is_published=True
        )
        return category.posts.filter(
            is_published=True,
            pub_date__lte=timezone.now()
        ).annotate(comment_count=Count('comments')).order_by('-pub_date')


def ProfileView(request, username):
    profile = get_object_or_404(User, username=username)
    posts = Post.objects.select_related('author').filter(
        author__username=username,).annotate(comment_count=Count('comments')
                                             ).order_by('-pub_date')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'profile': profile,
        'page_obj': page_obj
    }
    return render(request, 'blog/profile.html', context)


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """Вью обновления профиля."""

    model = User
    form_class = UserForm
    template_name = 'blog/user.html'
    success_url = reverse_lazy('blog:index')

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.save()
        return super().form_valid(form)


class CommentCreateView(LoginRequiredMixin, CreateView):
    """Вью создания комментариев."""

    posts = None
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'post_id'

    def dispatch(self, request, *args, **kwargs):
        self.posts = get_object_or_404(Post, pk=kwargs['post_id'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = self.posts
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:post_detail',
                       kwargs={'pk': self.posts.pk})


class CommentMixin:
    """Миксин комментариев."""

    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'comment_id'

    def dispatch(self, request, *args, **kwargs):
        instance = get_object_or_404(Comment, pk=kwargs['comment_id'])
        if instance.author != request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('blog:post_detail',
                       kwargs={"pk": self.kwargs['comment_id']})


class CommentUpdateView(LoginRequiredMixin, CommentMixin, UpdateView):
    """Вью обновления комментариев."""

    pass


class CommentDeleteView(LoginRequiredMixin, CommentMixin, DeleteView):
    """Вью удаления комментариев."""

    pass
