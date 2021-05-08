from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'index.html')

def Vista_Peticiones(request):
    return render(request, 'Vista_Peticiones.html')

def Datos_Personales(request):
    return render(request, 'datosPersonales.html')