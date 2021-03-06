from http.client import REQUEST_URI_TOO_LONG
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment
from django.views.generic import ListView
from .forms import CommentForm, UpdatePostForm 
from taggit.models import Tag
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import DeleteView, CreateView
from account.models import UserData


from .forms import (
    PostForm
)

def home(request):
    context = {}
    data = Post.objects.all()
    context['posts'] = data
    return render(request, "blog/post/list.html", context )


def post_list(request, tag_slug=None):
    object_list = Post.published.all()
    
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tag__in=[tag])

    paginator = Paginator(object_list, 3)  #it have 3 posts in each page
    page = request.GET.get('page')  #it indicates the current page number
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    
    return render(request, 'blog/post/list.html', { 'page': page, 'posts': posts, 'tag' : tag})
    

    

def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, status='published', publish__year=year, publish__month=month, publish__day=day)
     
    comments = post.comments.filter(active=True)

    new_comment = None

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = CommentForm()

    #List of similar posts

    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]



    return render(request, 'blog/post/detail.html', {'post': post, 'comments': comments, 'new _comment' : new_comment, 'comment_form' : comment_form ,  'similar_posts': similar_posts})

class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    pagination_by = 3
    template_name = 'blog/post/list.html'

    

#create new post
def create_post(request):
    form = PostForm()
    if request.method == "POST":
        form = PostForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.author = request.user
            instance.save()
            form.save_m2m()
            messages.success(request, "Post was created successfully")
            return redirect("home")
        else:
            messages.error(request, "Post was created successfully")
            print(form.errors)
            form = PostForm()
            return render(request, "blog/post/create_post.html", {'form': form})
    context = {'form': form}
    return render(request, "blog/post/create_post.html", context)


def post_detail(request, year, month, day, post):
    item = get_object_or_404(Post , slug=post, status='published', publish__year=year, publish__month=month, publish__day=day)
    user = request.user
    context = {
        'item': item
    }
    return render(request, "blog/post/post_detail.html", context)



def update_post(request, slug):
    context = {}
    user = request.user
    post = get_object_or_404(Post, slug=slug)
    if request.method  == 'POST':
        form = UpdatePostForm(request.POST or None, request.FILES or None, instance=post)
        if form.is_valid():
            item = form.save(commit=False)
            item.save()
            context['success_message'] = "updated"
            post = item
            messages.success(request, "{} was updated".format(item.title))
            return HttpResponseRedirect(post.get_absolute_url())

    form = UpdatePostForm(initial={
        'title': post.title,
        'body' : post.body,
        'image': post.image
    })

    context['form'] = form
    return render(request, "blog/post/update_post.html", context)

class post_delete(DeleteView):
    model = Post
    template_name = 'blog/post/delete_post.html'
    success_url = reverse_lazy("home")
    success_message = "Post Deleted Successfully"


class AddCommentView(CreateView):
    model = Comment
    template_name = 'blog/post/comment_form.html'
    fields = '__all__'  


def profile_page(request, phone):
    user = UserData.objects.get(phone=phone)
    return render(request, 'blog/post/profile.html', {"user": user})
   
