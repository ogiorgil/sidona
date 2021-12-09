from django.shortcuts import render
from utils.query import query
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
from django.http import HttpResponseRedirect, HttpResponse
from pengguna.views import is_authenticated

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
    if not is_authenticated(request):
        return redirect("/auth/login?next=/t4/profil-pengguna")
    
    if request.session["role"] == "admin":
        return HttpResponse("Admin tidak mempunyai profil")

    email = request.session['email']
    # ntar pas di query select berdasarkan email sessionnya
    data = query(
        """select d.idpd, pdd.judul, k.namakategori,s.status,d.email,d.timestamp
        from penggalangan_dana_pd pdd
        join kategori_pd k on pdd.idkategori = k.id
        join donasi d on pdd.id = d.idpd
        join status_pembayaran s on d.idstatuspembayaran=s.id"""
    )
    print("DATA: " + str(data))
    argument = {"donasi": data}
    return render(request, "profilpengguna.html", argument)
  

def data_donasi(request):
    # harus tau email si pengguna
    email = request.session['email']

    # tampilin semua donasi yang pernah dia buat
    data = query(
        f"""select d.idpd, pdd.judul, k.namakategori,s.status,d.email,d.timestamp
        from penggalangan_dana_pd pdd
        join kategori_pd k on pdd.idkategori = k.id
        join donasi d on pdd.id = d.idpd
        join status_pembayaran s on d.idstatuspembayaran=s.id
        where d.email = '{ email }' """
    )
    print("DATA: " + str(data))
    argument = {"donasi": data}
    return render(request, "datadonasi.html", argument)


def detail_donasi_pengguna_pov(request):
    return render(request, "detaildonasi.html")

def detail_penggalangan(request):
    context = dict()
    email_pengguna = request.GET.get("email")
    timestamp = request.GET.get("timestamp")
 
    data = query(
        f"""select d.email,d.timestamp, pdd.judul,d.nominal, d.metodebayar, d.statusanonim, d.doa
        from donasi d, penggalangan_dana_pd pdd
        where d.email = '{email_pengguna}' and d.timestamp = '{timestamp}' and d.idpd = pdd.id"""
    )
    context["p"] = data[0]
    return render(request, "detaildonasi.html", context)