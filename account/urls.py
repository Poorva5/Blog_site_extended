from django.urls import path
from account.views import  registration_view, home, login_view, logout_view, profile_page

urlpatterns = [ 
    path('register/' , registration_view, name="signup"),
    path('logout/', logout_view, name = "logout"),
    path('login/', login_view, name="login"),
    path('home/', home, name="home"),
    path("user/<phone>/", profile_page, name="profile"),
]