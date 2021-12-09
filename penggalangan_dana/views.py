from django.http.response import HttpResponse
from django.shortcuts import redirect, render

from pengguna.views import get_session_data, is_authenticated
from utils.query import query


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
    return render(request, "read_pd.html", data)


def read_pd_details(request):
    id = request.GET.get("id", "")

    # No penggalangan dana id provided.
    if not id:
        return redirect("/pd")

    if not is_authenticated(request):
        return redirect(f"/auth/login?next=/pd/details/?id={id}")

    session = get_session_data(request)
    if session.get("role", "") not in ["admin", "individu", "organisasi"]:
        return HttpResponse("You are not authorized!")

    penggalangan_dana = query(f"""
        SELECT * 
        FROM penggalangan_dana_pd AS pdpd, (
            SELECT id AS kategori_id, namakategori FROM kategori_pd
        ) AS k
        WHERE pdpd.id = '{id}' AND pdpd.idkategori = k.kategori_id
    """)

    if len(penggalangan_dana) == 0:
        return HttpResponse("Penggalangan Dana does not exists!")

    penggalangan_dana = penggalangan_dana[0]

    # Current user is not the owner
    if penggalangan_dana.emailuser != session["email"]:
        return HttpResponse("You are not authorized to view this Penggalangan Dana!")

    data = {"penggalangan_dana": penggalangan_dana}

    if penggalangan_dana.namakategori == "Kesehatan":
        pasien = query(f"""
            SELECT * 
            FROM penggalangan_dana_pd AS pdpd 
            INNER JOIN pd_kesehatan AS pdk ON pdpd.id = pdk.idpd
            INNER JOIN pasien AS p ON pdk.idpasien = p.nik
        """)

        if len(pasien) == 0:
            return HttpResponse("Pasien does not exists!")

        data["pasien"] = pasien[0]
    elif penggalangan_dana.namakategori == "Rumah Ibadah":
        rumah_ibadah = query(f"""
            SELECT *
            FROM penggalangan_dana_pd AS pdpd
            INNER JOIN pd_rumah_ibadah AS pdri ON pdpd.id = pdri.idpd
            INNER JOIN rumah_ibadah AS ri ON pdri.idrumahibadah = ri.nosertifikat
            INNER JOIN (
                SELECT id AS aktivitas_id, nama AS aktivitasnama
                FROM kategori_aktivitas_pd_rumah_ibadah
            ) AS ka ON pdri.idaktivitas = ka.aktivitas_id
            INNER JOIN (
                SELECT idpd AS komorbid_idpd FROM komorbid
            ) AS ko ON pdpd.id = ko.komorbid_idpd
        """)

        if len(rumah_ibadah) == 0:
            return HttpResponse("Rumah Ibadah does not exitsts!")

        data["rumah_ibadah"] = rumah_ibadah[0]

    donasi = query(f"""
        SELECT d.email, d.timestamp, d.nominal, d.doa
        FROM penggalangan_dana_pd AS pdpd, donasi AS d
        WHERE pdpd.id = d.idpd
    """)

    data["donasi"] = donasi

    return render(request, "read_pd_details.html", data)


def create_pd(request):
    return render(request, "create_pd.html")
