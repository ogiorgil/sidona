from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt

from utils.query import query


def is_authenticated(request):
    try:
        request.session['email']
        return True
    except KeyError:
        return False


def get_role(email, password):
    admin_query = query(
        f"SELECT email FROM ADMIN WHERE email = '{email}' AND password = '{password}'")
    if type(admin_query) == list and len(admin_query):
        return "admin"

    pd_query = query(
        f"SELECT email FROM PENGGALANG_DANA WHERE email = '{email}' AND password = '{password}'")
    if type(pd_query) == list and len(pd_query):
        individu_query = query(
            f"SELECT email FROM INDIVIDU WHERE email = '{email}'")
        if type(individu_query) == list and len(individu_query):
            return "individu"
        else:
            return "organisasi"

    return ""


def get_session_data(request):
    if not is_authenticated(request):
        return {}

    try:
        return {"email": request.session["email"], "role": request.session["role"]}
    except:
        return {}


@csrf_exempt
def login(request):
    next = request.GET.get('next')

    if request.method != "POST":
        return login_view(request)

    if is_authenticated(request):
        email = str(request.session['email'])
        password = str(request.session['password'])
    else:
        email = str(request.POST['email'])
        password = str(request.POST['password'])

    role = get_role(email, password)

    if (role == ""):
        return login_view(request)
    else:
        request.session['email'] = email
        request.session['password'] = password
        request.session['role'] = role
        request.session.set_expiry(0)
        request.session.modified = True

        if (next != None and next != "None"):
            return redirect(next)
        else:
            return redirect("/t3/daftar-penggalangan")


def login_view(request):
    if is_authenticated(request):
        return redirect("/t3/daftar-penggalangan")

    return render(request, "login.html")


def logout(request):
    next = request.GET.get('next')

    if not is_authenticated(request):
        return redirect("/t3/daftar-penggalangan")

    request.session.flush()
    request.session.clear_expired()

    if (next != None and next != "None"):
        return redirect(next)
    else:
        return redirect("/t3/daftar-penggalangan")


@csrf_exempt
def register(request):
    if is_authenticated(request):
        return redirect("/t3/daftar-penggalangan")

    if request.method != "POST":
        return register_view(request)

    role1 = str(request.POST['role1'])
    if role1 == "admin":
        return register_admin(request)
    else:
        return register_pd(request)


@csrf_exempt
def register_admin(request):
    next = request.GET.get('next')
    body = request.POST

    email = body["adminEmailInput"]
    password = body["adminPasswordInput"]
    name = body["adminNamaInput"]
    nomorhp = body["adminNoHpInput"]

    result = query(f"""
        INSERT INTO admin VALUES
        ('{email}', '{password}', '{name}', '{nomorhp}')
    """)

    if not type(result) == int:
        return HttpResponse("Anda gagal registrasi!")

    request.session['email'] = email
    request.session['password'] = password
    request.session['role'] = 'admin'
    request.session.set_expiry(0)
    request.session.modified = True

    if (next != None and next != "None"):
        return redirect(next)
    else:
        return redirect("/t3/daftar-penggalangan")


@csrf_exempt
def register_pd(request):
    role2 = str(request.POST['role2'])
    if role2 == "individu":
        return register_individu(request)
    else:
        return register_organisasi(request)


@csrf_exempt
def register_individu(request):
    next = request.GET.get('next')
    body = request.POST

    email = body["pdEmailInput"]
    password = body["pdPasswordInput"]
    nama = body["pdNamaInput"]
    no_hp = body["pdNoHpInput"]
    alamat = body["pdAlamatInput"]

    nama_bank = body["pdNamaBankInput"]
    no_rekening = body["pdNomorRekeningInput"]

    nik = body["pdiNikInput"]
    tanggal_lahir = body["pdiTanggalLahirInput"]
    jenis_kelamin = body["pdiJenisKelaminInput"]
    foto_ktp = body["pdiKtpInput"]

    result = query(f"""
        INSERT INTO penggalang_dana VALUES
        ('{email}', '{password}', '{nama}', '{no_hp}', '{alamat}', 0, '{no_rekening}', '{nama_bank}', '{foto_ktp}', 0, 
        0, 'Belum Terverifikasi', null)
    """)
    print("PENGGALANG_DANA:", result)
    if not type(result) == int:
        return HttpResponse("Anda gagal registrasi!")

    result = query(f"""
        INSERT INTO individu VALUES
        ('{email}', '{nik}', '{tanggal_lahir}', '{jenis_kelamin}', 0)
    """)
    print("INDIVIDU", result)

    request.session['email'] = email
    request.session['password'] = password
    request.session['role'] = 'individu'
    request.session.set_expiry(0)
    request.session.modified = True

    if (next != None and next != "None"):
        return redirect(next)
    else:
        return redirect("/t3/daftar-penggalangan")


@csrf_exempt
def register_organisasi(request):
    body = request.POST

    email = body["pdEmailInput"]
    password = body["pdPasswordInput"]
    nama = body["pdNamaInput"]
    no_hp = body["pdNoHpInput"]
    alamat = body["pdAlamatInput"]

    nama_bank = body["pdNamaBankInput"]
    no_rekening = body["pdNomorRekeningInput"]

    nama_org = body["pdoNamaInput"]
    no_telp_org = body["pdoNoTelpInput"]
    tahun_berdiri_org = body["pdoTahunInput"]
    no_akta_pendirian_org = body["pdoNomorAktaInput"]
    foto_akta_pendirian_org = body["pdoFotoAktaInput"]

    query_str = query(f"""
        INSERT INTO penggalang_dana VALUES
        ('{email}', '{password}', '{nama}', '{no_hp}', '{alamat}', 0, '{no_rekening}', '{nama_bank}', '{foto_akta_pendirian_org}', 
        {0}, {0}, 'Belum Terverifikasi', null)
        """)
    result = query(query_str)

    if not type(result) == int:
        return HttpResponse("Anda gagal registrasi!")

    query_str = f"""
        INSERT INTO organisasi VALUES
        ('{email}', '{no_akta_pendirian_org}', '{nama_org}', '{no_telp_org}', '{tahun_berdiri_org}')
        """
    query(query_str)

    request.session['email'] = email
    request.session['password'] = password
    request.session['role'] = 'organisasi'
    request.session.set_expiry(0)
    request.session.modified = True

    if (next != None and next != "None"):
        return redirect(next)
    else:
        return redirect("/t3/daftar-penggalangan")


def register_view(request):
    return render(request, "register.html")


def read_pengguna(request):
    return render(request, "read_pengguna.html")


def tabel_daftar_pengguna(request):
    return render(request, "tabel_daftar_pengguna.html")


def admin_pov_read_pengguna(request):
    return render(request, "admin_pov_read_pengguna.html")
