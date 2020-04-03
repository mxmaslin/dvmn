from django.shortcuts import render
from django.db.models import Count, Prefetch

from blog.models import Comment, Post, Tag


def serialize_post_optimized(post):
    return {
        "title": post.title,
        "teaser_text": post.text[:200],
        "author": post.author.username,
        "comments_amount": post.comments_count,
        "image_url": post.image.url if post.image else None,
        "published_at": post.published_at,
        "slug": post.slug,
        "tags": [serialize_tag(tag) for tag in post.tags.all()],
        'first_tag_title': post.tags.all()[0].title,
    }


def serialize_tag(tag):
    return {
        'title': tag.title,
        'posts_with_tag': tag.posts_count
    }


def index(request):
    posts_with_prefetched_data = Post.objects.prefetch_related(
        'author',
        Prefetch(
            'tags',
            queryset=Tag.objects.annotate(posts_count=Count('posts'))
        )
    )

    most_popular_posts = posts_with_prefetched_data.popular().fetch_with_comments_count()[:5]

    most_fresh_posts = posts_with_prefetched_data.order_by(
        '-published_at'
    ).fetch_with_comments_count()[:5]

    most_popular_tags = Tag.objects.popular()[:5]
    context = {
        'most_popular_posts': [serialize_post_optimized(post) for post in most_popular_posts],
        'page_posts': [serialize_post_optimized(post) for post in most_fresh_posts],
        'popular_tags': [serialize_tag(tag) for tag in most_popular_tags],
    }
    return render(request, 'index.html', context)


def post_detail(request, slug):
    post = Post.objects.prefetch_related(
        Prefetch(
            'tags',
            queryset=Tag.objects.annotate(posts_count=Count('posts'))),
        Prefetch(
            'comments',
            queryset=Comment.objects.select_related('author')
        )
    ).select_related('author').get(slug=slug)

    serialized_post = {
        "title": post.title,
        "text": post.text,
        "author": post.author.username,
        "comments": post.comments.all(),
        'likes_amount': post.likes.count(),
        "image_url": post.image.url if post.image else None,
        "published_at": post.published_at,
        "slug": post.slug,
        "tags": [serialize_tag(tag) for tag in post.tags.all()],
    }

    most_popular_tags = Tag.objects.popular()[:5]

    most_popular_posts = Post.objects.prefetch_related(
        'author',
        Prefetch(
            'tags',
            queryset=Tag.objects.annotate(posts_count=Count('posts'))
        )
    ).popular().fetch_with_comments_count()[:5]

    context = {
        'post': serialized_post,
        'popular_tags': [serialize_tag(tag) for tag in most_popular_tags],
        'most_popular_posts': [
            serialize_post_optimized(post) for post in most_popular_posts
        ]
    }
    return render(request, 'post-details.html', context)


def tag_filter(request, tag_title):
    tag = Tag.objects.prefetch_related(
        Prefetch(
            'posts',
            queryset=Post.objects.annotate(comments_count=Count('comments'))
        )
    ).get(title=tag_title)
    most_popular_tags = Tag.objects.popular()[:5]

    most_popular_posts = Post.objects.prefetch_related(
        'author',
        Prefetch(
            'tags',
            queryset=Tag.objects.annotate(posts_count=Count('posts'))
        )
    ).popular().fetch_with_comments_count()[:5]

    related_posts = tag.posts.prefetch_related(
        'author',
        Prefetch(
            'tags',
            queryset=Tag.objects.annotate(posts_count=Count('posts'))
        )
    )[:20]

    context = {
        "tag": tag.title,
        'popular_tags': [serialize_tag(tag) for tag in most_popular_tags],
        "posts": [serialize_post_optimized(post) for post in related_posts],
        'most_popular_posts': [serialize_post_optimized(post) for post in most_popular_posts],
    }
    return render(request, 'posts-list.html', context)


def contacts(request):
    # позже здесь будет код для статистики заходов на эту страницу
    # и для записи фидбека
    return render(request, 'contacts.html', {})
