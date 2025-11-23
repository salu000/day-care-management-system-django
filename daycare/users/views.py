from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

def Index(request):
    return render(request, 'login.html')

def Login(request):
    if request.method == "POST":
        uname = request.POST.get('username')
        passw = request.POST.get('password')
        user = authenticate(request, username=uname, password=passw)
        if user is not None:
            login(request, user)
            return redirect('dashboard:index')  # redirect to dashboard
        else:
            # Pass error to the same login page
            return render(request, 'login.html', context={'error': "Incorrect Username or Password"})
    return redirect('users:login')


def Logout(request):
    return redirect('users:login')

def users_list(request):
    """Renders the list view for all users."""
    return render(request, 'users/users_list.html')