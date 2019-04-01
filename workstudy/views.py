from django.shortcuts import render
from django.http import HttpResponse
from .forms import PersonalInfoForm, AppDataForm, SitePlacementRankForm, SiteInfoForm, AppAvailabilityForm
from django.db.models import Q
from itertools import chain
import datetime

from django.shortcuts import redirect

from django.contrib import messages

# import tables from the database
from workstudy.models import PersonalInfo, AppData, AppAvailability,StudentPlacement, StudentSchedule, SiteInfo, SiteAvailability

def index(request):
	return render(request, "index.html", {})

def application_completed(request):
	return render(request, "completed.html", {})

def new_site_completed(request):
	return render(request, "new_site.html", {})

# This function is still in progress
def search(request):

	current_year = datetime.datetime.now().year
	choices = [(year, year) for year in range(current_year, current_year + 8)]

	query = request.GET.get('q')
	query2 = request.GET.get('r')
	query3 = request.GET.get('s')
	query4 = request.GET.get('t')

	if query:
		personalInfoResults = PersonalInfo.objects.filter(Q(student_id__icontains=query) |
		Q(first_name__icontains=query) | Q(preferred_name__icontains=query) | Q(last_name__icontains=query) |
		Q(email__icontains=query))
		appDataResults = AppData.objects.filter(Q(semester__icontains=query) |
		Q(phone_num__icontains=query) | Q(grad_month__icontains=query) | Q(grad_year__icontains=query) |
		Q(what_class__icontains=query) | Q(semester__icontains=query) | Q(wanted_hours__icontains=query) |
		Q(major__icontains=query) | Q(languages__icontains=query) | Q(prior_work__icontains=query) |
		Q(previous_site__icontains=query) | Q(hear_about_ccec__icontains=query))
		if personalInfoResults:
			results = personalInfoResults
		elif appDataResults:
			temp = PersonalInfo.objects.none()
			for app in appDataResults:
				person = PersonalInfo.objects.filter(Q(student_id__icontains = app.personal_info.student_id))
				temp = person.union(temp)
				# results = Q(person | temp)
			results = temp
		else:
			results = ""
	else:
		results = PersonalInfo.objects.all()
	if query2:
		pass

	context = {
		'items': results,
		'years': choices
	}

	return render(request, "search.html", context)

def add(request):
	pass

def placement(request):
	return render(request, "placement.html", {})

def application(request):
	#template_name = 'pages/create_normal.html'
	if request.method == "POST":
		personal_info_form = PersonalInfoForm(request.POST)
		app_data_form = AppDataForm(request.POST)
		site_placement_rank_form = SitePlacementRankForm(request.POST)
		app_availbility_modelformset = AppAvailabilityModelFormset(request.POST) #, request.FILES, prefix = 'availility')
		#formset = AuthorFormset(request.POST)

		if personal_info_form.is_valid() and app_data_form.is_valid() and site_placement_rank_form.is_valid() and app_availbility_modelformset.is_vaild():
			personal_info_instance = personal_info_form.save(commit=False)
			app_data_instance = app_data_form.save(commit=False)
			site_placement_rank_instance = site_placement_rank_form.save(commit=False)
			# here you can add more fields or change them the way you want, after that you will save them
			app_data_instance.personal_info = personal_info_instance
			site_placement_rank_instance.app_data = app_data_instance

			personal_info_instance.save()
			app_data_instance.save()
			site_placement_rank_instance.save()
			for form in app_availbility_modelformset:
				# so that `book` instance can be attached.
				app_availbility_instance = app_availbility_modelformset.save(commit=False)
				app_availbility_instance.app_data = app_data_instance
				app_availbility_instance.day = day
				app_availbility_instance.start_time = start_time
				app_availbility_instance.end_time = end_time
				app_availbility_instance.save()
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
		app_availability_form = AppAvailabilityForm()
		context['personal_info_form'] = personal_info_form
		context['app_data_form'] = app_data_form
		context['site_placement_rank_form'] = site_placement_rank_form
		context['app_availability_form'] = app_availability_form
		return render(request, 'application.html', context)


def site_info_added (request):
	return render(request, "new_site.html", {})

def site_information (request):
	if request.method == "POST":
		site_info_form = SiteInfoForm(request.POST)

		if site_info_form.is_valid():
			site_info_instance = site_info_form.save(commit=False)
			site_info_instance.save()
			return redirect('workstudy:new_site')
		else:
			messages.warning(request, 'You filled up the form incorrectly, please try again. It has not been saved.')
			return redirect('workstudy:add_site_info')

	else:
		# show the forms
		context = {}
		site_info_form = SiteInfoForm()
		context['site_info_form'] = site_info_form
		return render(request, 'add_site_info.html', context)
