from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt

from utils.query import query


def is_authenticated(request):
    try:
        request.session['email']
        return True
    except KeyError:
        return False


def get_role(email, password):
    if len(query(f"SELECT 1 FROM ADMIN WHERE email = '{email}' AND password = '{password}'")):
        return "admin"

    if len(query(f"SELECT 1 FROM PENGGALANG_DANA WHERE email = '{email}' AND password = '{password}'")):
        if len(query(f"SELECT 1 FROM INDIVIDU WHERE email = '{email}'")):
            return "individu"
        else:
            return "organisasi"

    return ""


@csrf_exempt
def login(request):
    next = request.GET.get('next')

    if request.method != "POST":
        return login_view(request)

    try:
        email = str(request.session['email'])
        password = str(request.session['password'])
    except:
        email = str(request.POST['email'])
        password = str(request.POST['password'])

    role = get_role(email, password)
    print(role)

    if (role == ""):
        return login_view(request)
    else:
        request.session['email'] = email
        request.session['password'] = password
        request.session['role'] = role

        if (next != None and next != "None"):
            return redirect(next)
        else:
            return redirect("/t3/daftar-penggalangan")


def login_view(request):
    return render(request, "login.html")


def login_view(request):
    if is_authenticated(request):
        return redirect("/t3/daftar-penggalangan")

    return render(request, "login.html")


def register_view(request):
    return render(request, "register.html")


def read_pengguna(request):
    return render(request, "read_pengguna.html")


def tabel_daftar_pengguna(request):
    return render(request, "tabel_daftar_pengguna.html")


def admin_pov_read_pengguna(request):
    return render(request, "admin_pov_read_pengguna.html")
