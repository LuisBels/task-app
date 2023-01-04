from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
from .forms import TaskForm
from .models import Task
from django.utils import timezone
from django.contrib.auth.decorators import login_required

# Create your views here.


def home(request):
    tasks = Task.objects.filter(user=request.user)
    return render(request, "tasks/home.html", {
        "tasks": tasks
    })


def signup(request):
   if request.method == "GET":
    return render(request, "tasks/signup.html",{
        "form":UserCreationForm
    })

   else:
    if request.POST["password1"] == request.POST["password2"]:
        try:
            user = User.objects.create_user(username=request.POST["username"],
                                            password=request.POST["password1"])
            user.save()
            login(request, user)
            return redirect("tasks")
        except IntegrityError:
            return render(request, "tasks/signup.html",{
                "form":UserCreationForm,
                "error": "User ready exist"
            })
    return render(request, "tasks/signup.html",{
        "form":UserCreationForm,
        "error": "password not macht"
    })


@login_required
def tasks(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, "tasks/tasks.html", {"tasks":tasks})


@login_required
def tasks_completed(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=False)
    return render(request, "tasks/task_completed.html", {"tasks":tasks})

@login_required
def task_detail(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    return render(request, "tasks/task_detail.html",{
        "task":task
    })


@login_required
def edit_task(request, task_id):
    if request.method == "GET":
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        form = TaskForm(instance=task)
        return render(request, "tasks/edit_task.html",{
        "task":task,
        "form": form
        })
    else:
        try:
            task = get_object_or_404(Task, pk=task_id, user=request.user)
            form = TaskForm(request.POST,instance=task)
            form.save()
            return redirect("tasks")
        except ValueError:
            return render(request, "tasks/edit_task.html",{
            "task":task,
            "form": form,
            "error": "Error updating task sorry"
            })


@login_required
def complete_task(request,task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == "POST":
        task.datecompleted = timezone.now()
        task.save()
        return redirect("tasks")


@login_required
def delete_task(request,task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == "POST":
        task.delete()
        return redirect("tasks")


@login_required
def created_task(request):
    if request.method == "GET":
        return render(request, "tasks/created_task.html",{
            "form":TaskForm
        })
    else:
        try:
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect("tasks")
        except ValueError:
            return render(request, "tasks/created_task.html",{
            "form":TaskForm,
            "error": "Please provide valid data"
            })

@login_required
def sigout(request):
    logout(request)
    return redirect("tasks")


def signin(request):
    if request.method == "GET":
        return render(request, "tasks/signin.html",{
            "form": AuthenticationForm
        })
    else:
        user = authenticate(request, username=request.POST["username"],
                                    password=request.POST["password"])
        if user is None:
            return render(request, "tasks/signin.html",{
                "form": AuthenticationForm,
                "error": "username or passwors is incorrect"
            })
        else:
            login(request, user)
            return redirect("tasks")