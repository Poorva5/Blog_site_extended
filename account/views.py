from multiprocessing.spawn import old_main_modules
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import authenticate,logout,login
from django.shortcuts import redirect, render
from .forms import RegistrationForm, LoginForm
from blog.models import Post, UserData


def home(request):
    context = {}
    data = Post.objects.all()
    context['posts'] = data
    return render(request, "base.html", context )


def registration_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            new_user = authenticate(
                phone = form.cleaned_data['phone'],
                password = form.cleaned_data['password1']
            )
            login(request, new_user)
            return redirect('blog:home')
        
        else:
            print(request.POST, form.errors)
            form = RegistrationForm()
            return render(request, 'account/register.html', {'form': form})
    
    else:
        form = RegistrationForm()
        return render(request, 'account/register.html', {'form': form})


def login_view(request):
    context = {}
    user = request.user
    if user.is_authenticated:
        print("user authenticated")
        return redirect("blog:home")
    if request.POST:
        form = LoginForm(request.POST)
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        user = authenticate(phone=phone, password=password)
        if user:
            login(request, user)
            messages.success(request, "Logged In")
            return redirect("blog:home")
        else:
            print(request.POST, form.errors)
            return render(request, 'account/login.html', {'login_form': form})

    else:
        form = LoginForm()
        context['login_form'] = form
        return render(request, "account/login.html", context)


def logout_view(request):
    logout(request)
    messages.success(request, "Logged Out")
    return render(request, "account/logout.html")

def profile_page(request, phone):
    user = UserData.objects.get(phone=phone)
    return render(request, 'account/profile.html', {"user": user})


