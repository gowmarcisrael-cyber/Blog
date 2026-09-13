from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def profile(request):
    user_posts = request.user.posts.all().order_by('-created_at')
    
    published_posts = user_posts.filter(status='published')
    draft_posts = user_posts.filter(status='draft')
    
    context = {
        'published_posts': published_posts,
        'draft_posts': draft_posts,
        'total_count': user_posts.count(),
    }
    return render(request, 'account/profile.html', context)