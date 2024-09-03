from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Post, Reply
import joblib
from django.http import JsonResponse
import numpy as np

model = joblib.load("questionaires/models/models.joblib")

# Create your views here.
def home(request):
    return render(request, "home.html")

def createAccount(request):
    if request.method == "POST":
        email = request.POST["email"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]
        if password1 != password2:
            return redirect("home")
        else:
            myUser = User.objects.create_user(username=email.split("@")[0], email=email, password=password1)
            myUser.save()
            return redirect("home")


def handlelogin(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        myuser = authenticate(username=email.split("@")[0], email=email, password=password)
        if myuser:
            login(request, user=myuser)
            return render(request, "post.html")
        else:
            return HttpResponse("404 Not Found")

def handlePost(request):
    if request.method=="POST":
        user = request.user
        heading = request.POST.get("heading")
        problem = request.POST.get("problem")
        post = Post(email=user, heading=heading, post=problem)
        post.save()
        return HttpResponse("Posted Successfully")


def questions(request):
    if request.method == "POST":
        value = request.POST.get("subject").lower()
        if value == "biology":
            type_value = 0
        elif value == "physics":
            type_value = 1
        else:
            type_value = 2
        posts = Post.objects.all()
        values = []
        for post in posts:
            arr = np.array([post.post]).reshape(1, -1)
            predictions = model.predict(arr.ravel())
            if predictions == type_value:
                values.append(post)
        print(values)
        return render(request, "full_post.html", {"data":values})


def postanswers(request, object):
    value = Post.objects.filter(heading=object).first()
    check_data = Reply.objects.filter(post__heading=value)
    return render(request, "answer_post.html", {"data":value, "check_data":check_data})


def answerposted(request):
    if request.method == "POST":
        value = request.POST.get("heading")
        answer = request.POST.get("post_answer")
        user = request.user
        values = Post.objects.filter(heading=value).first()
        data = Reply(email=user, post=values, replay=answer)
        data.save()
        check_data = Reply.objects.filter(post__heading=value)
        return render(request, "answer_post.html", {"data":values, "check_data":check_data})
