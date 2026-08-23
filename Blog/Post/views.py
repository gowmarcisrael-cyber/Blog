from django.shortcuts import render, redirect,get_object_or_404
from .models import Post
from .forms import PostForm,CommentForm,ParagraphFormSet
from django.http import HttpResponseForbidden

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
    if request.method == 'POST':
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
 