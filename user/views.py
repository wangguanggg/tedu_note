from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .models import User
import hashlib

# Create your views here.
def reg_view(request):
    if request.method == 'GET':
        return render(request, "user/register.html")
    elif request.method == 'POST':
        username = request.POST['username']
        password_1 = request.POST['password_1']
        password_2 = request.POST['password_2']
        m = hashlib.md5()
        m.update(password_1.encode())
        password_m = m.hexdigest()

        if password_1 != password_2:
            return HttpResponse("两次密码输入不一致")
        old_users = User.objects.filter(username=username)
        if username:
            if old_users:
                return HttpResponse("用户名已注册")
        else:
            return HttpResponse('用户名不能为空')
        try:
            user = User.objects.create(username=username, password=password_m)
        except Exception as e:
            print("用户名已注册")
        request.session['username'] = user.username
        request.session['uid'] = user.id
        return HttpResponseRedirect("/index")

def login_view(request):
    if request.method == 'GET':
        if request.session.get("username") and request.session.get("uid"):
            return HttpResponseRedirect("/index")
        username =  request.COOKIES.get("username")
        uid = request.COOKIES.get("uid")
        if username and uid:
            request.session['username'] = username
            request.session['uid'] = uid
            return HttpResponseRedirect("/index")
        return render(request, "user/login.html")
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = User.objects.get(username=username)
        except Exception as e:
            print("用户名未查到")
            return HttpResponse("用户名或密码错误")
        m = hashlib.md5()
        m.update(password.encode())
        password_m = m.hexdigest()
        if user.password != password_m:
            print("密码错误")
            return HttpResponse('用户名或密码错误')

        request.session['username'] = username
        request.session['uid'] = user.id
        resp = HttpResponseRedirect("/index")
        if 'remember' in request.POST:
            resp.set_cookie("username", username, 3600 * 24 * 3)
            resp.set_cookie("uid", user.id, 3600 * 24 * 3)
        return resp

def logout_view(request):
    if 'username' in request.session:
        del request.session['username']
    if 'uid' in request.session:
        del request.session['uid']

    resp = HttpResponseRedirect('/index')
    if 'username' in request.COOKIES:
        resp.delete_cookie("username")
    if 'uid' in request.COOKIES:
        resp.delete_cookie("uid")
    return resp