from django.shortcuts import render
from blog.models import Post
from . import forms
from . import models

# Create your views here.


def blog_index(request):
    posts = Post.objects.all().order_by('-created_on')
    context = {"posts": posts,}
    return render(request, "blog_index.html", context)


def blog_category(request, category):
    posts = Post.objects.filter(categories__name__contains=category).order_by('-created_on')
    context = {"category": category,"posts": posts}
    return render(request, "blog_category.html", context)


def blog_detail(request, pk):
    post = Post.objects.get(pk=pk)
    comments = models.Comment.objects.filter(post=post)

    form = forms.CommentForm()
    if request.method == "POST":
        form = forms.CommentForm(request.POST)
        if form.is_valid():
            comment = models.Comment(
                author=form.cleaned_data["author"],
                body=form.cleaned_data["body"],
                post=post,
            )
            comment.save()

    context = {"post": post, "comments": comments, "form": form}
    return render(request, "blog_detail.html", context)