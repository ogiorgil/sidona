from django.shortcuts import render

# Create your views here.


def daftar_penggalangan_pengguna_pov(request):
    return render(request, "pengguna_pov_daftar_penggalangan.html")


def daftar_penggalangan_admin_pov(request):
    return render(request, "admin_pov_daftar_penggalangan.html")


def form_update_penggalangan(request):
    response = {"kategori": "Rumah Ibadah"}
    return render(request, "form_update_penggalangan.html", response)


def form_verifikasi_penggalangan(request):
    return render(request, "form_verifikasi_penggalangan.html")


def detail_penggalangan_pengguna_pov(request):
    response = {"kategori": "Kesehatan"}
    return render(request, "pengguna_pov_detail_penggalangan.html", response)


def form_create_kategori(request):
    return render(request, "form_create_kategori_penggalangan.html")


def form_update_kategori(request):
    return render(request, "form_update_kategori_penggalangan.html")


def kategori_penggalangan(request):
    kategoris = [
        "Rumah Ibadah",
        "Kesehatan",
        "Jembatan",
        "Pendidikan",
        "Sembako",
        "Yatim Piatu",
        "Bencana",
    ]
    lst = list()
    for i in enumerate(kategoris):
        lst.append({"id": i[0] + 1, "namakategori": i[1]})

    response = {"kategoris": lst}
    return render(request, "admin_pov_daftar_kategori.html", response)