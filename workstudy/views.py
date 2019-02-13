from django.shortcuts import render
from django.http import HttpResponse

# import tables from the database
from workstudy.models import PersonalInfo, AppData, AppAvailability,StudentPlacement, StudentSchedule, SiteInfo, SiteAvailability 

# Create your views here.
def index(request):
	
	return HttpResponse("hello world")#hold html page
	
def search(request):
	pass
	
def add(request):
	pass
