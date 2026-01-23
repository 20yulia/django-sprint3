from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from .models import Category, Post

POSTS_LIMIT = 5


def index(request):
    now = timezone.now()
    post_list = (
        Post.objects
        .select_related('category', 'location', 'author')
        .filter(
            is_published=True,
            pub_date__lte=now,
            category__is_published=True,
        )
        .order_by('-pub_date')[:POSTS_LIMIT]
    )
    return render(request, 'blog/index.html', {'post_list': post_list})


def category_posts(request, slug):
    category = get_object_or_404(Category, slug=slug, is_published=True)
    now = timezone.now()
    post_list = (
        Post.objects
        .select_related('category', 'location', 'author')
        .filter(
            category=category,
            is_published=True,
            pub_date__lte=now,
        )
        .order_by('-pub_date')
    )
    return render(
        request,
        'blog/category.html',
        {'category': category, 'post_list': post_list},
    )


def post_detail(request, post_id):
    now = timezone.now()
    post = get_object_or_404(
        Post.objects.select_related('category', 'location', 'author'),
        pk=post_id,
        is_published=True,
        pub_date__lte=now,
        category__is_published=True,
    )
    return render(request, 'blog/detail.html', {'post': post})
