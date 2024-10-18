# blog/views.py
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Blog
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.contrib.postgres.search import TrigramSimilarity
from django.core.mail import send_mail
from .models import Comment
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.html import strip_tags



def blog_list(request):
    query = request.GET.get('q')
    if query:
        blogs = Blog.objects.filter(title__icontains=query).order_by('-created_at')
    else:
        blogs = Blog.objects.all().order_by('-created_at')

    paginator = Paginator(blogs, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'blog/blog_list.html', {'page_obj': page_obj, 'query': query, 'total_blogs': blogs.count()})

def blog_detail(request, slug):
    blog = get_object_or_404(Blog, slug=slug)
    return render(request, 'blog/blog_detail.html', {'blog': blog})


def blog_search(request):
    query = request.GET.get('q')
    if query:
        vector = SearchVector('title', 'content')
        search_query = SearchQuery(query)
        blogs = Blog.objects.annotate(rank=SearchRank(vector, search_query)).filter(rank__gte=0.3).order_by('-rank')
    else:
        blogs = Blog.objects.all().order_by('-created_at')
    paginator = Paginator(blogs, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog/blog_list.html', {'page_obj': page_obj})


def blog_search_trigram(request):
    query = request.GET.get('q')
    if query:
        blogs = Blog.objects.annotate(similarity=TrigramSimilarity('title', query)).filter(similarity__gt=0.1).order_by('-similarity')
    else:
        blogs = Blog.objects.all().order_by('-created_at')
    paginator = Paginator(blogs, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog/blog_list.html', {'page_obj': page_obj})


from django.shortcuts import get_object_or_404
from .models import Comment
from django.http import HttpResponseRedirect

def add_comment(request, slug):
    blog = get_object_or_404(Blog, slug=slug)
    if request.method == "POST":
        content = request.POST.get('content')
        if content:
            comment = Comment.objects.create(blog=blog, user=request.user, content=content)
            return JsonResponse({
                'success': True,
                'commentId': comment.id,
                'username': comment.user.username,
                'content': comment.content,
                'likes': comment.likes.count(),
                'dislikes': comment.dislikes.count(),
            })
        else:
            return JsonResponse({'success': False})
    return JsonResponse({'success': False})

def like_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user in comment.likes.all():
        comment.likes.remove(request.user)
    else:
        comment.likes.add(request.user)
    return HttpResponseRedirect(comment.blog.get_absolute_url())

def dislike_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user in comment.dislikes.all():
        comment.dislikes.remove(request.user)
    else:
        comment.dislikes.add(request.user)
    return HttpResponseRedirect(comment.blog.get_absolute_url())


def share_blog(request, slug):
    blog = get_object_or_404(Blog, slug=slug)
    if request.method == 'POST':
        email = request.POST.get('email')
        plain_text_content = strip_tags(blog.content)

        send_mail(
            f'Read this Blog: {blog.title}',
            plain_text_content,
            'from@example.com',
            [email],
            fail_silently=False,
        )
        return render(request, 'blog/shared.html', {'blog': blog, 'email': email})
    return render(request, 'blog/share.html', {'blog': blog})

