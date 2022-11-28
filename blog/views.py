from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.views import generic, View
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Post, Category
from .forms import CommentForm, PostForm
from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseRedirect


class PostList(generic.ListView):
    # A class based view to see the list of posts in the app
    model = Post
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'index.html'
    paginate_by = 6


class PostDetail(View):
    # Define a get function to view a post in detail
    def get(self, request, slug, *args, **kwargs):
        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.filter(approved=True).order_by("-created_on")
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True

        return render(
            request,
            "post_detail.html",
            {
                "post": post,
                "comments": comments,
                "commented": False,
                "liked": liked,
                "comment_form": CommentForm()
            },
        )

    def post(self, request, slug, *args, **kwargs):
        # Define a post function to interact with a post
        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.filter(approved=True).order_by("-created_on")
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True

        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment_form.instance.email = request.user.email
            comment_form.instance.name = request.user.username
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
        else:
            comment_form = CommentForm()

        return render(
            request,
            "post_detail.html",
            {
                "post": post,
                "comments": comments,
                "commented": True,
                "comment_form": comment_form,
                "liked": liked
            },
        ) 


class PostLike(View):
    # Define a function for post like and unlike
    def post(self, request, slug, *args, **kwargs):
        post = get_object_or_404(Post, slug=slug)

        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)

        return HttpResponseRedirect(reverse('post_detail', args=[slug]))


def category(request, slug):
    # Define a function for post category
    category = get_object_or_404(Category, slug=slug)
    posts = category.posts.filter(status=1)

    return render(request, 'category.html', {'category': category, 'posts': posts})


class PostDeleteView(DeleteView):
    # Define a function for authenticated user to delete post
    model = Post
    success_url = reverse_lazy('home')


class PostUpdateView(UpdateView):
    # Define a function for authenticated user to delete post
    model = Post
    # fields = ['title', 'content']
    success_url = reverse_lazy('home')
    form_class = PostForm
    template_name = 'edit_post.html'

    def get_initial(self):
        initial = super(PostUpdateView, self).get_initial()

        # retrieve current object
        post_object = self.get_object()

        initial['title'] = post_object.title
        initial['content'] = post_object.content
        
        return initial

    def get_object(self, *args, **kwargs):
        post = get_object_or_404(Post, pk=self.kwargs['pk'])

        return post


class PostCreateView(View):
    # Define a function for authenticated user to create post
    def get(self, request, *args, **kwargs):
        return render(
            request,
            "create_post.html",
            {
                "post_form": PostForm()
            },
        )

    def post(self, request, *args, **kwargs):

        post_form = PostForm(data=request.POST)
        if post_form.is_valid():
            post_form.instance.slug = slugify(post_form.instance.title)
            email = request.user.email
            post_form.instance.author  = User.objects.get(email = email)
            post_form.instance.status = 1
            post_form.save()
            return HttpResponseRedirect(reverse('home'))
        else:
            return render(
                request,
                "create_post.html",
                {
                    "post_form": PostForm()
                },
            )
