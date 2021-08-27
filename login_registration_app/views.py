from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import User, UserManager
import bcrypt

def index(request): #GET REQUEST
    context = {
    "all_the_users": User.objects.all(),
    }
    return render(request, "index.html", context)

def register(request): #POST REQUEST
    errors = User.objects.register_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/")
    elif request.method != "POST":
        return redirect("/")
    elif request.method == "POST":
            password = request.POST['password']
            pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            user = User.objects.create(first_name = request.POST["first_name"], last_name = request.POST["last_name"], email = request.POST['email'], password=pw_hash)
            request.session['user_id'] = user.id
    return redirect("name_of_homepage")

def login(request): #POST REQUEST
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/")
    user = User.objects.filter(email=request.POST["email"])
    if user: 
        logged_user = user[0] 
        if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
            request.session["user_id"] = logged_user.id
            return redirect("name_of_homepage")
        return redirect("/")
    elif request.method != "POST":
        return redirect("/")
    return redirect("/")

def logout(request): #POST REQUEST
    if request.method != "POST":
        return redirect("/")
    request.session.flush()
    return redirect("/")