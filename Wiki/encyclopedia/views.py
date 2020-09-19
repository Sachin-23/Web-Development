from django import forms
from django.http import HttpResponse
import markdown2
from random import randrange

from django.shortcuts import render
from . import util


class EditAreaForm(forms.Form):
    title = forms.CharField(label="Title", widget=forms.TextInput(attrs={"style": "width: 200px;"}), required=True)
    textarea = forms.CharField(label="Content", widget=forms.Textarea(attrs={'rows':4, 'cols':15}), required=True)


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })
    
def get(request, title=None):
    if title == None:
        title = request.GET.get('q')
    entries = util.list_entries()
    if title in entries:
        return render(request, "encyclopedia/search.html", {
            "title": title,
            "content": markdown2.markdown(util.get_entry(title)),
        })
    else:
        match = [i for i in entries if title in i]
        if len(match) != 0:
            return render(request, "encyclopedia/similiar.html", {
                "title": f"Similiar search result found for {title}",
               "entries": match
            })
    return render(request, "encyclopedia/similiar.html",  {
                "title": f"No search result found for {title}",
    })


def create(request):
    if request.method == "POST":
        form = EditAreaForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["textarea"]
            if title not in util.list_entries():
                util.save_entry(title, content)
                return render(request, "encyclopedia/search.html", {
                    "title": title,
                    "content": markdown2.markdown(util.get_entry(title))
                })
            else: 
                return render(request, "encyclopedia/create.html", {
                    "editarea": form,
                    "Error": "<p style='color: #ff0000;'>Title Already Exists</p>"
                })
        else: 
            return HttpResponse("<h1>Form Invalid</h1>")
    return render(request, "encyclopedia/create.html", {
        "editarea": EditAreaForm(),
    })

def edit(request):
    if request.method == "POST":
        form = EditAreaForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["textarea"]
            util.save_entry(title, content)
            return render(request, "encyclopedia/search.html", {
                "title": title,
                "content": markdown2.markdown(util.get_entry(title)),
            })
    title = request.GET.get("title")
    content = util.get_entry(title)
    return render(request, "encyclopedia/edit.html", {
        "editarea": EditAreaForm(initial={"title": title, "textarea": content})
    })

def random_page(request):
    entries = util.list_entries()
    if len(entries) != 0:
        print(entries)
        rand_no = randrange(len(entries)) 
        print(entries[rand_no])
        return render(request, "encyclopedia/search.html", {
            "title": entries[rand_no],
            "content": markdown2.markdown(util.get_entry(entries[rand_no])),
        })
    else:
        return HttpResponse("<h1>404 Error Not Found</h1>")

