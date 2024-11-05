from datetime import datetime, timedelta
from django.views.decorators.http import require_http_methods
from django.shortcuts import render
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.conf import settings
from django.utils.timezone import make_aware
from .models import Todo
from .forms import TodoForm


def fix_todos(todos):
    fixed_todos = []
    for todo in todos:
        is_overdue = not todo.done and todo.due_date < timezone.now()
        fixed_todos += [{
            "id": todo.id,
            "title": todo.title,
            "description": todo.description,
            "due_date": todo.due_date,
            "is_overdue": is_overdue,
            "done": todo.done
        }]
    return fixed_todos


@login_required
def index(req):
    todos = fix_todos(Todo.objects.filter(user=req.user))
    context = {"todos": todos}
    context["form"] = TodoForm()
    return render(req, 'index.html', context)


@login_required
def new_todo(req):
    context = {}
    context["purpose"] = "New"
    context["form"] = TodoForm()
    return render(req, '_todo_form.html', context)


@login_required
@require_POST
def add_todo(req):
    form = TodoForm(req.POST)
    if form.is_valid():
        date = form.cleaned_data.get('date') or None
        time = form.cleaned_data.get('time') or None
        if not date:
            due_date = datetime.now() + timedelta(days=7)
        elif not time:
            due_date = datetime.combine(date, datetime.now().time())
        else:
            due_date = datetime.combine(date, time)
        settings.TIME_ZONE
        due_date = make_aware(due_date)
        todo = Todo(
            title=form.cleaned_data.get('title'), 
            description=form.cleaned_data.get('description'), 
            due_date=due_date,
            user = req.user
            )
        todo.save()
        context = {"todos": fix_todos(Todo.objects.filter(user=req.user))}
        return render(req, '_todo_table.html', context)


@login_required
def display_todo(req, pk):
    todo = Todo.objects.get(pk=pk, user=req.user)
    # split due_date into date and time
    due_date = todo.due_date
    formdate = due_date.date().strftime('%Y-%m-%d')
    formtime = due_date.time().strftime('%H:%M:%S')
    formdata = {"title": todo.title, "description": todo.description, "date": formdate, "time": formtime}
    context = {"todo": todo}
    context["purpose"] = "Update"
    context["form"] = TodoForm(formdata)
    return render(req, '_todo_form.html', context)


@login_required
@require_POST
def update_todo(req, pk):
    todo = Todo.objects.get(pk=pk, user=req.user)
    form = TodoForm(req.POST)
    if form.is_valid():
        date = form.cleaned_data.get('date') or None
        time = form.cleaned_data.get('time') or None
        if not date:
            due_date = datetime.now() + timedelta(days=7)
        elif not time:
            due_date = datetime.combine(date, datetime.now().time())
        else:
            due_date = datetime.combine(date, time)
        settings.TIME_ZONE
        due_date = make_aware(due_date)

        todo.title=form.cleaned_data.get('title')
        todo.description=form.cleaned_data.get('description')
        todo.due_date=due_date
        todo.save()

        context = {"todos": fix_todos(Todo.objects.filter(user=req.user))}
        return render(req, '_todo_table.html', context)

@login_required
def toggle_todo(req, pk):
    todo = Todo.objects.get(pk=pk, user=req.user)
    todo.done = not todo.done
    todo.save()
    context = {"todos": fix_todos(Todo.objects.filter(user=req.user))}
    return render(req, '_todo_table.html', context)


@login_required
@require_http_methods(['DELETE'])
def delete_todo(req, pk):
    todo = Todo.objects.get(pk=pk, user=req.user)
    todo.delete()
    context = {"todos": fix_todos(Todo.objects.filter(user=req.user))}
    return render(req, '_todo_table.html', context)
