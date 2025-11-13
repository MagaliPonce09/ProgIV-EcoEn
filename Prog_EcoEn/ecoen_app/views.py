from .models import Opinion
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from .models import Producto
from django.contrib.auth.decorators import login_required
from .models import Producto, Opinion, Compra, Puntuacion
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from .models import Perfil
from .forms import EditarPerfilForm
from django.contrib import messages
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from openai import AzureOpenAI
from django.conf import settings

# Configura tu API key (mejor usar variables de entorno)
client = AzureOpenAI(
    api_key=settings.AZURE_OPENAI_API_KEY,
    azure_endpoint=settings.AZURE_OPENAI_ENDPOINT,
    api_version=settings.AZURE_OPENAI_API_VERSION,
    )

@csrf_exempt
def chatbot_view(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user_message = data.get("message", "")

        response = client.chat.completions.create(
            model="gpt-4o-mini",  # motor que usa Copilot
            messages=[{"role": "user", "content": user_message}]
        )

        bot_reply = response.choices[0].message.content
        return JsonResponse({"reply": bot_reply})



def index(request):
    productos = Producto.objects.all()
    puntuaciones_usuario = {}

    if request.user.is_authenticated:
        puntuaciones = Puntuacion.objects.filter(usuario=request.user)
        puntuaciones_usuario = {p.producto_id: p.valor for p in puntuaciones}

    for producto in productos:
        producto.puntuacion_usuario = puntuaciones_usuario.get(producto.id, 0)

    opiniones = Opinion.objects.all()  # ✅ Agregado

    context = {
        "productos": productos,
        "opiniones": opiniones,  # ✅ Agregado
    }
    return render(request, "index.html", context)

def iniciar_sesion(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            usuario = form.get_user()
            login(request, usuario)
            return redirect("productos")
    else:
        form = AuthenticationForm()
    return render(request, "login.html", {"form": form})

def cerrar_sesion(request):
    logout(request)
    return redirect("index")


def productos(request):
    query = request.GET.get("q", "")
    productos = Producto.objects.filter(nombre__icontains=query) if query else Producto.objects.all()

    puntuaciones_usuario = {}
    if request.user.is_authenticated:
        puntuaciones = Puntuacion.objects.filter(usuario=request.user)
        puntuaciones_usuario = {p.producto_id: p.valor for p in puntuaciones}

    for producto in productos:
        producto.puntuacion_usuario = puntuaciones_usuario.get(producto.id, 0)

    return render(request, "producto.html", {"productos": productos, "query": query})

@login_required
def crear_producto(request):
    if not request.user.perfil.es_vendedor:
        return redirect("productos")

    if request.method == "POST":
        nombre = request.POST.get("nombre")
        descripcion = request.POST.get("descripcion")
        precio = request.POST.get("precio")
        imagen = request.FILES.get("imagen")

        if nombre and descripcion and precio and imagen:
            Producto.objects.create(
                nombre=nombre,
                descripcion=descripcion,
                precio=precio,
                imagen=imagen,
                vendedor=request.user
            )
            return redirect("productos")

    return render(request, "crear_producto.html")

def enviar_opinion(request):
    if request.method == "POST":
        mensaje = request.POST.get("mensaje")
        if mensaje and request.user.is_authenticated:
            Opinion.objects.create(nombre=request.user.username, mensaje=mensaje)
    return redirect("inicio")

@login_required
def carrito(request):
    mostrar_pago = request.GET.get("comprar") == "1"
    return render(request, "carrito.html", {"mostrar_pago": mostrar_pago})


def confirmar_pago(request, metodo):
    if not request.user.is_authenticated:
        return redirect("login")

    # Simulación: guardar una compra ficticia
    Compra.objects.create(
        usuario=request.user,
        metodo_pago=metodo,
        total=calcular_total_carrito(request),  # función que suma los ítems
        estado="simulado"
    )

    return redirect(f"/?confirmacion=1&metodo={metodo}")

def calcular_total_carrito(request):
    # Simulación: suma ficticia de ítems del carrito
    # En producción, deberías sumar los precios reales desde sesión o base de datos
    return 1000.00  # valor simulado en ARS

def registro(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")  # o redirigí a donde quieras
    else:
        form = UserCreationForm()
    return render(request, "registro.html", {"form": form})

def producto_detalle(request, id):
    producto = get_object_or_404(Producto, id=id)
    puntuacion_usuario = 0
    if request.user.is_authenticated:
        try:
            puntuacion_usuario = Puntuacion.objects.get(producto=producto, usuario=request.user).valor
        except Puntuacion.DoesNotExist:
            pass
    return render(request, "detalle_producto.html", {
        "producto": producto,
        "puntuacion_usuario": puntuacion_usuario
    })

@login_required
def mi_perfil(request):
    perfil, creado = Perfil.objects.get_or_create(user=request.user)
    compras = Compra.objects.filter(usuario=request.user).order_by("-fecha")
    opiniones = Opinion.objects.filter(nombre=request.user.username).order_by("-fecha")

    return render(request, "perfil.html", {
        "perfil": perfil,
        "compras": compras,
        "opiniones": opiniones
    })

@login_required
def editar_perfil(request):
    perfil = request.user.perfil

    if request.method == "POST":
        form = EditarPerfilForm(request.POST, request.FILES, instance=perfil, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Perfil actualizado correctamente.")
            return redirect("mi_perfil")
        else:
            messages.error(request, "Hubo un error al actualizar tu perfil.")
    else:
        form = EditarPerfilForm(instance=perfil, user=request.user)

    return render(request, "editar_perfil.html", {"form": form})
