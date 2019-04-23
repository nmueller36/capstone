from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from .forms import PersonalInfoForm, AppDataForm, SitePlacementRankForm, SiteInfoForm, AppAvailabilityForm, SiteAvailabilityForm, StudentPlacementForm, StudentScheduleForm
from django.db.models import Q
from itertools import chain
import datetime

from django.urls import reverse

# add imports for login and logout
from django.contrib.auth import authenticate, login, logout

from django.shortcuts import redirect

from django.contrib import messages

# import tables from the database
from workstudy.models import PersonalInfo, AppData, SitePlacementRank, AppAvailability, SiteAvailability, SiteInfo, \
	StudentPlacement, StudentSchedule


def index(request):
	return render(request, "index.html", {})


def application_completed(request):
	return render(request, "completed.html", {})


def new_site_completed(request):
	return render(request, "new_site.html", {})


# This function is still in progress
def search(request):
	# Calculates the current and next two semesters to populate search criteria
	current_year = datetime.datetime.now().year
	choices = [
		("Spring " + str(current_year)),
		("Fall " + str(current_year)),
		("Spring " + str(current_year + 1))]
	whichSearch = 0

	general = request.GET.get('a')
	firstname = request.GET.get('p')
	lastname = request.GET.get('q')
	email = request.GET.get('r')
	semester = request.GET.get('s')
	driver = request.GET.get('t')
	day = request.GET.get('u')
	starttime = request.GET.get('v')
	endtime = request.GET.get('w')

	# Initialize results to display all items in database
	personalInfoResults = PersonalInfo.objects.none()
	appDataResults = PersonalInfo.objects.none()
	appAvailabilityResults = PersonalInfo.objects.none()

	if general != None and general != "":
		whichSearch = 1
		personalInfoSearch = PersonalInfo.objects.filter(Q(student_id__icontains=general) |
			Q(first_name__icontains=general) | Q(preferred_name__icontains=general) | Q(last_name__icontains=general) |
			Q(email__icontains=general))
		appDataSearch = AppData.objects.filter(Q(semester__icontains=general) |
			Q(phone_num__icontains=general) | Q(grad_month__icontains=general) |
			Q(grad_year__icontains=general) | Q(what_class__icontains=general) |
			Q(wanted_hours__icontains=general) | Q(major__icontains=general) |
			Q(languages__icontains=general) | Q(prior_work__icontains=general) |
			Q(previous_site__icontains=general) | Q(hear_about_ccec__icontains=general))
		appAvailabilitySearch = AppAvailability.objects.filter(Q(day__icontains=general) |
			Q(start_time__icontains=general) | Q(end_time__icontains=general))

		if personalInfoSearch:
			personalInfoResults = personalInfoSearch
		elif appDataSearch:
			temp = PersonalInfo.objects.none()
			for app in appDataSearch:
				person = PersonalInfo.objects.filter(Q(student_id=app.personal_info.student_id))
				temp = person.union(temp)
			appDataResults = temp
		elif appAvailabilitySearch:
			temp = PersonalInfo.objects.none()
			for app in appAvailabilitySearch:
				person = PersonalInfo.objects.filter(Q(student_id=app.personal_info.student_id))
				temp = person.union(temp)
			appAvailabilityResults = temp
	else:
		# Advanced search
		results = PersonalInfo.objects.all()

		# Make sure spaces/full names accounted for
		if firstname:
			print("first name")
			firstname = firstname.strip()
			firstNameSearch = results.filter(Q(first_name__icontains=firstname) | Q(preferred_name__icontains=firstname))
			results = firstNameSearch
			whichSearch = 2
		if lastname:
			print("last name")
			lastname = lastname.strip()
			lastNameSearch = results.filter(Q(last_name__icontains=lastname))
			results = lastNameSearch
			whichSearch = 2
		if email:
			print("email")
			email = email.strip()
			emailSearch = results.filter(Q(email__icontains=email))
			results = emailSearch
			whichSearch = 2
		if semester:
			print("semester")
			wanted_items = set()
			for entry in results:
				if entry.appdata_set.filter(Q(semester__icontains=semester)).count() > 0:
					wanted_items.add(entry.student_id)
			results = PersonalInfo.objects.filter(student_id__in=wanted_items)
			whichSearch = 2
		if driver is not None:
			print("driver")
			# check if the results contain the drivers and if not, do not add them
			wanted_items = set()
			for entry in results:
				if entry.appdata_set.filter(car=True).count() > 0:
					wanted_items.add(entry.student_id)
			results = PersonalInfo.objects.filter(student_id__in=wanted_items)
			whichSearch = 2
		if day:
			print("day")
			wanted_items = set()
			for entry in results:
				apps = entry.appdata_set.all()
				for app in apps:
					if app.appavailability_set.filter(Q(day__icontains=day)).count() > 0:
						wanted_items.add(entry.student_id)
			results = PersonalInfo.objects.filter(student_id__in=wanted_items)
			whichSearch = 2
		if starttime:
			print("start time")
			wanted_items = set()
			for entry in results:
				apps = entry.appdata_set.all()
				for app in apps:
					if app.appavailability_set.filter(Q(start_time__lte=starttime)).count() > 0:
						wanted_items.add(entry.student_id)
			results = PersonalInfo.objects.filter(student_id__in=wanted_items)
			whichSearch = 2
		if endtime:
			print("end time")
			wanted_items = set()
			for entry in results:
				apps = entry.appdata_set.all()
				for app in apps:
					if app.appavailability_set.filter(Q(end_time__gte=endtime)).count() > 0:
						wanted_items.add(entry.student_id)
			results = PersonalInfo.objects.filter(student_id__in=wanted_items)
			whichSearch = 2

		personalInfoResults = results

	context = {
		'PerInfo': personalInfoResults,
		'AppData': appDataResults,
		'AppAvail': appAvailabilityResults,
		'years': choices,
		'searchType': whichSearch
	}

	return render(request, "search.html", context)


def student_placement_search(request):
	whichSearch = 0

	general = request.GET.get('a')
	firstname = request.GET.get('p')
	lastname = request.GET.get('q')
	email = request.GET.get('r')

	# Initialize results to display all items in database
	personalInfoResults = PersonalInfo.objects.none()
	studentPlacementResults = PersonalInfo.objects.none()
	studentScheduleResults = PersonalInfo.objects.none()

	if general != None and general != "":
		whichSearch = 1
		personalInfoSearch = PersonalInfo.objects.filter(Q(student_id__icontains=general) |
			Q(first_name__icontains=general) | Q(preferred_name__icontains=general) | Q(last_name__icontains=general) |
			Q(email__icontains=general))
		studentPlacementSearch = StudentPlacement.objects.filter(Q(driver__icontains=general) |
			Q(started__icontains=general) | Q(fbi_fingerprint__icontains=general) | Q(child_abuse__icontains=general) |
			Q(state_police__icontains=general) | Q(physical__icontains=general)  | Q(ppd__icontains=general)  |
			Q(comments__icontains=general))
		studentScheduleSearch = StudentSchedule.objects.filter(Q(day__icontains=general) |
			Q(start_time__icontains=general) | Q(end_time__icontains=general))

		if personalInfoSearch:
			personalInfoResults = personalInfoSearch
		elif studentPlacementSearch:
			temp = PersonalInfo.objects.none()
			for student in studentPlacementSearch:
				person = PersonalInfo.objects.filter(Q(student_id=student.personal_info.student_id))
				temp = person.union(temp)
			studentPlacementResults = temp
		elif studentScheduleSearch:
			temp = PersonalInfo.objects.none()
			for student in studentScheduleSearch:
				person = PersonalInfo.objects.filter(Q(student_id=student.student_placement.personal_info.student_id))
				temp = person.union(temp)
			studentScheduleResults = temp
	else:
		# Advanced search
		results = PersonalInfo.objects.all()

		# Make sure spaces/full names accounted for
		if firstname:
			print("first name")
			firstname = firstname.strip()
			firstNameSearch = results.filter(Q(first_name__icontains=firstname) | Q(preferred_name__icontains=firstname))
			results = firstNameSearch
			whichSearch = 2
		if lastname:
			print("last name")
			lastname = lastname.strip()
			lastNameSearch = results.filter(Q(last_name__icontains=lastname))
			results = lastNameSearch
			whichSearch = 2
		if email:
			print("email")
			email = email.strip()
			emailSearch = results.filter(Q(email__icontains=email))
			results = emailSearch
			whichSearch = 2

		personalInfoResults = results


	context = {
		'PerInfo': personalInfoResults,
		'StudPlace': studentPlacementResults,
		'StudSched': studentScheduleResults,
		'searchType': whichSearch
	}
	return render(request, "student_placement_search.html", context)


def site_info_search(request):
	whichSearch = 0

	general = request.GET.get('a')

	# Initialize results to display all items in database
	siteInfoResults = SiteInfo.objects.none()
	siteAvailabilityResults = SiteInfo.objects.none()

	if general != None and general != "":
		whichSearch = 1
		siteInfoSearch = SiteInfo.objects.filter(Q(site_name__icontains=general) |
			Q(address__icontains=general) | Q(description__icontains=general) | Q(supervisor__icontains=general) |
			Q(supervisor_email__icontains=general) | Q(supervisor_phone__icontains=general) |
			Q(second_contact__icontains=general) | Q(second_contact_email__icontains=general) |
			Q(second_contact_number__icontains=general) | Q(clearances_needed__icontains=general) |
			Q(comments__icontains=general))
		siteAvailabilitySearch = SiteAvailability.objects.filter(Q(day__icontains=general) |
			Q(start_time__icontains=general) | Q(end_time__icontains=general))

		if siteInfoSearch:
			siteInfoResults = siteInfoSearch
		elif siteAvailabilitySearch:
			temp = SiteInfo.objects.none()
			for student in siteAvailabilitySearch:
				person = SiteInfo.objects.filter(Q(site_name=student.site_info.site_name))
				temp = person.union(temp)
			siteAvailabilityResults = temp

	else:
		# Advanced search
		results = SiteInfo.objects.all()

		siteInfoResults = results

	context = {
		'SiteInfo': siteInfoResults,
		'SiteAvail': siteAvailabilityResults,
		'searchType': whichSearch
	}
	return render(request, "site_info_search.html", context)


def add(request):
	pass


def placement(request):
	if request.method == "POST":
		student_placement_form = StudentPlacementForm(request.POST)
		#id = int(request.POST.get('id'))
		#student = PersonalInfo(student_id=id)
		student_avail_days = request.POST.getlist('student_days[]')
		student_avail_start_time = request.POST.getlist('student_start_time[]')
		student_avail_end_time = request.POST.getlist('student_end_time[]')

		if student_placement_form.is_valid():
			student_placement_instance = student_placement_form.save(commit=False)
			student_placement_instance.save()

			for i in range(len(student_avail_days)):
				if student_avail_days[i] and student_avail_start_time[i] and student_avail_end_time[i]:
					student_availability = StudentSchedule(student_placement=student_placement_instance, day=student_avail_days[i], start_time=student_avail_start_time[i], end_time=app_avail_end_time[i])
					student_availability.save()
		else:
			messages.warning(request, 'You filled up the form incorrectly, please try again. It has not been saved.')
			return redirect('workstudy:placement')

	else:
		# show the forms
		context = {}
		student_placement_form = StudentPlacementForm()
		student_schedule_form = StudentScheduleForm()
		context['student_placement_form'] = student_placement_form
		context['student_schedule_form'] = student_schedule_form
		return render(request, 'placement.html', context)

def display_student(request):
	if request.method=='GET':
		id = request.GET.get('id')
		if not id:
			return render(request, 'search.html')
		else:
			allPersonalInfo = PersonalInfo.objects.all().filter(student_id = id)
			allAppData = AppData.objects.all().filter(personal_info__student_id = id)
			allAppAvail = AppAvailability.objects.all().filter(app_data__personal_info__student_id = id)
			context = {
				'allPersonalInfo': allPersonalInfo,
				'allAppData': allAppData,
				'allAppAvail': allAppAvail
			}
			return render(request, 'display_student.html', context)

def edit_student(request):
	if request.method=='GET':
		id = request.GET.get('id')
		if not id:
			return render(request, 'display_student.html')
		else:
			#code to just display info
			# name = PersonalInfo.objects.get(student_id = id)
			# allPersonalInfo = PersonalInfo.objects.all().filter(student_id = id)
			# allAppData = AppData.objects.all().filter(personal_info__student_id = id)
			# allAppAvail = AppAvailability.objects.all().filter(app_data__personal_info__student_id = id)
			# context = {
			# 	'allPersonalInfo': allPersonalInfo,
			# 	'allAppData': allAppData,
			# 	'allAppAvail': allAppAvail
			# }
			if request.method == "POST":
				details = PersonalInfo.objects.get(student_id = id)
				per_info = EditStudentPerForm(request.POST, instance = details)
				# app_info = EditStudentAppForm(request.POST)
				# ranking_info = EditStudentRankForm(request.POST)
				# avail_info = EditStudentAvailForm(request.POST)
				# app_availability_form = AppAvailabilityForm(request.POST)
				# app_avail_days = request.POST.getlist('days[]')
				# app_avail_start_time = request.POST.getlist('start_time[]')
				# app_avail_end_time = request.POST.getlist('end_time[]')
				# app_availbility_modelformset = AppAvailabilityModelFormset(request.POST) #, request.FILES, prefix = 'availility')
				# formset = AuthorFormset(request.POST)

				if per_info.is_valid(): #and app_info.is_valid() and site_placement_rank_form.is_valid():
					per_info_instance = per_info.save(commit=False)
					#app_info_instance = app_info.save(commit=False)
					#ranking_info_instance = ranking_info.save(commit=False)
					# app_availbility_instance = app_availability_form.save(commit=False)
					# here you can add more fields or change them the way you want, after that you will save them
					#app_info_instance.personal_info = per_info_instance
					#ranking_info_instance.app_data = app_info_instance
					#app_availbility_instance.app_data = app_data_instance

					per_info_instance.save()
					#app_info_instance.save()
					#ranking_info_instance.save()
					# messages.info(request, str(app_avail_days))
					# for i in range(len(app_avail_days)):
					# 	if app_avail_days[i] and app_avail_start_time[i] and app_avail_end_time[i]:
					# 		user_availability = AppAvailability(app_data=app_data_instance, day=app_avail_days[i], start_time=app_avail_start_time[i], end_time=app_avail_end_time[i])
					# 		user_availability.save()
					return redirect('workstudy:edit-completed')
				# if the form validation failed, for now just show the application form again and show the error
				else:
					messages.warning(request, 'You have changed information incorrectly, please try dagain. It has not been saved.')
					return redirect('workstudy:display_student')
			else:
				# show the forms
				per_info_form = EditStudentPerForm()
				context = {
					'allPersonalInfo': allPersonalInfo,
					'per_info_form': per_info_form
				}

				# app_info = EditStudentAppForm()
				# ranking_info = EditStudentRankForm()
				# avail_info = EditStudentAvailForm()
				#context['per_info'] = per_info
				# context['app_info'] = app_info
				# context['ranking_info'] = ranking_info
				# context['avail_info'] = avail_info
				return render(request, 'edit_student.html', context)

def display_site(request):
	if request.method=='GET':
		name = request.GET.get('name')
		if not name:
			return render(request, 'site_info_search.html')
		else:
			allSiteInfo = SiteInfo.objects.all().filter(site_name = name)
			allSiteAvail = SiteAvailability.objects.all().filter(site_info__site_name = name)
			context = {
				'allSiteInfo': allSiteInfo,
				'allSiteAvail': allSiteAvail
			}
			return render(request, 'display_site.html', context)

def application(request):
	# template_name = 'pages/create_normal.html'
	if request.method == "POST":
		personal_info_form = PersonalInfoForm(request.POST)
		app_data_form = AppDataForm(request.POST)
		site_placement_rank_form = SitePlacementRankForm(request.POST)
		# app_availability_form = AppAvailabilityForm(request.POST)
		app_avail_days = request.POST.getlist('days[]')
		app_avail_start_time = request.POST.getlist('start_time[]')
		app_avail_end_time = request.POST.getlist('end_time[]')
		# app_availbility_modelformset = AppAvailabilityModelFormset(request.POST) #, request.FILES, prefix = 'availility')
		# formset = AuthorFormset(request.POST)

		if personal_info_form.is_valid() and app_data_form.is_valid() and site_placement_rank_form.is_valid():
			personal_info_instance = personal_info_form.save(commit=False)
			app_data_instance = app_data_form.save(commit=False)
			site_placement_rank_instance = site_placement_rank_form.save(commit=False)
			# app_availbility_instance = app_availability_form.save(commit=False)
			# here you can add more fields or change them the way you want, after that you will save them
			app_data_instance.personal_info = personal_info_instance
			site_placement_rank_instance.app_data = app_data_instance
			#app_availbility_instance.app_data = app_data_instance

			personal_info_instance.save()
			app_data_instance.save()
			site_placement_rank_instance.save()
			# messages.info(request, str(app_avail_days))
			for i in range(len(app_avail_days)):
				if app_avail_days[i] and app_avail_start_time[i] and app_avail_end_time[i]:
					user_availability = AppAvailability(app_data=app_data_instance, day=app_avail_days[i], start_time=app_avail_start_time[i], end_time=app_avail_end_time[i])
					user_availability.save()
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


def site_info_added(request):
	return render(request, "new_site.html", {})


def user_logout(request):
	logout(request)
	return HttpResponseRedirect(reverse('workstudy:index'))


def login_page(request):
	if request.user.is_authenticated:
		return render(request, 'workstudy/index.html', {})
	return render(request, "login.html", {})


def process_login(request):
	username = request.POST.get('username')
	password = request.POST.get('password')
	user = authenticate(username=username, password=password)
	if user is not None:
		request.session.set_expiry(settings.SESSION_EXPIRY_TIME)
		login(request, user)
		return HttpResponseRedirect(reverse('workstudy:index'))
	messages.info(request, 'Wrong username or password')
	return HttpResponseRedirect(reverse('workstudy:login'))


def site_information (request):
	if request.user.is_authenticated:
		if request.method == "POST":
			site_info_form = SiteInfoForm(request.POST)
			site_avail_days = request.POST.getlist('site_days[]')
			site_avail_start_time = request.POST.getlist('site_start_time[]')
			site_avail_end_time = request.POST.getlist('site_end_time[]')

			if site_info_form.is_valid():
				site_info_instance = site_info_form.save(commit=False)
				site_info_instance.save()

				for i in range(len(site_avail_days)):
					if site_avail_days[i] and site_avail_start_time[i] and site_avail_end_time[i]:
						site_availability = SiteAvailability(site_info=site_info_instance, day=site_avail_days[i], start_time=site_avail_start_time[i], end_time=site_avail_end_time[i])
						site_availability.save()
				return redirect('workstudy:new_site')
			else:
				messages.warning(request, 'You filled up the form incorrectly, please try again. It has not been saved.')
				return redirect('workstudy:add_site_info')
		else:
			# show the forms
			context = {}
			site_info_form = SiteInfoForm()
			site_availability_form = SiteAvailabilityForm()
			context['site_info_form'] = site_info_form
			context['site_availability_form'] = site_availability_form
			return render(request, 'add_site_info.html', context)
	return HttpResponseRedirect(reverse('workstudy:login'))

def edit_complete(request):
	return render(request, "edit_complete.html", {})
