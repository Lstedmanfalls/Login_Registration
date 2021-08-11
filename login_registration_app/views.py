from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import Users
import bcrypt

def index(request): #GET REQUEST
    context = {
    "all_the_users": Users.objects.all(),
    }
    return render(request, "index.html", context)

def register(request): #POST REQUEST
    errors = Users.objects.register_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/")
    elif request.method != "POST":
        return redirect("/")
    elif request.method == "POST":
            password = request.POST['password']
            pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            user_id = Users.objects.create(first_name = request.POST["first_name"], last_name = request.POST["last_name"], email = request.POST['email'], password=pw_hash)
            request.session['user_id'] = user_id.id
    return redirect("/success")

def login(request): #POST REQUEST
    errors = Users.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/")
    user = Users.objects.filter(email=request.POST["email"])
    if user: 
        logged_user = user[0] 
        if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
            request.session["user_id"] = logged_user.id
            return redirect("/success")
        return redirect("/")
    elif request.method != "POST":
        return redirect("/")
    return redirect("/")

def success(request): #GET REQUEST
    if 'user_id' not in request.session:
        messages.error(request, "You must be logged in to view this site")
        return redirect ("/")
    else:
        this_user = Users.objects.get(id = request.session['user_id'])
        if this_user:
            messages.success(request, "Successfully registered (or logged in)")
            context = {
            "this_user": this_user
            }
            return render(request, "success.html", context)
    return redirect("/")

def logout(request): #POST REQUEST
    if request.method != "POST":
        return redirect("/")
    request.session.flush()
    return redirect("/")