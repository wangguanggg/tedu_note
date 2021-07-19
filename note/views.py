from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .models import Note
from user.models import User
import csv
def check_login(fn):
    def wrap(request, *args, **kwargs):
        if 'username' not in request.session or 'uid' not in request.session:
            c_username = request.COOKIES.get("username")
            c_uid = request.COOKIES.get("uid")
            if not c_username or not c_uid:
                return HttpResponseRedirect("/user/login")
            else:
                request.session['username'] = c_username
                request.session['uid'] = c_uid
        return fn(request, *args, **kwargs)
    return wrap



# Create your views here.
@check_login
def add_note(request):
    if request.method == 'GET':
        return render(request, "note/add.html")
    elif request.method == 'POST':
        uid = request.session['uid']
        title = request.POST['title']
        content = request.POST['content']
        Note.objects.create(title=title, content=content, user_id=uid)
        return HttpResponse("添加笔记成功")

@check_login
def all_view(request):
    notes = Note.objects.filter(user_id=request.session['uid'])
    page_num = request.GET.get('page', 1)
    paginator = Paginator(notes, 2)
    c_page = paginator.page(int(page_num))
    return render(request, "note/all.html", {"notes": c_page, "c_pagenum": int(page_num), "paginator": paginator})

@check_login
def delete_view(request):
    id = request.GET['id']
    note = Note.objects.get(id=id)
    note.delete()
    return HttpResponseRedirect("/note/all")

@check_login
def update_view(request):
    if request.method == 'GET':
        id = request.GET['id']
        note = Note.objects.get(id=id)
        return render(request, "note/update.html", {"note": note})
    elif request.method == 'POST':
        id = request.POST['id']
        title = request.POST['title']
        content = request.POST['content']
        # note = Note.objects.get(id=id)
        # note.title = title
        # note.content = content
        # note.save()
        Note.objects.filter(id=id).update(title=title, content=content)
        return HttpResponseRedirect("/note/all")
    else:
        raise NotImplementedError("无方法")

@check_login
def download_view(request):
    id = request.session['uid']
    user = User.objects.get(id=id)
    notes = Note.objects.filter(user=user)
    resp = HttpResponse(content_type="text/csv")
    resp['Content-disposition'] = 'attachment;filename="mybook.csv"'
    writer = csv.writer(resp)
    writer.writerow(['id', 'title', 'content', 'created_time', 'update_time'])
    for i in notes:
        writer.writerow(([i.id, i.title, i.content, i.created_time, i.update_time]))
    return resp

@check_login
def downpage_view(request):
    c_page = request.GET.get("page", 1)
    notes = Note.objects.filter(user_id=request.session['uid'])
    paginator = Paginator(notes, 2)
    c_notes = paginator.page(int(c_page))
    resp = HttpResponse(content_type="text/csv")
    resp['Content-disposition'] = 'attachment;filename="notes-page-%s.csv"' % c_page
    writer = csv.writer(resp)
    writer.writerow(['id', 'title', 'content', 'created_time', 'update_time'])
    for i in c_notes:
        writer.writerow(([i.id, i.title, i.content, i.created_time, i.update_time]))
    return resp