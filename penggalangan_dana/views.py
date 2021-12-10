from django.http.response import HttpResponse
from django.shortcuts import redirect, render

from pengguna.views import get_session_data, is_authenticated
from utils.query import query


def create_pd(request):
    return render(request, "create_pd.html")


def read_pd(request):
    if not is_authenticated(request):
        return redirect("/auth/login?next=/pd")

    session = get_session_data(request)
    if session.get("role", "") not in ["admin", "individu", "organisasi"]:
        return HttpResponse("You are not authorized!")

    penggalangan_dana_pribadi = query(f"""
        SELECT * 
        FROM penggalangan_dana_pd AS pdpd, (
            SELECT id AS kategori_id, namakategori FROM kategori_pd
        ) AS k
        WHERE pdpd.emailuser = '{session["email"]}' AND pdpd.idkategori = k.kategori_id
    """)

    data = {"penggalangan_dana": penggalangan_dana_pribadi}
    print(data)
    return render(request, "read_pd.html", data)


def read_pd_details(request):
    return render(request, "read_pd_details.html")
