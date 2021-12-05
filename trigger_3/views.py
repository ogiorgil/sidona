from django.shortcuts import render
from utils.query import query
from django.views.decorators.csrf import csrf_exempt

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


@csrf_exempt
def form_create_kategori(request):
    if request.method == "POST":
        print(request.POST)
        body = request.POST

    context = query("SELECT id FROM KATEGORI_PD")[-1]
    print(context)
    print(int(context.id) + 1)
    print(type(context.id))
    context = {"context": context}
    return render(request, "form_create_kategori_penggalangan.html", context)


def form_update_kategori(request):
    return render(request, "form_update_kategori_penggalangan.html")


def kategori_penggalangan(request):
    data = query("SELECT id, namakategori FROM kategori_pd")
    argument = {"kategoris": data}
    return render(request, "admin_pov_daftar_kategori.html", argument)