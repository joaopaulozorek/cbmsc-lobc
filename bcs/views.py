from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm
from .models import *



def bc_list(request):
	bcs_por_cidade()
	bcs = Bc.objects.all()
	return render(request, 'bcs/bc_list.html', {'bcs':bcs})	

def bc_detail(request, user):
	usuario = get_object_or_404(Usuario, usu_user__username=user)
	print(usuario)
	bc = get_object_or_404(Bc, bc_usuario=usuario.pk)
	print(bc)

	return render(request,'bcs/bc_detail.html',{'bc':bc})


def bcs_por_cidade():
	q = Bc.objects.all()

	print(q)


def cadastro_usuario(request):
	if request.method == "POST":
		form_usuario = UserCreationForm(request.POST)
		if form_usuario.is_valid():
			form_usuario.save()
			return redirect('bc_list')
	else:
		form_usuario = UserCreationForm()
		return render(request, 'bcs/register.html', {'form_usuario': form_usuario})
