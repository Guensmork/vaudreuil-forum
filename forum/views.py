from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Thread, Post
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify
from django import forms
from django.core.paginator import Paginator


# Simple forms inline for now
class ThreadForm(forms.ModelForm):
    class Meta:
        model = Thread
        fields = ['title']

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content']

def forum_index(request):
    categories = Category.objects.all()
    return render(request, 'forum/index.html', {'categories': categories})

def thread_list(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    threads = category.threads.order_by('-created_at')

    paginator = Paginator(threads, 10)  # 10 threads per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'forum/thread_list.html', {
        'category': category,
        'page_obj': page_obj,
    })


def thread_detail(request, category_slug, thread_slug):
    category = get_object_or_404(Category, slug=category_slug)
    thread = get_object_or_404(Thread, category=category, slug=thread_slug)
    posts = thread.posts.order_by('created_at')

    paginator = Paginator(posts, 10)  # 10 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.author = request.user
            reply.thread = thread
            reply.save()
            return redirect('forum:thread_detail', category_slug=category_slug, thread_slug=thread_slug)
    else:
        form = PostForm()

    return render(request, 'forum/thread_detail.html', {
        'category': category,
        'thread': thread,
        'page_obj': page_obj,
        'form': form
    })


@login_required
def create_thread(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)

    if request.method == 'POST':
        thread_form = ThreadForm(request.POST)
        post_form = PostForm(request.POST)
        if thread_form.is_valid() and post_form.is_valid():
            thread = thread_form.save(commit=False)
            thread.creator = request.user
            thread.category = category
            thread.slug = slugify(thread.title)
            thread.save()

            post = post_form.save(commit=False)
            post.thread = thread
            post.author = request.user
            post.save()

            return redirect('forum:thread_detail', category_slug=category.slug, thread_slug=thread.slug)
    else:
        thread_form = ThreadForm()
        post_form = PostForm()

    return render(request, 'forum/create_thread.html', {
        'category': category,
        'thread_form': thread_form,
        'post_form': post_form
    })
