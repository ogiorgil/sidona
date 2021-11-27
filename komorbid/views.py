from django.shortcuts import render


def create_komorbid(request):
    return render(request, "create_komorbid.html")


def read_komorbid(request):
    return render(request, "read_komorbid.html")


def update_komorbid(request):
    return render(request, "update_komorbid.html")
