from django.http import Http404
from django.shortcuts import render, redirect
from MainApp.forms import SnippetForm
from MainApp.models import Snippet


def get_base_context(request, pagename):
    return


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
    # context["comments"] = comments
    return render(request, 'pages/snippet.html', context)


def snippet_list(request):
    context = {'pagename': 'Просмотр сниппетов'}
    snippets = Snippet.objects.all()
    context["snippets"] = snippets
    return render(request, 'pages/view_snippets.html', context)


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
            if request.user.is_authenticated:
                snippet.user = request.user
            snippet.save()
            return redirect('snippet_list')
        # Если данные не валидные, возвращаем страницу с формой и отображаем ошибки заполнения
        form = SnippetForm(request.POST)
        print("errors = ", form.errors)
        context["form"] = form
        return render(request, 'pages/add_snippet.html', context)


def snippet_delete(request, snippet_id):
    try:
        snippet = Snippet.objects.get(id=snippet_id)
    except Snippet.DoesNotExist:
        raise Http404

    snippet.delete()
    return redirect('snippet_list')
