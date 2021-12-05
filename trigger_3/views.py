from django.shortcuts import render
from utils.query import query
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect

# Create your views here.


def daftar_penggalangan_pengguna_pov(request):
    data = query(
        """SELECT p.id, p.judul, p.kota, p.provinsi, p.tanggalaktifakhir, p.sisahari, p.jumlahdibutuhkan, k.namakategori
        FROM penggalangan_dana_pd p JOIN kategori_pd k on p.idkategori=k.id WHERE statusverifikasi = 'Terverifikasi'"""
    )
    print("DATA: " + str(data))
    argument = {"penggalangans": data}
    return render(request, "pengguna_pov_daftar_penggalangan.html", argument)


def daftar_penggalangan_admin_pov(request):
    data = query(
        """SELECT p.id, p.judul, p.kota, p.provinsi, p.tanggalaktifakhir, p.sisahari, p.jumlahdibutuhkan, k.namakategori, p.statusverifikasi
        FROM penggalangan_dana_pd p JOIN kategori_pd k ON p.idkategori=k.id"""
    )
    print("DATA: " + str(data))
    argument = {"penggalangans": data}
    return render(request, "admin_pov_daftar_penggalangan.html", argument)


def form_update_penggalangan(request):
    response = {"kategori": "Rumah Ibadah"}
    return render(request, "form_update_penggalangan.html", response)


def form_verifikasi_penggalangan(request):
    return render(request, "form_verifikasi_penggalangan.html")


def detail_penggalangan_pengguna_pov(request):
    response = {"kategori": "Kesehatan"}
    return render(request, "pengguna_pov_detail_penggalangan.html", response)


@csrf_exempt
def form_create_kategori(request):
    if request.method == "POST":
        body = request.POST
        namakategori = body["namakategori"]
        query_str = f"INSERT INTO kategori_pd (namakategori, alias_kategori) VALUES ('{namakategori}', '{namakategori[0]}')"
        print(query(query_str))
        return HttpResponseRedirect("/t3/kategori-penggalangan-admin/")

    context = query("SELECT id FROM KATEGORI_PD ORDER BY id DESC LIMIT 1")[0]
    context = {"context": context}
    return render(request, "form_create_kategori_penggalangan.html", context)


def form_update_kategori(request):
    return render(request, "form_update_kategori_penggalangan.html")


def kategori_penggalangan(request):
    data = query("SELECT id, namakategori FROM kategori_pd")
    argument = {"kategoris": data}
    return render(request, "admin_pov_daftar_kategori.html", argument)