from django.shortcuts import render, redirect
from utils.query import query
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect
from pengguna.views import is_authenticated
from datetime import datetime

# Create your views here.
# def data_donasi(request):
#     return render(request, "datadonasi.html")


def detail_penggalangan_pengguna_pov(request):
    response = {"kategori": "Kesehatan"}
    return render(request, "detail_penggalangan_dana.html", response)


@csrf_exempt
def form_create_donasi(request):
    id_penggalangan = request.GET.get("id")
    if not is_authenticated(request):
        return redirect(f"/auth/login?next=/t4/create-donasi/?id={id_penggalangan}")
    
    if request.session["role"] != "individu":
        return HttpResponse("Hanya individu yang bisa berdonasi")

    context = dict()
    id_penggalangan = request.GET.get("id")
    email = request.session['email']
    if request.method == "POST":
        print(request.POST)
        print(email)
        timestamp = request.POST.get('timestamp')
        print(timestamp)
        nominal = request.POST.get('nominal', False)
        print(nominal)
        metode_bayar = request.POST.get('metode_bayar', False)
        print(metode_bayar)
        opsi = request.POST.get('opsi', False)
        doa = request.POST.get('doa', False)
        idstatuspembayaran = 1 
        # timestamp = body["timestamp"]
        # judul = body["judul"]
        # nominal = body['nominal']
        # metode_bayar = body['metode_bayar']
        # opsi = body['opsi']
        opsi2 = 'Ya'
        if(opsi == 'Ya'):
            opsi2 = 'Anonim'
        else:
            opsi2 = 'Tidak Anonim'
        
        print(opsi2)
        print(doa)
        
        query_str = f"INSERT INTO donasi VALUES ('{email}', '{timestamp}',{nominal},'{metode_bayar}','{opsi2}','{doa}','{id_penggalangan}','{idstatuspembayaran}')"
        # (email, timestamp,nominal,metodebayar,statusanonim,doa,idpd,idstatuspembayaran) 
        print(query(query_str))

    
        # //print(query_str)

        return HttpResponseRedirect("/t4/data-donasi/")
    
    else :
        data = query(
            f"""select p.email, pdd.judul
            from penggalang_dana p, penggalangan_dana_pd pdd
            where p.email = '{email}' and pdd.id = '{id_penggalangan}'"""
        )
        print(data)
        context["d"] = data[0]
        return render(request, "formdonasi.html", context)


def daftar_penggalangan_pengguna_pov(request):
    return render(request, "penggalangandana.html")


def profil_pengguna(request):
    context = dict()
    if not is_authenticated(request):
        return redirect("/auth/login?next=/t4/profil-pengguna")

    if request.session["role"] == "admin":
        return HttpResponse("Admin tidak mempunyai profil")

    email = request.session['email']
    # ntar pas di query select berdasarkan email sessionnya
    if request.session["role"] == "individu":
        data = query(
            f"""select p.email, p.nama, p.nomorhp,p.alamat,p.namabank,p.norek,i.NIK,i.tanggallahir,i.jeniskelamin,i.jumlahwishlist
            from penggalang_dana p, individu i
            where p.email ='{email}' and i.email = p.email """
        )
        
        context["p"] = data[0]
        print(data)
    elif request.session["role"] == "organisasi":
        org = query(f"""select p.nama, p.nomorhp,p.alamat,p.namabank,p.norek, o.email, o.namaorganisasi,o.nap,o.notelporganisasi,o.tahunberdiri from penggalang_dana p, organisasi o where o.email ='{email}' and o.email = p.email """)
        context["org"] = org[0]
        print(context)

    wishlist = query(
        f"""select w.idpd, pdd.judul, k.namakategori
        from wishlist_donasi w
        join penggalangan_dana_pd pdd on w.idpd= pdd.id
        join kategori_pd k on pdd.idkategori = k.id
        where w.email ='{email}'"""
    )
    context["wishlist"] = wishlist
    context["role"]= request.session["role"]

    return render(request, "profilpengguna.html", context)


def data_donasi(request):
    # harus tau email si pengguna
    if not is_authenticated(request):
        return redirect("/auth/login?next=/t4/data-donasi")

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
    context = dict()
    email_pengguna = request.GET.get("email")
    timestamp = request.GET.get("timestamp")
    # datetimeObj = datetime.strptime(timestamp, '%Y-%m-%dT%H::%M::%S.%f')
    print(email_pengguna)
    print(timestamp)
    data = query(
        f"""select d.email,d.timestamp, pdd.judul,d.nominal, d.metodebayar, d.statusanonim, d.doa
        from donasi d, penggalangan_dana_pd pdd
        where d.email = '{email_pengguna}' and d.timestamp ='{timestamp}' and d.idpd = pdd.id"""
    )
    print(data)
    context["d"] = data[0]
    
    return render(request, "detaildonasi.html", context)


  # d.timestamp ='{timestamp}'
@csrf_exempt
def tambah_wishlist(request):
    if not is_authenticated(request):
        return redirect("/auth/login?next=/t3/daftar-penggalangan")
    email = request.session['email']
    if request.method == "POST":
        body = request.POST
        id = body["id"]
        
        query_str = f"INSERT INTO wishlist_donasi (email, idpd) VALUES ('{email}', '{id}')"
        print(query(query_str))
        return HttpResponseRedirect("/t4/profil-pengguna/")

    return render(request, "pengguna_pov_daftar_penggalangan.html")


@csrf_exempt
def delete_wishlist(request):
    email = request.session['email']
    if request.method == "POST":
        body = request.POST
        id = body["id"]
        
        query_str = f"delete from wishlist_donasi where idpd = '{id}' and email ='{email}' "
        print(query(query_str))
        return HttpResponseRedirect("/t4/profil-pengguna/")

    return render(request, "pengguna_pov_daftar_penggalangan.html")