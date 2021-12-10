from datetime import datetime

from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt

from pengguna.views import get_session_data, is_authenticated
from utils.query import query


def read_pd(request):
    if not is_authenticated(request):
        return redirect("/auth/login?next=/pd")

    session = get_session_data(request)
    if session.get("role", "") not in ["individu", "organisasi"]:
        return HttpResponse("You are not authorized!")

    penggalangan_dana_pribadi = query(f"""
        SELECT * 
        FROM penggalangan_dana_pd AS pdpd, (
            SELECT id AS kategori_id, namakategori FROM kategori_pd
        ) AS k
        WHERE pdpd.emailuser = '{session["email"]}' AND pdpd.idkategori = k.kategori_id
    """)

    if type(penggalangan_dana_pribadi) != list:
        return HttpResponse("Failed to fetch Penggalangan Dana!")

    jumlah_pd_id = query(f"""
        SELECT jumlahpd, jumlahpdaktif
        FROM penggalang_dana
        WHERE email = '{session.get("email", "")}'
    """)

    if type(jumlah_pd_id) != list or len(jumlah_pd_id) != 1:
        return HttpResponse("Failed to fetch jumlah Penggalangan Dana!")

    jumlah_pd_id = jumlah_pd_id[0]

    data = {
        "penggalangan_dana": penggalangan_dana_pribadi, 
        "email": session.get("email", ""), 
        "jumlah_pd": jumlah_pd_id.jumlahpd, 
        "jumlah_pd_aktif": jumlah_pd_id.jumlahpdaktif
    }
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
        WHERE pdpd.id = d.idpd AND pdpd.id = '{id}'
    """)

    data["donasi"] = donasi

    return render(request, "read_pd_details.html", data)


@csrf_exempt
def create_pd(request):
    if not is_authenticated(request):
        return redirect(f"/auth/login?next=/pd/create")

    session = get_session_data(request)
    if session.get("role", "") not in ["individu", "organisasi"]:
        return HttpResponse("You are not authorized!")

    if request.method != "POST":
        return create_pd_view(request, session)

    body = request.POST

    pd_id = body.get("pdIdInput", "")
    email = body.get("pdEmailInput", "")
    judul = body.get("pdJudulInput", "")
    deskripsi = body.get("pdDeskripsiInput", "")
    kota = body.get("pdKotaInput", "")
    provinsi = body.get("pdProvinsiInput", "")
    deadline = body.get("pdDeadlinePenggalanganDanaInput", "")
    target_dana = body.get("pdJumlahTargetDanaInput", "")
    kategori_id = body.get("pdKategoriInput", "")
    berkas = body.get("pdBerkasInput", "")

    if not body or not (pd_id and email and judul and deskripsi and kota and provinsi and deadline and target_dana and kategori_id and berkas):
        return HttpResponse("Must provide request body!", status=400)

    current_time = datetime.today().strftime("%Y-%m-%d")
    insert = query(f"""
        INSERT INTO penggalangan_dana_pd VALUES
        ('{pd_id}', '{judul}', '{deskripsi}', '{kota}', '{provinsi}', '{berkas}', 'Belum Terverifikasi', 
        '{current_time}', null, '{deadline}', '{target_dana}', 0, 0, 0, '{email}', null, '{kategori_id}')
    """)

    if type(insert) != int:
        return HttpResponse("Failed to create new Penggalangan Dana!", status=500)

    return redirect("/pd")


def create_pd_view(request, session):
    kategori = query("SELECT * FROM kategori_pd")

    if type(kategori) != list or len(kategori) == 0:
        return HttpResponse("Failed to fetch Kategori Penggalangan Dana!", status=500)

    data = {"kategori": kategori, "email": session.get("email", "")}
    return render(request, "create_pd.html", data)


@csrf_exempt
def generate_id(request):
    if request.method != "POST":
        return HttpResponse("Must use POST method!", status=400)

    body = request.POST

    id_kategori = body.get("id_kategori_pd", "")
    alias_kategori = body.get("alias_kategori_pd", "")

    if not body or not (id_kategori and alias_kategori):
        return HttpResponse("Must provide request body!", status=400)

    id_kategori = body["id_kategori_pd"]
    alias_kategori = body["alias_kategori_pd"]

    id_pd = query(f"""
        SELECT id FROM penggalangan_dana_pd AS pdpd
        WHERE idkategori = '{id_kategori}'
    """)

    if type(id_pd) != list:
        return HttpResponse("Failed to fetch new Penggalangan Dana ID!", status=500)

    if len(id_pd) == 0:
        return JsonResponse({"id": f"{alias_kategori}-001"})

    id_terakhir = int(id_pd[-1].id.split("-")[-1])
    return JsonResponse({"id": f"{alias_kategori}-{id_terakhir + 1:03d}"})


@csrf_exempt
def create_pasien(request):
    if request.method != "POST":
        return HttpResponse("Must use POST method!", status=400)

    body = request.POST

    nik = body.get("nik", "")
    nama = body.get("nama", "")
    tanggal_lahir = body.get("tanggalLahir", "")
    alamat = body.get("alamat", "")
    pekerjaan = body.get("pekerjaan", "")

    if not body or not (nik and nama and tanggal_lahir and alamat and pekerjaan):
        return HttpResponse("Must provide request body!", status=400)

    insert = query(f"""
        INSERT INTO pasien VALUES
        ('{nik}', '{nama}', '{tanggal_lahir}', '{alamat}', '{pekerjaan}')
    """)

    if type(insert) != int:
        return HttpResponse("Failed to create new Pasien!", status=500)

    return HttpResponse("success", status=200)


@csrf_exempt
def get_kategori(_):
    kategori = query("SELECT * FROM kategori_pd")
    kategori = [{
        "id": k.id,
        "nama": k.namakategori,
        "alias": k.alias_kategori
    } for k in kategori]

    return JsonResponse({"kategori": kategori})
