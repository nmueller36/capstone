from django.shortcuts import render
from django.http import HttpResponse
from .forms import PersonalInfoForm, AppDataForm, AppAvailabilityForm, SitePlacementRankForm
from django.db.models import Q

from django.shortcuts import redirect

from django.contrib import messages

# import tables from the database
from workstudy.models import PersonalInfo, AppData, AppAvailability,StudentPlacement, StudentSchedule, SiteInfo, SiteAvailability

def index(request):
	return render(request, "index.html", {})

def application_completed(request):
	return render(request, "completed.html", {})

def search(request):
	# template = 'pages/search.html'

	query = request.GET.get('q')

	if query:
		results = AppAvailability.objects.filter(Q(day__icontains=query))
	else:
		results = AppAvailability.objects.all()

	context = {
		'items': results
	}

	return render(request, "search.html", context)

def add(request):
	pass

def application(request):
	if request.method == "POST":
		personal_info_form = PersonalInfoForm(request.POST)
		app_data_form = AppDataForm(request.POST)
		site_placement_rank_form = SitePlacementRankForm(request.POST)

		if personal_info_form.is_valid() and app_data_form.is_valid() and site_placement_rank_form.is_valid():
			personal_info_instance = personal_info_form.save(commit=False)
			app_data_instance = app_data_form.save(commit=False)
			site_placement_rank_instance = site_placement_rank_form.save(commit=False)
			# here you can add more fields or change them the way you want, after that you will save them
			app_data_instance.personal_info = personal_info_instance
			site_placement_rank_instance.app_data = app_data_instance

			personal_info_instance.save()
			app_data_instance.save()
			site_placement_rank_instance.save()

			# return redirect('workstudy:application-details', pk=app_data_instance.pk)
			return redirect('workstudy:application-completed')
		# if the form validation failed, for now just show the application form again and show the error
		else:
			messages.warning(request, 'You filled up the form incorrectly, please try again. It has not been saved.')
			return redirect('workstudy:application')
	else:
		# show the forms
		context = {}
		personal_info_form = PersonalInfoForm()
		app_data_form = AppDataForm()
		site_placement_rank_form = SitePlacementRankForm()
		context['personal_info_form'] = personal_info_form
		context['app_data_form'] = app_data_form
		context['site_placement_rank_form'] = site_placement_rank_form
		return render(request, 'application.html', context)
