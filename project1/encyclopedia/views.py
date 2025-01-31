from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
from . import util
import random
import markdown2


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry_page(request,title):
    content=util.get_entry(title)
    if content:
        return render (request, "encyclopedia/entry.html",{
            "title":title,
            "content":markdown2.markdown(content)
        })
    else:
        return render (request, "encyclopedia/error.html",{
        "message": "Page not found"
    })

def search(request):
    query=request.GET.get("q","").strip()
    entries=util.list_entries()
    if query in entries:
        return redirect (reverse("entry_page",args=[query]))
    matches=[entry for entry in entries if query.lower()in entry.lower()]
    return render(request,"encyclopidia/search.html",{"query":query,"matches":matches})

def new_page(request):
    if request.method=="POST":
        title=request.POST["title"].strip()
        content=request.POST["content"].strip()
        if title in util.list_entries():
            return render(request,"encyclopedia/entry.html",{"message: Entry already exists!"})
        util.save_entry(title,content)
        return redirect (reverse("entry_page",args=[title]))
    return render (request, "encyclopedia/new_page.html")

def edit_page(request,title):
    content=util.get_entry(title)
    if content is None:
        return render (request,"encyclopedia/error.html",{"message":"entry not found"})
    if request.method=="POST":
        new_content=request.POST["content"].strip()
        util.save_entry(title, new_content)
        return redirect (reverse("entry_page",args=[title]))
    return render (request, "encyclopedia/edit_page.html",{"title":title,"content":content})

def random_page(request):
    entries=util.list_entries()
    if entries:
        random_title=random.choice(entries)
        return redirect (reverse("entry_page",args=[random_title]))
    return render (request, "encyclopedia/error_page.html",{"no entries found"})
