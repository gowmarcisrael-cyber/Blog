from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpResponse
from .models import Post
from .forms import PostForm,CommentForm,ParagraphFormSet
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

# Create your views here.

def index(request):
    posts = (
        Post.objects
        .filter(status="published")
        .select_related("author", "category")
        .prefetch_related("tags", "likes","paragraphs")
    )

    return render(request, "Blog/index.html", {
        "posts": posts
    })

def add(request):
    if request.method == 'POST' and request.user.is_authenticated:
        form = PostForm(request.POST, request.FILES)
        formset = ParagraphFormSet(request.POST, request.FILES, prefix='paragraphs')
 
        if form.is_valid() and formset.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()
 
            formset.instance = post
            formset.save()
 
            return redirect('index')
 
        return render(request, "Blog/add.html", context={
            'form': form,
            'formset': formset,
        })
 
    form = PostForm()
    formset = ParagraphFormSet(prefix='paragraphs')
    return render(request, "Blog/add.html", context={
        'form': form,
        'formset': formset,
    })

def detail(request,slug):
    post = get_object_or_404(Post.objects.select_related('author','category').prefetch_related('likes','tags'),slug=slug)
    return render(request,'Blog/detail.html',context={
        'post':post
    })

def edit(request, slug):
    post = get_object_or_404(Post, slug=slug)
 
    if post.author != request.user:
        return HttpResponseForbidden("Tu ne peux pas modifier cet article.")
 
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        formset = ParagraphFormSet(request.POST, request.FILES, instance=post, prefix='paragraphs')
 
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect('post_detail', slug=post.slug)
 
        return render(request, "Blog/add.html", context={
            'form': form,
            'formset': formset,
            'post': post,
        })
 
    form = PostForm(instance=post)
    formset = ParagraphFormSet(instance=post, prefix='paragraphs')
    return render(request, "Blog/add.html", context={
        'form': form,
        'formset': formset,
        'post': post,
    })

@login_required
@require_POST
def delete_post(request,slug):
    post = get_object_or_404(Post,author=request.user,slug=slug)
    if post.cover:
        post.cover.delete()
    for paragraph in post.paragraphs.all():
        if paragraph.image:
            paragraph.image.delete()
    post.delete()
    return HttpResponse('')

@login_required
@require_POST
def change_status(request,slug):
    post = get_object_or_404(Post,slug=slug,author=request.user)
    post.status = request.POST['status']
    post.save()
    return render(request,'Blog/partials/status.html',context={
        'post':post
    })