from django.shortcuts import render

from django.shortcuts import render

def perfil_view(request):
    return render(request, "perfil.html")

def profile_view(request):
    return render(request, "profile.html")

def edit_profile_view(request):
    return render(request, "edit_profile.html")
