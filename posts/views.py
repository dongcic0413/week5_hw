from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required

# Create your views here.

def post_list(request):
    posts = Post.objects.filter(is_published=True)
    return render(request, 'posts/list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post.objects.select_related("author"), pk=pk)
    comments = post.comments.select_related("author").all()

    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect("login")
        content = request.POST.get("content", "").strip()
        if content:
            Comment.objects.create(post=post, author=request.user, content=content)
            return redirect("post_detail", pk=post.pk)

    return render(request, "posts/detail.html", {"post": post, "comments": comments})

@login_required
def post_create(request):
    if request.method == 'POST':
        post, error = _build_post_from_request(request, Post())
        if error is None:
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)  # 성공만 redirect
        return render(request, 'posts/form.html', {'post': post, 'error': error})
    return render(request, 'posts/form.html', {'post': Post()})

@login_required
def post_update(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if not post.is_author(request.user):
        raise PermissionDenied("본인이 작성한 글만 수정할 수 있습니다.")
    if request.method == "POST":
        post, error = _build_post_from_request(request, post)
        if error is None:
            post.save()
            return redirect("post_detail", pk=post.pk)
        return render(request, "posts/form.html", {"post": post, "error": error})
    return render(request, "posts/form.html", {"post": post})


@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if not post.is_author(request.user):
        raise PermissionDenied("본인이 작성한 글만 삭제할 수 있습니다.")
    if request.method == "POST":
        post.delete()
        return redirect("post_list")
    return render(request, "posts/confirm_delete.html", {"post": post})

def _build_post_from_request(request, post):
    title = request.POST.get('title', '').strip()
    content = request.POST.get('content', '').strip()
    post.title = title
    post.content = content
    post.category = request.POST.get('category', '')
    post.is_published = 'is_published' in request.POST
    if not title or not content:
        return post, '제목과 내용은 비워둘 수 없어요.'
    return post, None
