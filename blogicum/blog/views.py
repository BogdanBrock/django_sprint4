from datetime import datetime

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import (
    ListView, CreateView, UpdateView, DetailView, DeleteView
)

from .forms import PostForm, CommentForm, UserEditForm
from .models import Post, Category, Comment


User = get_user_model()


def query_set():
    return Post.objects.select_related(
        'category',
        'location',
        'author'
    )


SELECT_LIMIT = 10


class IndexListView(ListView):
    """Отображаем на главной странице список объектов из базы данных"""

    template_name = 'blog/index.html'
    paginate_by = SELECT_LIMIT

    def get_queryset(self):
        return Post.objects.filter(
            is_published=True,
            category__is_published=True,
            pub_date__lte=datetime.now()
        ).order_by('-pub_date')


class PostDetailView(DetailView):
    """Отображаем отдельный пост"""

    model = Post
    template_name = 'blog/detail.html'
    pk_url_kwarg = 'post_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = get_object_or_404(
            query_set().filter(
                pk=self.kwargs['post_id'],
            )
        )
        if post.author != self.request.user:
            post = get_object_or_404(
                query_set().filter(
                    pk=self.kwargs['post_id'],
                    category__is_published=True,
                    is_published=True,
                    pub_date__lte=datetime.now(),
                )
            )
        form = CommentForm()
        comments = post.comments.select_related('author').order_by(
            'created_at'
        )
        context.update({'post': post, 'form': form, 'comments': comments})
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    """Создание поста одного из пользователей"""

    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:profile', kwargs={'username': self.request.user})


class PostUpdateView(LoginRequiredMixin, UpdateView):
    """Редактирование поста"""

    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'
    pk_url_kwarg = 'post_id'

    def dispatch(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.author != self.request.user:
            return redirect('blog:post_id', post_id=self.kwargs['post_id'])
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('blog:post_id', kwargs={'post_id': self.object.pk})


class PostDeleteView(LoginRequiredMixin, DeleteView):
    """Удаление поста"""

    model = Post
    template_name = 'blog/create.html'
    pk_url_kwarg = 'post_id'

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.author == self.request.user:
            response = super().delete(request, *args, **kwargs)
        else:
            response = HttpResponseRedirect(reverse('blog:index'))
        return response

    def get_success_url(self):
        return reverse('blog:index')


class CategoryPostsListView(ListView):
    """Отображение категорий, которые связаны с разными постами"""

    model = Post
    template_name = 'blog/category.html'
    paginate_by = SELECT_LIMIT

    def get_queryset(self):
        post_list = query_set().filter(
            category__slug=self.kwargs['category_slug'],
            is_published=True,
            category__is_published=True,
            pub_date__lte=datetime.now()
        ).order_by('-pub_date')
        return post_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = get_object_or_404(
            Category.objects.values(
                'title',
                'description'
            ).filter(
                slug=self.kwargs['category_slug'],
                is_published=True,
            )
        )
        context['category'] = category
        return context


class CommentCreateView(LoginRequiredMixin, CreateView):
    """Можно создать комментарий к посту"""

    model = Post
    form_class = CommentForm
    template_name = 'blog/detail.html'
    pk_url_kwarg = 'post_id'

    def form_valid(self, form):
        instance = self.get_object()
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.post = instance
        self.object.save()
        return super().form_valid(form)

    def get_success_url(self):
        instance = self.get_object()
        return reverse('blog:post_id', kwargs={'post_id': instance.pk})


class CommentUpdateView(LoginRequiredMixin, UpdateView):
    """Возможность редактирования комментария"""

    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'comment_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comment = get_object_or_404(Comment, pk=self.kwargs['comment_id'])
        context.update({'comment': comment})
        return context

    def dispatch(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.author == self.request.user:
            return super().dispatch(request, *args, **kwargs)
        else:
            response = HttpResponseRedirect(reverse(
                'blog:post_id', kwargs={'post_id': instance.pk}
            ))
        return response

    def get_success_url(self):
        instance = self.get_object()
        return reverse('blog:post_id', kwargs={'post_id': instance.pk})


class CommentDeleteView(LoginRequiredMixin, DeleteView):
    """Возможность удалить комментарий"""

    model = Comment
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'comment_id'

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.author == self.request.user:
            response = super(). delete(request, *args, **kwargs)
        else:
            response = HttpResponseRedirect(reverse(
                'blog:post_id', kwargs={'post_id': instance.pk}
            ))
        return response

    def get_success_url(self):
        instance = self.get_object()
        return reverse('blog:post_id', kwargs={'post_id': instance.pk})


class ProfileListView(ListView):
    """Отображение профиля зарегистрированного пользователя"""

    template_name = 'blog/profile.html'
    paginate_by = SELECT_LIMIT

    def get_queryset(self):
        profile = get_object_or_404(User, username=self.kwargs['username'])
        if self.kwargs['username'] == self.request.user.username:
            post = query_set().filter(author=profile).order_by('-pub_date')
        else:
            post = query_set().filter(
                author=profile,
                is_published=True,
                pub_date__lte=datetime.now(),
                category__is_published=True
            ).order_by('-pub_date')
        return post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = get_object_or_404(User, username=self.kwargs['username'])
        context['profile'] = profile
        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """Редактирование профиля"""

    form_class = UserEditForm
    template_name = 'blog/user.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse('blog:profile', kwargs={'username': self.request.user})
