import imp
from django.urls import path
from django.urls.resolvers import URLPattern
from . import views
from .feeds import LatestPostsFeed
from blog.views import *
from .views import post_delete, AddCommentView, profile_page


urlpatterns = [ 
    path('', views.post_list, name='post_list'),
    path('home/', home, name="home"),
    path('tag/<slug:tag_slug>/', views.post_list, name='post_list_by_tag' ),
    #  path('', views.PostListView.as_view(), name= 'post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail, name='post_detail'),
    path('feed/', LatestPostsFeed(), name='post_feed'),
    path('create/', create_post, name="create"),
    path('update/<slug>/', update_post, name='update_post'),
    path('delete/<str:slug>', post_delete.as_view(), name="post_delete"),
    # path('comment/', AddCommentView.as_view(), name='add_comment'),
    path('profile/<phone>/', profile_page, name="profile_page"),
]