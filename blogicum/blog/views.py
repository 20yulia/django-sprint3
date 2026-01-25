from django.shortcuts import get_object_or_404, render

from .models import Category, Post

POSTS_LIMIT = 5


def index(request):
    post_list = Post.objects.published()[:POSTS_LIMIT]
    return render(request, 'blog/index.html', {'post_list': post_list})


def category_posts(request, slug):
    category = get_object_or_404(
        Category,
        slug=slug,
        is_published=True,
    )

    post_list = Post.objects.published().filter(category=category)

    return render(
        request,
        'blog/category.html',
        {
            'category': category,
            'post_list': post_list,
        },
    )


def post_detail(request, post_id):
    post = get_object_or_404(
        Post.objects.published(),
        pk=post_id,
    )
    return render(request, 'blog/detail.html', {'post': post})
