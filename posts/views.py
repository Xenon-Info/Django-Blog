from django.core import paginator
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Post, Tag
from .forms import PostForm, ReviewForm
from .utils import search_posts, paginate_posts


def posts(request):
    posts, search_query = search_posts(request)
    custom_range, posts = paginate_posts(request, posts, 6)
    try:
        profile_request = request.user.profile
    except:
        profile_request = None
    if profile_request is None:
        context = {'posts': posts,
                   'search_query': search_query, 'custom_range': custom_range}
    else:
        message_requests = profile_request.messages.all()
        unread_count = message_requests.filter(is_read=False).count()
        context = {'posts': posts, 'search_query': search_query,
                   'custom_range': custom_range, 'unread_count': unread_count}
    return render(request, 'posts/posts.html', context)


def post(request, pk):
    post_obj = Post.objects.get(id=pk)
    form = ReviewForm()

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        review = form.save(commit=False)
        review.post = post_obj
        review.owner = request.user.profile
        review.save()

        post_obj.get_vote_count

        messages.success(request, 'Your review was successfully submitted!')
        return redirect('post', pk=post_obj.id)

    try:
        profile_request = request.user.profile
    except:
        profile_request = None

    if profile_request is None:
        context = {'post': post_obj, 'form': form}
    else:
        message_requests = profile_request.messages.all()
        unread_count = message_requests.filter(is_read=False).count()
        context = {'post': post_obj, 'form': form, 'unread_count': unread_count}

    return render(request, 'posts/single-post.html', context)


@login_required(login_url="login")
def create_post(request):
    profile = request.user.profile
    form = PostForm()

    if request.method == 'POST':
        newtags = request.POST.get('newtags').replace(',',  " ").split()
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.owner = profile
            post.save()

            for tag in newtags:
                tag, created = Tag.objects.get_or_create(name=tag)
                post.tags.add(tag)
            messages.success(request, 'New Post successfully submitted!')
            return redirect('account')
    message_requests = profile.messages.all()
    unread_count = message_requests.filter(is_read=False).count()
    context = {'form': form, 'unread_count': unread_count}
    return render(request, "posts/post_form.html", context)


@login_required(login_url="login")
def update_post(request, pk):
    profile = request.user.profile
    post = profile.post_set.get(id=pk)
    form = PostForm(instance=post)

    if request.method == 'POST':
        newtags = request.POST.get('newtags').replace(',',  " ").split()

        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save()
            for tag in newtags:
                tag, created = Tag.objects.get_or_create(name=tag)
                post.tags.add(tag)
            messages.success(request, 'Your Post was successfully updated!')
            return redirect('account')
    message_requests = profile.messages.all()
    unread_count = message_requests.filter(is_read=False).count()

    context = {'form': form, 'post': post, 'unread_count': unread_count}
    return render(request, "posts/post_form.html", context)


@login_required(login_url="login")
def delete_post(request, pk):
    profile = request.user.profile
    post = profile.post_set.get(id=pk)
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post Deleted!')
        return redirect('account')
    message_requests = profile.messages.all()
    unread_count = message_requests.filter(is_read=False).count()
    context = {'object': post, 'unread_count': unread_count}
    return render(request, 'delete_template.html', context)
