from __future__ import unicode_literals
from django.shortcuts import render,redirect,HttpResponse
from .models import User, UserManager,Wall_Message,Comment
from django.contrib import messages
import bcrypt


def index1(request):
    return render(request, "main.html")

def index(request):
    return render(request, 'index.html')

def create_user(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        password = bcrypt.hashpw(request.POST['password'].encode(),bcrypt.gensalt()).decode()
        user=User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'],email=request.POST['email'], password= password)
        request.session['userid']= user.id
        return redirect('/success')
    
          
def login(request):
    user = User.objects.filter(email=request.POST['email'])
    if len(user) > 0:
        logged_user = user[0]
        if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
            request.session['userid'] = logged_user.id
            return redirect('/success')
        else:
            messages.error(request, 'Email and password did not match')
            
    else:
        messages.error(request, 'Email is not registered')
    return redirect('/')

def success(request):
    context = {
        'logged': User.objects.get(id=request.session['userid']),
        'wall_messages': Wall_Message.objects.all()
    }
    return render(request, 'success.html', context)

def post_mess(request):
    Wall_Message.objects.create(message=request.POST['mess'], poster=User.objects.get(id=request.session['userid']))
    return redirect('/success')

def post_comment(request, id):
    poster = User.objects.get(id=request.session['userid'])
    message = Wall_Message.objects.get(id=id)
    Comment.objects.create(comment=request.POST['comment'], poster=poster, wall_message=message)
    return redirect('/success')


def add_like(request, id):
    liked_message = Wall_Message.objects.get(id=id)
    user_liking = User.objects.get(id=request.session['userid'])
    liked_message.user_likes.add(user_liking)
    return redirect('/success')

def delete_comment(request, id):
    destroyed = Comment.objects.get(id=id)
    destroyed.delete()
    return redirect('/success')

def profile(request, id):
    context = {
        'logged1': User.objects.get(id=id),
        'user': User.objects.get(id=id)
        
    }
    return render(request, 'profile.html', context)

def log_out(request):
    request.session.clear()
    return redirect("/")


def edit_profile(request, id):
    context={
        'edit_profile': User.objects.get(id=id),
    }
    
    return render(request, 'edit_profile.html', context)

def update(request, id):
    str_id=str(id)
    edit_profile=User.objects.get(id=id)
    edit_profile.first_name=request.POST['first_name']
    edit_profile.last_name=request.POST['last_name']
    edit_profile.save()
    return redirect('/success')
        