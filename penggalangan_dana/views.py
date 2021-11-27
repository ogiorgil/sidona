from django.shortcuts import render


def create_pd(request):
    return render(request, "create_pd.html")

def read_pd(request):
    return render(request, "read_pd.html")

def read_pd_details(request):
    return render(request, "read_pd_details.html")
