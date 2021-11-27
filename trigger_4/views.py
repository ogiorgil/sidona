from django.shortcuts import render

# Create your views here.
def data_donasi(request):
    return render(request, "datadonasi.html")


def detail_penggalangan_pengguna_pov(request):
    response = {"kategori": "Kesehatan"}
    return render(request, "detail_penggalangan_dana.html", response)

def form_create_donasi(request):
    return render(request, "formdonasi.html")

def detail_donasi_pengguna_pov(request):
    return render(request, "detaildonasi.html")

def daftar_penggalangan_pengguna_pov(request):
    return render(request, "penggalangandana.html")

def profil_pengguna(request):
    return render(request, "profilpengguna.html")