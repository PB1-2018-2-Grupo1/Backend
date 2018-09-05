from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect

from user.forms import SignUpForm

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            """raw_password = form.cleaned_data.get('password')"""
            login(request, user)
            return redirect('home.html')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})