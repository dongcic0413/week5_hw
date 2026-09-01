from django.shortcuts import render, get_object_or_404, redirect
from .models import Post

# Create your views here.

def post_list(request):
    posts = Post.objects.filter(is_published = True)
    return render(request, 'posts/list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk = pk)
    return render(request, 'posts/detail.html', {'post': post})

def _build_post_from_request(request, post):
    title = request.POST.get('title', '').strip()
    content = request.POST.get('content', '').strip()
    post.title = title
    post.content = content
    post.category = request.POST.get('category', '')
    post.is_published = 'is_published' in request.POST
    if not title or not content:
        return post, '제목과 내용은 비워돌 수 없어요.'
    return post, None

def post_create(request):
    if request.method == 'POST':
        post, error = _build_post_from_request(request, Post())
        if error is None:
            post.save()
            return redirect('post_detail', pk = post.pk)
        return render(request, 'posts/form.html', {'post': post, 'error': error})
    return render(request, 'posts/form.html', {'post': Post()})

def post_update(request, pk):
    post = get_object_or_404(Post, pk = pk)
    if request.method == 'POST':
        post, error = _build_post_from_request(request, post)
        if error is None:
            post.save()
            return redirect('post_detail', pk = post.pk)
        return render(request, 'posts/form.html', {'post': post, 'error': error})
    return render(request, 'posts/formm.html', {'post': post})

def post_delete(request, pk):
    post = get_object_or_404(Post, pk = pk)
    if request.method == 'POST':
        post.delete()
        return redirect('post_list')
    return render(request, 'posts/confirm_delete.html', {post: post})
