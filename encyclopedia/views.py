from random import randint

from django.http import HttpRequest, HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, title):
    content = util.get_entry(title)
    if content == None:
        return HttpResponseBadRequest("Bad Request: the requested page was not found")

    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": content
    })


def search(request):
    if request.method == "POST":
        title = request.POST["q"]
        entries = util.list_entries()
        contents = []

        for entry in entries:
            entry = entry
            if entry.find(title) != -1:
                contents.append(entry)

        if len(contents) == 0:
            return HttpResponseBadRequest("Bad Request: the requested page was not found")

        return render(request, "encyclopedia/search.html", {
            "contents": contents
        })

    return HttpResponseRedirect(reverse("wiki:index"))


def new(request):
    if request.method == "POST":
        title = request.POST["title"]
        content = request.POST["content"]
        entries = util.list_entries()

        for entry in entries:
            if entry == title:
                return HttpResponseBadRequest("Bad Request: the encyclopedia entry title already exists")

        util.save_entry(title, content)

        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": content
        })

    return render(request, "encyclopedia/new.html")


def edit(request, title):
    content = util.get_entry(title)
    if content == None:
        return HttpResponseBadRequest("Bad Request: the requested page was not found")

    if request.method == "POST":
        new = request.POST["new"]
        util.save_entry(title, new)
        return HttpResponseRedirect(reverse("wiki:entry", args=(title,)))

    return render(request, "encyclopedia/edit.html", {
        "title": title,
        "content": content
    })


def random(request):
    entries = util.list_entries()
    random_num = randint(0, len(entries) - 1)
    title = entries[random_num]
    content = util.get_entry(title)

    if content == None:
        return HttpResponseBadRequest("Bad Request: the requested page was not found")

    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": content
    })
