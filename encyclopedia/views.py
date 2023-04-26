from django.shortcuts import render
from markdown2 import Markdown
import random

from . import util


def convertMdToHTML(title):
    context = util.get_entry(title)
    markdown_machine = Markdown()
    if context == None:
        return None
    else:
        return markdown_machine.convert(context)


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, title):
    content_of_html = convertMdToHTML(title)
    if content_of_html == None:
        return render(request, "encyclopedia/error.html", {
            "error_massage": "This topic is not exist"
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": content_of_html
        })


def for_search(request):
    if request.method == "POST":
        search_entry = request.POST['q']
        html_content = convertMdToHTML(search_entry)
        if html_content is not None:
            return render(request, "encyclopedia/entry.html", {
                "title": search_entry,
                "content": html_content
            })
        else:
            allEntry = util.list_entries()
            recommendations = []
            for entry in allEntry:
                if search_entry.lower() in entry.lower():
                    recommendations.append(entry)
            return render(request, "encyclopedia/search.html", {
                "recommendations": recommendations
            })


def new_page(request):
    if request.method == "GET":
        return render(request, "encyclopedia/new_page.html")
    else:
        title = request.POST["title"]
        content = request.POST["content"]
        existenseTitle = util.get_entry(title)
        if existenseTitle is not None:
            return render(request, "encyclopedia/error.html", {
                "error_massage": "Entry Page exist"
            })
        else:
            util.save_entry(title, content)
            html_content = convertMdToHTML(title)
            return render(request, "encyclopedia/entry.html", {
                "title": title,
                "content": html_content
            })


def edit(request):
    if request.method == 'POST':
        title = request.POST['entry_title']
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "content": content
        })


def save_edit(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        util.save_entry(title, content)
        html_content = convertMdToHTML(title)
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": html_content
        })


def rand(request):
    allEntries = util.list_entries()
    random_entry = random.choice(allEntries)
    html_content = convertMdToHTML(random_entry)
    return render(request, "encyclopedia/entry.html", {
        "title": random_entry,
        "content": html_content
    })
