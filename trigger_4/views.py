from django.shortcuts import render
from utils.query import query
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect

# Create your views here.
# def data_donasi(request):
#     return render(request, "datadonasi.html")


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

def data_donasi(request):
    data = query(
        """select d.idpd, pdd.judul, k.namakategori,s.status,d.email,d.timestamp
        from penggalangan_dana_pd pdd
        join kategori_pd k on pdd.idkategori = k.id
        join donasi d on pdd.id = d.idpd
        join status_pembayaran s on d.idstatuspembayaran=s.id"""
    )
    print("DATA: " + str(data))
    argument = {"donasi": data}
    return render(request, "datadonasi.html", argument)



def detail_donasi_pengguna_pov(request):
    return render(request, "detaildonasi.html")