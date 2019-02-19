from django.shortcuts import render
from django.http import HttpResponse
from .forms import PersonalInfoForm, AppDataForm, AppAvailabilityForm, SitePlacementRankForm

# import tables from the database
from workstudy.models import PersonalInfo, AppData, AppAvailability,StudentPlacement, StudentSchedule, SiteInfo, SiteAvailability

# Create your views here.
#def index(request):

#	return HttpResponse("hello world")#hold html page

#add how many total hours a student worked per semester
#add how many total hours worked at each sites per semester


def search(request):
	pass

def add(request):
	pass

def application (request):
	form = PersonalInfoForm()
	return render (request, 'pages/application.html', {'form' : form})

def index(request):

	if request.method == "POST":
		form = PersonalInfoForm(request.POST)
		if form.is_valid():
			model_instance = form.save(commit=False)
			model_instance = instance.timestamp = timezone.now()
			model_instance.save()
			return redirect('')
			#render(request, "my_template.html", {'items': items})
	else:
		form = PersonalInfoForm()
		return render(request, "my_template.html", {'form': form})
