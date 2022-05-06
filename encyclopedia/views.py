from http.client import HTTPResponse
from turtle import title
from django.shortcuts import render, redirect
from encyclopedia.forms import EntryCreateForm as enterycreateform, EntryEditForm as editForm
import random
from . import util
import encyclopedia
import markdown2

def index(request):
    q=request.GET.get('q')
    entries=util.list_entries()
    if q:
        entries=[e for e in entries if q.lower() in e.lower()]
    if q in entries:
        return redirect('wiki:single-entry',entries[0])
            
    return render(request, "encyclopedia/index.html", {
        "entries": entries
    })
def single_entry(request,title: str):
    content=util.get_entry(title)
    return render(request,'encyclopedia/single_entry.html',context={'title':title,'content':markdown2.markdown(content)})
def create(request):
    form=enterycreateform()
    if request.method=='POST':
        print("----------------------------------")
        form=enterycreateform(request.POST)
        if form.is_valid():
            title=form.cleaned_data['title']
            if title in util.list_entries():
                return render(request,'encyclopedia/error.html',context={
                    'title':f'the entry {title}already exist'})
            content=form.cleaned_data['content']
            util.save_entry(title,content)
            return redirect('wiki:index')
    return render(request,'encyclopedia/create.html',{'form':form,}) 
     
    
def edit(request, title: str):
    if request.method == 'GET' :
        entries = util.get_entry(title)
        return render(request, 'encyclopedia/edit.html', context={
            'title': title,
            'form': editForm(initial={'content': entries}),
        })
    elif request.method == 'POST':
        form = editForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data['content']
            util.save_entry(title, content)
            entries = util.get_entry(title)
            return render(request, 'encyclopedia/edit.html', context={
                'title':title,
                'form': markdown2.markdown(entries),
               })

    
def random_entry(request):
    return redirect('wiki:single-entry',title=random.choice(util.list_entries()))