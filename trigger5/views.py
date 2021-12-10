from django.shortcuts import render
from django.http import response
from django.http.response import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

# Create your views here.


@csrf_exempt
def pencairanDana(request):
    context = dict()
    id_penggalangan = request.GET.get("id")
    data = query(
        f"""SELECT PD.SaldoDonaPay, PDD.Judul, PDD.JumlahTerpakai, PD.Email, PDD.Id FROM PENGGALANG_DANA PD, PENGGALANGAN_DANA_PD PDD
        WHERE PDD.id = '{id_penggalangan} AND PD.Email = PDD.EmailUser'
        """
    )
    context["data"] = data[0]
    if not is_authenticated(request):
        return redirect("/auth/login?next=/t3/create-kategori")
    if request.method == "POST":
        body = request.POST
        nominal = body["nominal"]
        new_saldo = body["saldo"] + nominal
        print(new_saldo)
        print(nominal)
        # belom dicek
        update_query1 = f"UPDATE PENGGALANG_DANA SET SaldoDonaPay = '{new_saldo}' WHERE EmailUser = '{context["data"].Email}'"
        update_query2 = f"UPDATE PENGGALANGAN_DANA_PD SET JumlahTerpakai = '{context["data"].JumlahTerpakai + nominal}' WHERE Judul = '{body["judul"]}'"
        update_query3 = f"INSERT INTO RIWAYAT_PENGGUNAAN_DANA(idPD, Timestamp, Nominal, Deskripsi) VALUES ('{context["data"].Id}','{nominal}','{body["keterangan"]}')"
        run_query1 = query(update_query1)
        run_query2 = query(update_query2)
        run_query3 = query(update_query3)
        return HttpResponseRedirect("/pd/details/")
    return render(request, 'pencairanDana.html', context)
