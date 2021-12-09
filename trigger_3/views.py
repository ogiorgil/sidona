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


def detail_penggalangan(request):
    context = dict()
    id_penggalangan = request.GET.get("id")
    data = query(
        f"""SELECT p.id, p.emailuser, p.judul, p.deskripsi, p.kota, p.provinsi, p.tanggalaktifakhir, p.jumlahdibutuhkan, p.statusverifikasi, emailadmin,
        k.namakategori, p.linkrepo, p.jumlahterkumpul, p.jumlahterpakai
        FROM penggalangan_dana_pd p JOIN kategori_pd k ON p.idkategori=k.id
        WHERE p.id='{id_penggalangan}'"""
    )
    context["p"] = data[0]

    catatans = query(
        f"""SELECT informasi
        FROM catatan_pengajuan 
        WHERE idpd='{id_penggalangan}'"""
    )
    context["catatans"] = catatans

    donasis = query(
        f"""SELECT email, timestamp, nominal, doa
        FROM donasi
        WHERE idpd='{id_penggalangan}'"""
    )
    context["donasis"] = donasis

    penggunaan_danas = query(
        f"""SELECT timestamp, nominal, deskripsi
        FROM riwayat_penggunaan_dana
        WHERE idpd='{id_penggalangan}'"""
    )
    context["penggunaan_danas"] = penggunaan_danas

    if data[0].namakategori == "Kesehatan":
        data_pasien = query(
            f"""SELECT p.nik, p.nama, pk.penyakit
            FROM pd_kesehatan pk JOIN pasien p ON pk.idpasien=p.nik
            WHERE pk.idpd='{id_penggalangan}'"""
        )
        print(data_pasien)
        context["pasien"] = data_pasien[0]
        komorbid = query(
            f"""SELECT komorbid FROM komorbid
            WHERE idpd='{id_penggalangan}'"""
        )
        print(komorbid)
        context["komorbid"] = komorbid
    if data[0].namakategori == "Rumah Ibadah":
        data_rumah_ibadah = query(
            f"""SELECT p.idrumahibadah, k.nama as kategori
            FROM pd_rumah_ibadah p JOIN kategori_aktivitas_pd_rumah_ibadah k
            ON p.idaktivitas=k.id
            WHERE idpd='{id_penggalangan}'"""
        )
        print(data_rumah_ibadah)
        context["rumah_ibadah"] = data_rumah_ibadah[0]
    print(context)
    return render(request, "detail_penggalangan.html", context)


@csrf_exempt
def form_create_kategori(request):
    if request.method == "POST":
        body = request.POST
        namakategori = body["namakategori"]
        
        query_str = f"INSERT INTO kategori_pd (namakategori, alias_kategori) VALUES ('{namakategori}', '{namakategori[0]}')"
        print(query(query_str))
        return HttpResponseRedirect("/t3/kategori-penggalangan-admin/")

    context = query("SELECT id FROM KATEGORI_PD ORDER BY id DESC LIMIT 1")[0]
    latest_id = int(context.id) + 1
    context = {"latest_id": latest_id}
    return render(request, "form_create_kategori_penggalangan.html", context)


@csrf_exempt
def form_update_kategori(request):
    id_kategori = request.GET.get("id")
    nama_kategori = request.GET.get("nama")
    if request.method == "POST":
        body = request.POST
        namakategori = body["namakategori"]
        query_str = f"""UPDATE kategori_pd
        SET namakategori='{namakategori}', alias_kategori='{namakategori[0]}' 
        WHERE id='{id_kategori}'"""
        print(query(query_str))
        return HttpResponseRedirect("/t3/kategori-penggalangan-admin")
    context = {"id_kategori": id_kategori, "nama_kategori": nama_kategori}
    return render(request, "form_update_kategori_penggalangan.html", context)


def kategori_penggalangan(request):
    data = query("SELECT id, namakategori FROM kategori_pd")
    context = {"kategoris": data}
    return render(request, "admin_pov_daftar_kategori.html", context)