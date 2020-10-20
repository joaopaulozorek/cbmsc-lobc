from django.shortcuts import render, get_object_or_404
from .models import *



def bc_list(request):
	bcs = Bc.objects.all()
	return render(request, 'bcs/bc_list.html', {'bcs':bcs})	

def bc_detail(request, user):
	usuario = get_object_or_404(Usuario, usu_user__username=user)
	print(usuario)
	bc = get_object_or_404(Bc, bc_usuario=usuario.pk)
	print(bc)

	return render(request,'bcs/bc_detail.html',{'bc':bc})