from multiprocessing.spawn import old_main_modules
from django.shortcuts import render
# from .models import Account
# from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import authenticate,logout,login,
from django.shortcuts import redirect, render
from .forms import RegistrationForm, LoginForm
from blog.models import Post


def home(request):
    context = {}
    data = Post.objects.all()
    context['posts'] = data
    return render(request, "blog/post/list.html", context )


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
            return redirect('home')
        
        else:
            print(request.POST, form.errors)
            form = RegistrationForm()
            return render(request, 'blog/account/register.html', {'form': form})
    
    else:
        form = RegistrationForm()
        return render(request, 'blog/account/register.html', {'form': form})


def login_view(request):
    context = {}
    user = request.user
    if user.is_authenticated:
        print("user authenticated")
        return redirect("home")
    if request.POST:
        form = LoginForm(request.POST)
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        user = authenticate(phone=phone, password=password)
        if user:
            login(request, user)
            messages.success(request, "Logged In")
            return redirect("home")
        else:
            print(request.POST, form.errors)
            return render(request, 'blog/account/login.html', {'login_form': form})
            messages.error(request, 'please Correct Below Errors')

    else:
        form = LoginForm()
        context['login_form'] = form
        return render(request, "blog/account/login.html", context)


def logout_view(request):
    logout(request)
    messages.success(request, "Logged Out")
    return render(request, "blog/account/logout.html")


