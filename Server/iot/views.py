from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required(login_url='/login/')
def lab_one(request):
	return render(request,'lab_one_dashboard.html',{'title':'Laboratorio_uno'})

@login_required(login_url='/login/')
def lab_two(request):
	return render(request,'lab_two_dashboard.html',{'title':'Laboratorio_dos'})
