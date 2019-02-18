from django.shortcuts import render
from django.http import HttpResponse
from .forms import PersonalInfoForm, AppDataForm, AppAvailabilityForm, SitePlacementRankForm

# import tables from the database
from workstudy.models import PersonalInfo, AppData, AppAvailability,StudentPlacement, StudentSchedule, SiteInfo, SiteAvailability

# Create your views here.
#def index(request):

#	return HttpResponse("hello world")#hold html page

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
		items = PersonalInfo.objects.all()
		return render(request, "my_template.html", {'items': items})
