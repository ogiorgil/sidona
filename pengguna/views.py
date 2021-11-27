from django.shortcuts import render


def login(request):
    return render(request, "login.html")


def register(request):
    return render(request, "register.html")


def read_pengguna(request):
    return render(request, "read_pengguna.html")

def tabel_daftar_pengguna(request):
    return render(request, "tabel_daftar_pengguna.html")

def admin_pov_read_pengguna(request):
    return render(request, "admin_pov_read_pengguna.html")