from django.shortcuts import get_object_or_404, render
from django.core.mail import send_mail
from .models import Post
from .forms import EmailPostForm

# Create your views here.
def post_list(request):
    """Retreive all Published Posts"""
    posts = Post.objects.filter(status=Post.Status.PUBLISHED)
    return render(request, 'aviblog/post_list.html', {'posts': posts})

def post_detail(request, post):
    """Retreive a single Post"""
    post = get_object_or_404(Post, slug=post, status=Post.Status.PUBLISHED)
    return render(request, 'aviblog/post_detail.html', {'post': post})

def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    sent = False
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri( post.get_absolute_url)
            subject = (f"{cd['name']} ({cd['email']}) " f"recommends you read {post.title}" ) 
            message = ( f"Read {post.title} at {post_url}\n\n"f"{cd['name']}\'s comments: {cd['comments']}" ) 
            send_mail(subject=subject, message=message, from_email=None, recipient_list=[cd['to']] ) 
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'aviblog/post_share.html', {'post': post, 'form': form, 'sent':sent})
