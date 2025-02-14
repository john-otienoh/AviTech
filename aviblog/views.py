from django.shortcuts import get_object_or_404, render, redirect
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
from .models import Post, Comment, Profile
from .forms import EmailPostForm, CommentForm
from django.utils import timezone
from taggit.models import Tag
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.
def post_list(request, tag_slug=None):
    """Retreive all Published Posts"""
    posts = Post.objects.filter(status=Post.Status.PUBLISHED)
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])   
    return render(request, 'aviblog/post_list.html', {'posts': posts, 'tag': tag})

def post_detail(request, post):
    """Retreive a single Post"""
    post = get_object_or_404(Post, slug=post, status=Post.Status.PUBLISHED)
    comments = post.comments.filter(active=True)
    form = CommentForm
    return render(request, 'aviblog/post_detail.html', {'post': post, 'comments': comments, 'form': form})

@login_required
def post_new(request):
    "Create New Post"
    if request.method == 'POST':
        title = request.POST.get('title')
        status = request.POST.get('status', Post.Status.DRAFT)
        body = request.POST.get('body')
        author = request.user
        post = Post(
            title=title,
            status=status,
            body=body,
            publish=timezone.now(),
            author=author,
        )
        post.save()
        return redirect('aviblog:post_list')
    choices  = Post.Status.choices
    return render(request, 'aviblog/post_new.html', {'choices': choices})

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

@require_POST
@login_required
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    comment = None
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
    return render(request, 'aviblog/comment.html', {'post': post, 'form': form, 'comment': comment})

def search(request):
    if request.method == "POST":
        searched = request.POST['Search']
        posts = Post.objects.filter(title__contains=searched)
        return render(request, "aviblog/search.html", {'searched':searched, 'posts':posts})
    else:
        return render(request, "aviblog/search.html", {})
    
def delete(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.user == post.author:
        post.delete()
    
    return redirect('aviblog:post_list')

def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        image = request.POST.get('profile')

        user_data_has_error = False
        if User.objects.filter(username=username).exists():
            user_data_has_error = True
            # messages.error(request, "Username Already Exists")

        if User.objects.filter(email=email).exists():
            user_data_has_error = True
            # messages.error(request, "Email Already Exists")

        if len(password) < 8:
            user_data_has_error = True
            # messages.error(request, "Password must be atleast 8 Characters")


        if user_data_has_error:
            return redirect('aviblog:register')
        else:
            new_user = User.objects.create_user(
                email=email,
                username=username,
                password=password,
            )
            Profile.objects.create(user=new_user, photo=image)
            # messages.success(request, "Account created successfully, Login Now")
            return redirect('aviblog:login')
    return render(request, 'aviblog/register.html')
