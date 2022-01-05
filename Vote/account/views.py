from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from Tools.i18n.msgfmt import MESSAGES
from .forms import UserForm

# Create your views here.
def login(request):
    #already login
    if request.user.is_authenticated:
        return render(request, 'polls/index.html')
    
    #GET
    template = 'account/login.html'
    if request.method == 'GET':
        return render(request, template, {'nextURL':request.GET.get('next')})
    
    #POST
    username = request.POST.get('username')
    password = request.POST.get('password')
    if not username or not password:
        messages.error(request, '請填帳號密碼')
        return render(request, template)
    
    user = authenticate(username=username, password=password)
    if not user:
        messages.error(request, '帳號密碼錯誤')
        return render(request, template)
    
    #login success
    auth_login(request, user)
    nextURL = request.POST.get('nextURL')
    if nextURL:
        return redirect(nextURL)
    messages.success(request, '登入成功')
    return redirect('main:main') 

@login_required
def logout(request):
    auth_logout(request)
    messages.success(request, '登出成功!')
    return redirect('account:login')

@login_required
def register(request):
    #Need is superuser
    if not(request.user.is_superuser):
        messages.error(request,'權限不足!!')
        return redirect('main:main')    
    #GET
    if request.method == 'GET':
        template = 'account/register.html'
        form = UserForm()
        return render(request, template, locals())
    #POST
    user_form = UserForm(data=request.POST)    
    if user_form.is_valid():
        user = user_form.save()
        user.set_password(user.password)
        user.save()
        
        messages.success(request, '新增成功!!')
        return redirect('main:main')
    else:
        print(user_form.errors)
        messages.error('錯誤!!')
        return render(request, template, {'user_form':user_form})
    return render(request, template)