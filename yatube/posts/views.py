from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.conf import settings


from .forms import CommentForm, PostForm
from .models import Group, Follow, Post


def index(request):
    template = 'posts/index.html'
    posts = Post.objects.all()
    paginator = Paginator(posts, settings.POST_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    title = 'Последние обновления на сайте'
    context = {
        'page_obj': page_obj,
        'title': title,
        'page_number': page_number,
    }
    return render(request, template, context)


def group_posts(request, slug):
    template = 'posts/group_list.html'
    group = get_object_or_404(Group, slug=slug)
    posts = group.group_label.all()
    paginator = Paginator(posts, settings.POST_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    title = f'{group}'
    context = {
        'group': group,
        'page_obj': page_obj,
        'title': title,
    }
    return render(request, template, context)


User = get_user_model()


def profile(request, username):
    template = 'posts/profile.html'
    user = User.objects.get(username=username)
    user_fn = user.first_name + ' ' + user.last_name
    posts = Post.objects.filter(author=user)
    paginator = Paginator(posts, settings.POST_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    title = f'{username} профайл пользователя'
    if request.user.username:
        current_user = request.user
        if Follow.objects.filter(user=request.user, author=user).exists():
            following = True
        else:
            following = False
        context = {
            'page_obj': page_obj,
            'title': title,
            'posts': posts,
            'author': user,
            'user_fn': user_fn,
            'current_user': current_user.username,
            'following': following,
        }
    else:
        context = {
            'page_obj': page_obj,
            'title': title,
            'posts': posts,
            'author': user,
            'user': user_fn,
        }
    return render(request, template, context)


def post_detail(request, post_id):
    template = 'posts/post_detail.html'
    post = get_object_or_404(Post, pk=post_id)
    current_user = User.objects.get(username=post.author)
    posts = Post.objects.filter(author=current_user)
    title = f'Пост {post.text[:30]}'
    comment_form = CommentForm(request.POST or None)
    comments = post.comments.all()
    context = {
        'post': post,
        'title': title,
        'posts': posts,
        'user': request.user,
        'comment_form': comment_form,
        'comments': comments,
    }
    return render(request, template, context)


@login_required
def post_create(request):
    template = 'posts/create_post.html'
    title = 'Добавить запись'
    form = PostForm(request.POST or None)
    context = {
        'form': form,
        'title': title,
    }
    if request.method == 'POST' and form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        form.save()
        return redirect('posts:profile', request.user)
    return render(request, template, context)


def post_edit(request, post_id):
    if request.method == 'GET':
        post = get_object_or_404(Post, pk=post_id)

        if post.author != request.user:
            return redirect('posts:post_detail', post_id=post.id)

        form = PostForm(instance=post)
        template = 'posts/update_post.html'
        context = {
            'form': form,
            'title': 'Редактировать пост',
            'post': post,
            'is_edit': True,
        }
        return render(request, template, context)
    if request.method == 'POST':
        post = get_object_or_404(Post, pk=post_id)
        form = PostForm(
            request.POST,
            files=request.FILES or None,
            instance=post
        )

        if form.is_valid():
            form.save()
        return redirect('posts:post_detail', post_id)


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('posts:post_detail', post_id=post_id)


@login_required
def follow_index(request):
    list_author = [a.author for a in Follow.objects.filter(user=request.user)]
    feed = Post.objects.filter(author__in=list_author).order_by('-pub_date')
    paginator = Paginator(feed, settings.POST_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    title = f'Подписки пользователя {request.user}'
    context = {
        'page_obj': page_obj,
        'title': title,
    }
    return render(request, 'posts/follow.html', context)


@login_required
def profile_follow(request, username):
    author = get_object_or_404(User, username=username)
    if not Follow.objects.filter(
        user=request.user, author=author).exists() and \
            author != request.user:
        Follow.objects.create(
            user=request.user,
            author=author)
    return redirect('posts:profile', username=author.username)


@login_required
def profile_unfollow(request, username):
    author = get_object_or_404(User, username=username)
    Follow.objects.get(
        user=request.user,
        author=author).delete()
    return redirect('posts:profile', username=author.username)
