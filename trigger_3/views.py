from django.shortcuts import render, redirect
from utils.query import query
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from pengguna.views import is_authenticated

# Create your views here.


def daftar_penggalangan_pengguna_pov(request):
    data = query(
        """SELECT p.id, p.judul, p.kota, p.provinsi, p.tanggalaktifakhir, p.sisahari, p.jumlahdibutuhkan, k.namakategori
        FROM penggalangan_dana_pd p JOIN kategori_pd k on p.idkategori=k.id WHERE statusverifikasi = 'Terverifikasi'"""
    )
    argument = {"penggalangans": data}
    return render(request, "pengguna_pov_daftar_penggalangan.html", argument)


def daftar_penggalangan_pribadi(request):
    if not is_authenticated(request):
        return redirect("/auth/login/?next=/t3/daftar-penggalangan-pribadi")

    if request.session["role"] == "admin":
        return HttpResponse("Admin tidak bisa memiliki penggalangan")

    data = query(
        f"""SELECT p.id, p.judul, p.kota, p.provinsi, p.tanggalaktifawal, p.tanggalaktifakhir, p.sisahari, p.jumlahdibutuhkan, k.namakategori, p.statusverifikasi
        FROM penggalangan_dana_pd p JOIN kategori_pd k on p.idkategori=k.id
        WHERE p.emailuser='{request.session["email"]}'
        """
    )

    context = {"penggalangans": data}
    return render(request, "pengguna_pov_pribadi_daftar_penggalangan.html", context)


def daftar_penggalangan_admin_pov(request):
    if not is_authenticated(request):
        return redirect("/auth/login?next=/t3/daftar-penggalangan-admin")

    if request.session["role"] != "admin":
        return HttpResponse("Hanya admin bisa mengakses halaman ini")

    data = query(
        """SELECT p.id, p.judul, p.kota, p.provinsi, p.tanggalaktifawal, p.tanggalaktifakhir, p.sisahari, p.jumlahdibutuhkan, k.namakategori, p.statusverifikasi
        FROM penggalangan_dana_pd p JOIN kategori_pd k ON p.idkategori=k.id"""
    )
    print("DATA: " + str(data))
    argument = {"penggalangans": data}
    return render(request, "admin_pov_daftar_penggalangan.html", argument)


@csrf_exempt
def form_update_penggalangan(request):
    # if not is_authenticated(request):
    #     return redirect("/auth/login/?next=/t3/daftar-penggalangan-pribadi")

    # if request.session["role"] == "admin":
    #     return HttpResponse("Admin tidak bisa memiliki penggalangan")

    context = dict()
    id_penggalangan = request.GET.get("id")
    data = query(
        f"""SELECT p.id, p.emailuser, p.judul, p.deskripsi, p.kota, p.provinsi, p.tanggalaktifakhir, p.jumlahdibutuhkan, p.statusverifikasi, emailadmin,
        k.namakategori, p.linkrepo, p.jumlahterkumpul, p.jumlahterpakai
        FROM penggalangan_dana_pd p JOIN kategori_pd k ON p.idkategori=k.id
        WHERE p.id='{id_penggalangan}'"""
    )
    context["p"] = data[0]
    context["tanggalaktifakhir"] = context["p"].tanggalaktifakhir.strftime("%Y-%m-%d")

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
        context["pasien"] = data_pasien[0]
        komorbid = query(
            f"""SELECT komorbid FROM komorbid
            WHERE idpd='{id_penggalangan}'"""
        )
        context["komorbid"] = komorbid
    if data[0].namakategori == "Rumah Ibadah":
        data_rumah_ibadah = query(
            f"""SELECT p.idrumahibadah, k.nama as kategori
            FROM pd_rumah_ibadah p JOIN kategori_aktivitas_pd_rumah_ibadah k
            ON p.idaktivitas=k.id
            WHERE idpd='{id_penggalangan}'"""
        )
        context["rumah_ibadah"] = data_rumah_ibadah[0]

        kategori_aktivitas = query(
            f"""SELECT id, nama
            FROM kategori_aktivitas_pd_rumah_ibadah
            """
        )
        print(kategori_aktivitas)
        context["kategori_aktivitas"] = kategori_aktivitas

    if request.method == "POST":
        body = request.POST
        result = query(
            f"""UPDATE penggalangan_dana_pd
        SET judul='{body["judul"]}',
        deskripsi='{body["deskripsi"]}',
        kota='{body["kota"]}',
        provinsi='{body["provinsi"]}',
        tanggalaktifakhir='{body["tanggalaktifakhir"]}',
        jumlahdibutuhkan='{body["jumlahdibutuhkan"]}',
        linkrepo='{body["linkrepo"]}'
        WHERE id='{body["id"]}'
        """
        )
        print("update penggalangan_dana_pd:", result)

        if body["namakategori"] == "Kesehatan":
            result = query(
                f"""UPDATE pd_kesehatan
            SET penyakit='{body["penyakit"]}'
            WHERE idpd='{body["id"]}'
            """
            )
            print("update pd_kesehatan:", result)
            query(
                f"""UPDATE pasien
            SET nik='{body["nik"]}',
            nama='{body["namapasien"]}',
            WHERE nik='{context["pasien"].nik}'
            """
            )
            print("update pasien:", result)

        elif body["namakategori"] == "Rumah Ibadah":
            result = query(
                f"""UPDATE pd_rumah_ibadah
                SET idrumahibadah='{body["idrumahibadah"]}',
                idaktivitas='{body["ri_kategori"]}'
                WHERE idpd='{body["id"]}'
                """
            )
            print("update pd_rumah_ibadah", result)

        return redirect("/t3/daftar-penggalangan-pribadi")
    return render(request, "form_update_penggalangan.html", context)


@csrf_exempt
def form_verifikasi_penggalangan(request):
    if not is_authenticated(request):
        return redirect("/auth/login?next=/t3/daftar-penggalangan-admin")

    if request.method == "POST":
        body = request.POST
        idpd = body["id"]
        timestamp = body["timestamp"]
        informasi = body["catatan"]
        action = body["action"]

        if action == "true":
            date = timestamp[:10]
            result = query(
                f"""UPDATE penggalangan_dana_pd
                SET emailadmin = '{request.session["email"]}',
                tanggalaktifawal = '{date}',
                sisahari = tanggalaktifakhir - '{date}'
                WHERE id = '{idpd}'"""
            )
            if result != 1:
                raise Exception("Error verifikasi on UPDATE penggalangan_dana_pd")

        result = query(
            f"""INSERT INTO catatan_pengajuan VALUES
                ('{idpd}', '{timestamp}', '{informasi}', {action})"""
        )
        return redirect("/t3/daftar-penggalangan-admin")

    context = {"id": request.GET.get("id")}
    return render(request, "form_verifikasi_penggalangan.html", context)


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
        context["pasien"] = data_pasien[0]
        komorbid = query(
            f"""SELECT komorbid FROM komorbid
            WHERE idpd='{id_penggalangan}'"""
        )
        context["komorbid"] = komorbid
    if data[0].namakategori == "Rumah Ibadah":
        data_rumah_ibadah = query(
            f"""SELECT p.idrumahibadah, k.nama as kategori
            FROM pd_rumah_ibadah p JOIN kategori_aktivitas_pd_rumah_ibadah k
            ON p.idaktivitas=k.id
            WHERE idpd='{id_penggalangan}'"""
        )
        context["rumah_ibadah"] = data_rumah_ibadah[0]
    return render(request, "detail_penggalangan.html", context)


@csrf_exempt
def form_create_kategori(request):
    if not is_authenticated(request):
        return redirect("/auth/login?next=/t3/create-kategori")

    if request.session["role"] != "admin":
        return HttpResponse("Hanya admin bisa mengakses halaman ini")

    if request.method == "POST":
        body = request.POST
        namakategori = body["namakategori"]
        
        query_str = f"INSERT INTO kategori_pd (namakategori, alias_kategori) VALUES ('{namakategori}', '{namakategori[0]}')"
        result = query(query_str)
        return redirect("/t3/kategori-penggalangan-admin/")

    context = query("SELECT id FROM KATEGORI_PD ORDER BY id DESC LIMIT 1")[0]
    latest_id = int(context.id) + 1
    context = {"latest_id": latest_id}
    return render(request, "form_create_kategori_penggalangan.html", context)


@csrf_exempt
def form_update_kategori(request):
    if not is_authenticated(request):
        return redirect("/auth/login?next=/t3/update-kategori-admin")

    if request.session["role"] != "admin":
        return HttpResponse("Hanya admin bisa mengakses halaman ini")

    id_kategori = request.GET.get("id")
    nama_kategori = request.GET.get("nama")
    if request.method == "POST":
        body = request.POST
        namakategori = body["namakategori"]
        query(
            f"""UPDATE kategori_pd
        SET namakategori='{namakategori}', alias_kategori='{namakategori[0]}' 
        WHERE id='{id_kategori}'"""
        )
        return redirect("/t3/kategori-penggalangan-admin")
    context = {"id_kategori": id_kategori, "nama_kategori": nama_kategori}
    return render(request, "form_update_kategori_penggalangan.html", context)


def kategori_penggalangan(request):
    if not is_authenticated(request):
        return redirect("/auth/login?next=/t3/kategori-penggalangan-admin")

    if request.session["role"] != "admin":
        return HttpResponse("Hanya admin bisa mengakses halaman ini")

    data = query("SELECT id, namakategori FROM kategori_pd")
    context = {"kategoris": data}
    return render(request, "admin_pov_daftar_kategori.html", context)