from django.shortcuts import render
from .models import *



def bc_list(request):
	bcs = Bc.objects.all()
	return render(request, 'bcs/bc_list.html', {'bcs':bcs})
