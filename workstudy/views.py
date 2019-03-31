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

# This function is still in progress
def search(request):
	# Calculates the current and next two semesters to populate search criteria
	current_year = datetime.datetime.now().year
	choices = [
		("Spring " + str(current_year)),
		("Fall " + str(current_year)),
		("Spring " + str(current_year + 1))
	]

	general = request.GET.get('a')
	name = request.GET.get('q')
	email = request.GET.get('r')
	semester = request.GET.get('s')
	driver = request.GET.get('t')
	day = request.GET.get('u')
	starttime = request.GET.get('v')
	endtime = request.GET.get('w')

	# Initialize results to dispaly all items in database
	personalInfoResults = PersonalInfo.objects.none()
	appDataResults = PersonalInfo.objects.none()
	appAvailabilityResults = PersonalInfo.objects.none()

	if general:
		personalInfoSearch =  PersonalInfo.objects.filter(Q(student_id__icontains=general) |
		Q(first_name__icontains=general) | Q(preferred_name__icontains=general) | Q(last_name__icontains=general) |
		Q(email__icontains=general))
		appDataSearch = AppData.objects.filter(Q(semester__icontains=general) |
		Q(phone_num__icontains=general) | Q(grad_month__icontains=general) | Q(grad_year__icontains=general) |
		Q(what_class__icontains=general) | Q(wanted_hours__icontains=general) |
		Q(major__icontains=general) | Q(languages__icontains=general) | Q(prior_work__icontains=general) |
		Q(previous_site__icontains=general) | Q(hear_about_ccec__icontains=general))
		appAvailabilitySearch = AppAvailability.objects.filter(Q(day__icontains=general) | Q(start_time__icontains=general) |
		Q(end_time__icontains=general))

		if personalInfoSearch:
			personalInfoResults = personalInfoSearch
		elif appDataSearch:
			temp = PersonalInfo.objects.none()
			for app in appDataSearch:
				person = PersonalInfo.objects.filter(Q(student_id = app.personal_info.student_id))
				temp = person.union(temp)
			appDataResults = temp
		elif appAvailabilitySearch:
			temp = PersonalInfo.objects.none()
			for app in appAvailabilitySearch:
				person = PersonalInfo.objects.filter(Q(student_id = app.personal_info.student_id))
				temp = person.union(temp)
			appAvailabilityResults = temp
	else:
		# Advanced search
		results = PersonalInfo.objects.all()
		# nameSearch = PersonalInfo.objects.none()
		# emailSearch = PersonalInfo.objects.none()
		# semesterData = PersonalInfo.objects.none()
		# semesterSearch = PersonalInfo.objects.none()

		if name:
			print("name")
			nameSearch = results.filter(Q(first_name__icontains=name) | Q(preferred_name__icontains=name) |
			Q(last_name__icontains=name))
			results = nameSearch
		if email:
			print("email")
			emailSearch = results.filter(Q(email__icontains=email))
			results = emailSearch
		if semester:
			print("semester")
			semesterData = AppData.objects.filter(Q(semester__icontains=semester))
			temp = PersonalInfo.objects.none()
			for sem in semesterData:
				semesterSearch = results.filter(Q(student_id = sem.personal_info.student_id))
				temp = semesterSearch.union(temp)
			results = temp
		if not driver is None:
			print("driver")
			driverData = AppData.objects.filter(Q(car=True) & Q(carpool=True))
			temp = PersonalInfo.objects.none()
			for driver in driverData:
				driverSearch = results.filter(Q(student_id = driver.personal_info.student_id))
				temp = driverSearch.union(temp)
			results = temp
		if day:
			print("day")
			dayData = AppAvailability.objects.filter(Q(day__icontains=day))
			temp = PersonalInfo.objects.none()
			for d in dayData:
				daySearch = results.filter(Q(student_id = d.app_data.personal_info.student_id))
				print(daySearch)
				temp = daySearch.union(temp)
			results = temp
		if starttime:
			print("start time")
			startData = AppAvailability.objects.filter(Q(start_time__icontains=starttime))
			temp = PersonalInfo.objects.none()
			for start in startData:
				startSearch = results.filter(Q(student_id = start.app_data.personal_info.student_id))
				temp = startSearch.union(temp)
			results = temp
		if endtime:
			print("end time")
			endData = AppAvailability.objects.filter(Q(end_time__icontains=endtime))
			temp = PersonalInfo.objects.none()
			for end in endData:
				endSearch = results.filter(Q(student_id = end.app_data.personal_info.student_id))
				temp = endSearch.union(temp)
			results = temp

		personalInfoResults = results

	context = {
		'PerInfo': personalInfoResults,
		'AppData': appDataResults,
		'AppAvail': appAvailabilityResults,
		'years': choices
	}

	return render(request, "search.html", context)

def add(request):
	pass

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
