from django.http import Http404
from django.shortcuts import render, redirect
from MainApp.forms import SnippetForm, UserForm, CommentForm
from MainApp.models import Snippet
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


def index(request):
    context = {'pagename': 'PythonBin'}
    return render(request, 'pages/index.html', context)


def snippet(request, snippet_id):
    context = {'pagename': 'Страница сниппета'}
    try:
        snippet = Snippet.objects.get(id=snippet_id)
        # comments = snippet.comment_set.all()
    except Snippet.DoesNotExist:
        raise Http404

    context["snippet"] = snippet
    form = CommentForm()
    context["comment_form"] = form
    return render(request, 'pages/snippet.html', context)


def snippet_list(request):
    context = {'pagename': 'Просмотр сниппетов'}
    snippets = Snippet.objects.filter(public=True)
    context["snippets"] = snippets
    return render(request, 'pages/view_snippets.html', context)


@login_required()
def snippet_my(request):
    context = {'pagename': 'Мои сниппеты'}
    snippets = Snippet.objects.filter(user=request.user)
    context["snippets"] = snippets
    return render(request, 'pages/view_snippets.html', context)


# /accounts/login/?next=/snippet/add
@login_required()
def snippet_add(request):
    # Если GET-запрос,то мы хотим получить сраницу с формой создания сниппета
    context = {'pagename': 'Добавление нового сниппета'}
    if request.method == "GET":
        form = SnippetForm()
        context["form"] = form
        return render(request, 'pages/add_snippet.html', context)
    # Если POST-запрос,то мы получаем его от формы "создание сниппета"
    elif request.method == "POST":
        form = SnippetForm(request.POST)
        if form.is_valid():
            snippet = form.save(commit=False)
            snippet.user = request.user
            snippet.save()
            return redirect('snippet_list')
        # Если данные не валидные, возвращаем страницу с формой и отображаем ошибки заполнения
        form = SnippetForm(request.POST)
        print("errors = ", form.errors)
        context["form"] = form
        return render(request, 'pages/add_snippet.html', context)


def comment_add(request):
    if request.method == "POST":
        ...

def snippet_edit(request, snippet_id):
    context = {'pagename': 'Редактирование сниппета'}
    if request.method == "GET":
        try:
            snippet = Snippet.objects.get(id=snippet_id)
        except Snippet.DoesNotExist:
            raise Http404
        form = SnippetForm(instance=snippet)
        context["form"] = form
        context['button_name'] = "Edit"
        return render(request, 'pages/add_snippet.html', context)
    elif request.method == "POST":
        snippet = Snippet.objects.get(id=snippet_id)
        form = SnippetForm(request.POST, instance=snippet)
        form.save()
        return redirect('snippet_list')


def snippet_delete(request, snippet_id):
    try:
        snippet = Snippet.objects.get(id=snippet_id)
    except Snippet.DoesNotExist:
        raise Http404

    snippet.delete()
    return redirect('snippet_list')


def create_user(request):
    context = {'pagename': 'Регистрация пользователя'}
    if request.method == "GET":
        form = UserForm()
        context["form"] = form
        return render(request, 'pages/registration.html', context)
    elif request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('main_page')
        context["form"] = form
        return render(request, 'pages/registration.html', context)
    # user = User.objects.create_user


def login_page(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = auth.authenticate(request, username=username, password=password)
        print("user = ", user)
        if user is not None:
            auth.login(request, user)
        else:
            # Return error message
            pass
    return redirect('main_page')


def logout_page(request):
    auth.logout(request)
    return redirect('main_page')
