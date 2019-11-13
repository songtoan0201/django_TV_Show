from django.shortcuts import render, redirect
from django.contrib import messages
from django import forms
from .models import *
# Create your views here.


def index(request):
    context = {
        'all_show': Show.objects.all()
    }

    return render(request, "TVShow/index.html", context)


def show(request, number):
    context = {
        'show': Show.objects.get(id=number)
    }
    return render(request, "TVShow/read.html", context)


def edit(request, number):
    context = {
        "number": number,
        "show": Show.objects.get(id=number)
    }
    context["show"].release_date = context["show"].release_date.strftime(
        '%Y-%m-%d')
    if request.method == "POST":
        errors = Show.objects.basic_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            # redirect the user back to the form to fix the errors
            print(errors)
            return redirect(f'/shows/{number}/edit')
        else:
            show = Show.objects.get(id=number)
            show.title = request.POST["title"]
            show.network = request.POST["network"]
            show.release_date = request.POST["release_date"]
            show.description = request.POST["description"]
            show.save()
            return redirect("/shows")
    else:
        return render(request, "TVShow/update.html", context)


def add(request):
    # if the errors object is empty, that means there were no errors!
    if request.method == "POST":
        # pass the post data to the method we wrote and save the response in a variable called errors
        errors = Show.objects.basic_validator(request.POST)
        # check if the errors dictionary has anything in it
        all_show = Show.objects.all()

        for show in all_show:
            if show.title.lower() != request.POST["title"].lower():
                errors["unique"] = "Title already exists in the database"
        if len(errors) > 0:
            # if the errors dictionary contains anything, loop through each key-value pair and make a flash message
            for key, value in errors.items():
                # Adding errors into messages
                messages.error(request, value)
            # redirect the user back to the form to fix the errors
            print(errors)
            return redirect('/shows/new')
        else:
            Show.objects.create(title=request.POST["title"], network=request.POST["network"],
                                release_date=request.POST["release_date"], description=request.POST["description"])
            messages.success(request, "Show successfully updated")
            return redirect("/shows")
    else:
        return render(request, "TVShow/create.html")


def delete(request, number):
    show = Show.objects.get(id=number)
    show.delete()
    return redirect("/shows")
