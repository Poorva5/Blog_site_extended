from django.urls import path
from .feeds import LatestPostsFeed
from blog.views import home, post_list, post_detail

app_name = 'blog'

urlpatterns = [ 
    path('home/', home, name="home"),
    path('', post_list, name='post_list'),   
    path('<slug:category_slug>/', post_list, name='blog_list_by_category'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', post_detail, name='post_detail'),
    # path('tag/<slug:tag_slug>/', views.post_list, name='post_list_by_tag' ),
    # #  path('', views.PostListView.as_view(), name= 'post_list'),
    # path('feed/', LatestPostsFeed(), name='post_feed'),
    # path('create/', create_post, name="create"),
    # path('update/<slug>/', update_post, name='update_post'),
    # path('delete/<str:slug>', post_delete.as_view(), name="post_delete"),
    # # path('comment/', AddCommentView.as_view(), name='add_comment'),
    # path('profile/<phone>/', profile_page, name="profile_page"),
]