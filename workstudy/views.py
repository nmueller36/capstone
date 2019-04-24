from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from .forms import PersonalInfoForm, AppDataForm, SitePlacementRankForm, SiteInfoForm, AppAvailabilityForm, SiteAvailabilityForm, StudentPlacementForm, StudentScheduleForm, EditStudentPerForm, EditStudentAppForm, EditStudentAvailForm, EditStudentRankForm, EditStudentScheduleForm, EditStudentPlacementForm
from django.db.models import Q
from itertools import chain
import datetime
from django.conf import settings

from django.urls import reverse

# add imports for login and logout
from django.contrib.auth import authenticate, login, logout

from django.shortcuts import redirect

from django.contrib import messages

# import tables from the database
from workstudy.models import PersonalInfo, AppData, SitePlacementRank, AppAvailability, SiteAvailability, SiteInfo, StudentPlacement, StudentSchedule


def index(request):
	return render(request, "index.html", {})


def application_completed(request):
	return render(request, "completed.html", {})


def new_site_completed(request):
	return render(request, "new_site.html", {})

def search(request):
	if request.user.is_authenticated:
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
				wanted_items = set()
				for entry in personalInfoResults:
					if not entry.appdata_set.filter(Q(placement="True")).count() > 0:
						wanted_items.add(entry.student_id)
				personalInfoResults = PersonalInfo.objects.filter(student_id__in=wanted_items)
			elif appDataSearch:
				temp = PersonalInfo.objects.none()
				for app in appDataSearch:
					person = PersonalInfo.objects.filter(Q(student_id=app.personal_info.student_id))
					temp = person.union(temp)
				appDataResults = temp
				wanted_items = set()
				for entry in appDataResults:
					if not entry.appdata_set.filter(Q(placement="True")).count() > 0:
						wanted_items.add(entry.student_id)
				appDataResults = PersonalInfo.objects.filter(student_id__in=wanted_items)
			elif appAvailabilitySearch:
				temp = PersonalInfo.objects.none()
				for app in appAvailabilitySearch:
					person = PersonalInfo.objects.filter(Q(student_id=app.personal_info.student_id))
					temp = person.union(temp)
				appAvailabilityResults = temp
				wanted_items = set()
				for entry in appAvailabilityResults:
					if not entry.appdata_set.filter(Q(placement="True")).count() > 0:
						wanted_items.add(entry.student_id)
				appAvailabilityResults = PersonalInfo.objects.filter(student_id__in=wanted_items)
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

			# Filter out results to only include applications, no placements
			wanted_items = set()
			for entry in results:
				if not entry.appdata_set.filter(Q(placement="True")).count() > 0:
					wanted_items.add(entry.student_id)
			results = PersonalInfo.objects.filter(student_id__in=wanted_items)

			personalInfoResults = results

		context = {
			'PerInfo': personalInfoResults,
			'AppData': appDataResults,
			'AppAvail': appAvailabilityResults,
			'years': choices,
			'searchType': whichSearch
		}

		return render(request, "search.html", context)
	return HttpResponseRedirect(reverse('workstudy:login'))

def student_placement_search(request):
	if request.user.is_authenticated:
		whichSearch = 0

		general = request.GET.get('a')
		firstname = request.GET.get('p')
		lastname = request.GET.get('q')
		email = request.GET.get('r')
		sitename = request.GET.get('s')
		day = request.GET.get('t')
		starttime = request.GET.get('u')
		endtime = request.GET.get('v')

		# Initialize results to display all items in database
		personalInfoResults = PersonalInfo.objects.none()
		studentPlacementResults = PersonalInfo.objects.none()
		studentScheduleResults = PersonalInfo.objects.none()
		siteInfoResults = PersonalInfo.objects.none()

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
			siteInfoSearch = SiteInfo.objects.filter(Q(site_name__icontains=general) |
				Q(address__icontains=general) | Q(description__icontains=general) | Q(supervisor__icontains=general) |
				Q(supervisor_email__icontains=general) | Q(supervisor_phone__icontains=general) |
				Q(second_contact__icontains=general) | Q(second_contact_email__icontains=general) |
				Q(second_contact_number__icontains=general) | Q(clearances_needed__icontains=general) |
				Q(comments__icontains=general))

			if personalInfoSearch:
				personalInfoResults = personalInfoSearch
				wanted_items = set()
				for entry in personalInfoResults:
					if entry.appdata_set.filter(Q(placement="True")).count() > 0:
						wanted_items.add(entry.student_id)
				personalInfoResults = PersonalInfo.objects.filter(student_id__in=wanted_items)
			elif studentPlacementSearch:
				temp = PersonalInfo.objects.none()
				for student in studentPlacementSearch:
					person = PersonalInfo.objects.filter(Q(student_id=student.personal_info.student_id))
					temp = person.union(temp)
				studentPlacementResults = temp
				wanted_items = set()
				for entry in studentPlacementResults:
					if entry.appdata_set.filter(Q(placement="True")).count() > 0:
						wanted_items.add(entry.student_id)
				studentPlacementResults = PersonalInfo.objects.filter(student_id__in=wanted_items)
			elif studentScheduleSearch:
				temp = PersonalInfo.objects.none()
				for student in studentScheduleSearch:
					person = PersonalInfo.objects.filter(Q(student_id=student.student_placement.personal_info.student_id))
					temp = person.union(temp)
				studentScheduleResults = temp
				wanted_items = set()
				for entry in studentScheduleResults:
					if entry.appdata_set.filter(Q(placement="True")).count() > 0:
						wanted_items.add(entry.student_id)
				studentScheduleResults = PersonalInfo.objects.filter(student_id__in=wanted_items)
			elif siteInfoSearch:
				temp = PersonalInfo.objects.none()
				for site in siteInfoSearch:
					placements = StudentPlacement.objects.filter(Q(site_info=site))
					for student in placements:
						person = PersonalInfo.objects.filter(Q(student_id=student.personal_info.student_id))
						temp = person.union(temp)
				siteInfoResults = temp
				wanted_items = set()
				for entry in siteInfoResults:
					if entry.appdata_set.filter(Q(placement="True")).count() > 0:
						wanted_items.add(entry.student_id)
				siteInfoResults = PersonalInfo.objects.filter(student_id__in=wanted_items)
		else:
			# Advanced search
			results = PersonalInfo.objects.all()

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
			if sitename:
				print("site name")
				sitename = sitename.strip()
				wanted_items = set()
				for entry in results:
					placements = entry.studentplacement_set.all()
					for place in placements:
						if place.site_info.site_name == sitename:
							wanted_items.add(entry.student_id)
				results = PersonalInfo.objects.filter(student_id__in=wanted_items)
				whichSearch = 2
			if day:
				print("day")
				wanted_items = set()
				for entry in results:
					placements = entry.studentplacement_set.all()
					for place in placements:
						if place.studentschedule_set.filter(Q(day__icontains=day)).count() > 0:
							wanted_items.add(entry.student_id)
				results = PersonalInfo.objects.filter(student_id__in=wanted_items)
				whichSearch = 2
			if starttime:
				print("start time")
				wanted_items = set()
				for entry in results:
					placements = entry.studentplacement_set.all()
					for place in placements:
						if place.studentschedule_set.filter(Q(start_time__lte=starttime)).count() > 0:
							wanted_items.add(entry.student_id)
				results = PersonalInfo.objects.filter(student_id__in=wanted_items)
				whichSearch = 2
			if endtime:
				print("end time")
				wanted_items = set()
				for entry in results:
					placements = entry.studentplacement_set.all()
					for place in placements:
						if place.studentschedule_set.filter(Q(end_time__gte=endtime)).count() > 0:
							wanted_items.add(entry.student_id)
				results = PersonalInfo.objects.filter(student_id__in=wanted_items)
				whichSearch = 2

			wanted_items = set()
			for entry in results:
				if entry.appdata_set.filter(Q(placement="True")).count() > 0:
					wanted_items.add(entry.student_id)
			results = PersonalInfo.objects.filter(student_id__in=wanted_items)

			personalInfoResults = results

		context = {
			'PerInfo': personalInfoResults,
			'StudPlace': studentPlacementResults,
			'StudSched': studentScheduleResults,
			'SiteInfo': siteInfoResults,
			'searchType': whichSearch
		}
		return render(request, "student_placement_search.html", context)
	return HttpResponseRedirect(reverse('workstudy:login'))

def site_info_search(request):
	if request.user.is_authenticated:
		whichSearch = 0

		general = request.GET.get('a')
		sitename = request.GET.get('s')
		day = request.GET.get('t')
		starttime = request.GET.get('u')
		endtime = request.GET.get('v')

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

			if sitename:
				print("site name")
				sitename = sitename.strip()
				siteNameSearch = results.filter(Q(site_name__icontains=sitename))
				results = siteNameSearch
				whichSearch = 2
			if day:
				print("day")
				wanted_items = set()
				for entry in results:
					if entry.siteavailability_set.filter(Q(day__icontains=day)).count() > 0:
						wanted_items.add(entry.site_name)
				results = SiteInfo.objects.filter(site_name__in=wanted_items)
				whichSearch = 2
			if starttime:
				print("start time")
				wanted_items = set()
				for entry in results:
					if entry.siteavailability_set.filter(Q(start_time__lte=starttime)).count() > 0:
						wanted_items.add(entry.site_name)
				results = SiteInfo.objects.filter(site_name__in=wanted_items)
				whichSearch = 2
			if endtime:
				print("end time")
				wanted_items = set()
				for entry in results:
					if entry.siteavailability_set.filter(Q(end_time__gte=endtime)).count() > 0:
						wanted_items.add(entry.site_name)
				results = SiteInfo.objects.filter(site_name__in=wanted_items)
				whichSearch = 2

			siteInfoResults = results

		context = {
			'SiteInfo': siteInfoResults,
			'SiteAvail': siteAvailabilityResults,
			'searchType': whichSearch
		}
		return render(request, "site_info_search.html", context)
	return HttpResponseRedirect(reverse('workstudy:login'))

def placement(request):
	if request.user.is_authenticated:
		#if request.method == "GET":
		#id = request.GET.get('stud_id')
		#id = int(request.GET.get('stud_id'))
		#allPersonalInfo = PersonalInfo.objects.all().filter(student_id = id)
		#messages.info(id)
			#student_personal_info = PersonalInfo.objects.all().filter(student_id = id)
			#student_app_data = AppData.objects.all().filter(personal_info__student_id = id)
		if request.method == "POST" and 'placing_student' in request.POST:
			student_placement_form = StudentPlacementForm(request.POST)
			#student = PersonalInfo(student_id=id)
			student_avail_days = request.POST.getlist('student_days[]')
			student_avail_start_time = request.POST.getlist('student_start_time[]')
			student_avail_end_time = request.POST.getlist('student_end_time[]')

			student_id = int(request.POST.get('student_id'))
			personal_info_instance = PersonalInfo.objects.get(student_id = student_id)
			app_data_instance = AppData.objects.get(personal_info__student_id = student_id)

			if student_placement_form.is_valid():
				student_placement_instance = student_placement_form.save(commit=False)
				student_placement_instance.personal_info = personal_info_instance
				app_data_instance.placement = True
				app_data_instance.save()
				student_placement_instance.app_data = app_data_instance
				student_placement_instance.save()

				for i in range(len(student_avail_days)):
					if student_avail_days[i] and student_avail_start_time[i] and student_avail_end_time[i]:
						student_availability = StudentSchedule(student_placement=student_placement_instance, day=student_avail_days[i], start_time=student_avail_start_time[i], end_time=student_avail_end_time[i])
						student_availability.save()
				messages.info(request, 'Thank you for submitting! The student has been placed.')
				return redirect('workstudy:placement')
			else:
				messages.warning(request, 'You filled up the form incorrectly, please try again. It has not been saved.')
				return redirect('workstudy:placement')

		elif request.method == "POST" and 'submit_placement' in request.POST:
			# show the forms
			context = {} #'allPersonalInfo': allPersonalInfo,}
			student_placement_form = StudentPlacementForm()
			student_schedule_form = StudentScheduleForm()
			context['student_id'] = request.POST.get('student_id')
			context['student_name'] = request.POST.get('student_name')
			context['student_placement_form'] = student_placement_form
			context['student_schedule_form'] = student_schedule_form
			return render(request, 'placement.html', context)
	return HttpResponseRedirect(reverse('workstudy:login'))

def display_student(request):
	if request.user.is_authenticated:
		if request.method=='GET':
			id = request.GET.get('id')
			if not id:
				return render(request, 'search.html')
			else:
				allPersonalInfo = PersonalInfo.objects.get(student_id = id)
				allAppData = AppData.objects.filter(personal_info__student_id = id).order_by('-timeStamp')[0]
				allAppAvail = AppAvailability.objects.filter(app_data__id = allAppData.id)
				context = {
					'allPersonalInfo': allPersonalInfo,
					'allAppData': allAppData,
					'allAppAvail': allAppAvail
				}
				return render(request, 'display_student.html', context)
	return HttpResponseRedirect(reverse('workstudy:login'))

def edit_student(request):
	if request.user.is_authenticated:
		if request.method == "POST"  and 'edit_student' in request.POST:
			student_id = int(request.POST.get('student_id'))
			allPersonalInfo = PersonalInfo.objects.all().filter(student_id = student_id)
			allAppData = AppData.objects.filter(personal_info__student_id = student_id).order_by('-timeStamp')[0]
			per_details = PersonalInfo.objects.get(student_id = student_id)
			app_details = AppData.objects.get(personal_info__student_id = student_id)
			per_info = EditStudentPerForm(request.POST, instance = per_details)
			app_info = EditStudentAppForm(request.POST, instance = app_details)

			if allAppData.placement == True: #has placement
				student_placement_details = StudentPlacement.objects.get(personal_info__student_id = student_id)
				student_schedule_details = StudentSchedule.objects.get(student_placement__personal_info__student_id = student_id)
				student_placement_info = EditStudentPlacementForm(request.POST, instance = student_placement_details)
				student_schedule_info = EditStudentScheduleForm(request.POST, instance = student_schedule_details)


				if per_info.is_valid() and app_info.is_valid() and student_placement_info.is_valid() and student_schedule_info.is_valid(): # and site_placement_rank_form.is_valid():
					per_info_instance = per_info.save(commit=False)
					app_instance = app_info.save(commit=False)
					student_placement_instance = student_placement_info.save(commit=False)
					student_schedule_instance = student_schedule_info.save(commit=False)


					per_info_instance.save()
					app_instance.save()
					student_placement_instance.save()
					student_schedule_instance.save()


					return redirect('workstudy:edit_completed')

				else:
					messages.warning(request, 'You have changed information incorrectly, please try again. It has not been saved.')
					return redirect('workstudy:edit_student')

			else: #not placed yet
				allAppAvail = AppAvailability.objects.get(app_data__personal_info__student__id = student_id)
				allSiteRank = SitePlacementRank.objects.get(app_data__personal_info__student__id = student_id)
				app_avail_details = AppAvailability.objects.get(app_data__personal_info__student_id = student_id)
				site_rank_details = SitePlacementRank.objects.get(app_data__personal_info__student_id = student_id)
				app_avail_info = EditStudentAvailForm(request.POST, instance = app_avail_details)
				site_rank_info = EditStudentRankForm(request.POST, instance = site_rank_details)


				if per_info.is_valid() and app_info.is_valid() and app_avail_info.is_valid() and site_rank_info.save(): # and site_placement_rank_form.is_valid():
					per_info_instance = per_info.save(commit=False)
					app_instance = app_info.save(commit=False)
					app_avail_instance = app_avail_info.save(commit=False)
					site_rank_instance = aite_rank_info.save(commit=False)

					per_info_instance.save()
					app_instance.save()
					app_avail_instance.save()
					site_rank_instance.save()

					return redirect('workstudy:edit_completed')

				else:
					messages.warning(request, 'You have changed information incorrectly, please try again. It has not been saved.')
					return redirect('workstudy:edit_student')

		elif request.method == "POST" and 'submit_edit' in request.POST:
			student_id = int(request.POST.get('student_id'))
			allPersonalInfo = PersonalInfo.objects.all().filter(student_id = student_id)
			allAppData = AppData.objects.filter(personal_info__student_id = student_id).order_by('-timeStamp')[0]

			if allAppData.placement == True: #has placement
				context = {}
				context['per_info_form'] = EditStudentPerForm(instance = PersonalInfo.objects.get(student_id = student_id))
				context['app_info_form'] = EditStudentAppForm(instance = PersonalInfo.objects.get(student_id = student_id))
				context['student_placement_info_form'] = EditStudentPlacementForm(instance = PersonalInfo.objects.get(student_id = student_id))
				context['student_schedule_form'] = EditStudentAppForm(instance = PersonalInfo.objects.get(student_id = student_id))
				context['allPersonalInfo'] = PersonalInfo.objects.all().filter(student_id = student_id)
				context['allAppData'] = AppData.objects.get(personal_info__student_id = student_id)
				context['allStudentPlacement'] = StudentPlacement.objects.get(personal_info__student_id = student_id)
				context['allStudentSchedule'] = StudentSchedule.objects.get(student_placement__personal_info__student_id = student_id)

			else:# no placcement
				context = {}
				context['per_info_form'] = EditStudentPerForm(instance = PersonalInfo.objects.get(student_id = student_id))
				context['app_info_form'] = EditStudentAppForm(instance = PersonalInfo.objects.get(student_id = student_id))
			#context['student_id'] = request.POST.get('student_id')
			#per_info_form = EditStudentPerForm(instance = PersonalInfo.objects.get(student_id = student_id))
				context['app_avail_info_form'] = EditStudentAvailForm(instance = PersonalInfo.objects.get(student_id = student_id))
				context['site_rank_info_form'] = EditStudentRankForm(instance = PersonalInfo.objects.get(student_id = student_id))
				context['allPersonalInfo'] = PersonalInfo.objects.all().filter(student_id = student_id)
				context['allAppData'] = AppData.objects.get(personal_info__student_id = student_id)

			return render(request, 'edit_student.html', context)
	return HttpResponseRedirect(reverse('workstudy:login'))

def edit_complete(request):
	return render(request, "edit_complete.html", {})

def display_site(request):
	if request.user.is_authenticated:

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
	return HttpResponseRedirect(reverse('workstudy:login'))


def application(request):
	# template_name = 'pages/create_normal.html'
	if request.method == "POST":
		personal_info_form = PersonalInfoForm(request.POST)
		student_id = int(request.POST.get('student_id'))
		if PersonalInfo.objects.filter(student_id = student_id).exists():
			personal_info_instance = PersonalInfo.objects.get(student_id = student_id)
		else:
			if personal_info_form.is_valid():
				personal_info_instance = personal_info_form.save(commit=False)
			else:
				messages.warning(request, 'Something is wrong with the personal information data, nothing is saved')
				return redirect('workstudy:application')
		app_data_form = AppDataForm(request.POST)
		site_placement_rank_form = SitePlacementRankForm(request.POST)
		# app_availability_form = AppAvailabilityForm(request.POST)
		app_avail_days = request.POST.getlist('days[]')
		app_avail_start_time = request.POST.getlist('start_time[]')
		app_avail_end_time = request.POST.getlist('end_time[]')
		# app_availbility_modelformset = AppAvailabilityModelFormset(request.POST) #, request.FILES, prefix = 'availility')
		# formset = AuthorFormset(request.POST)

		if app_data_form.is_valid() and site_placement_rank_form.is_valid():
			app_data_instance = app_data_form.save(commit=False)
			site_placement_rank_instance = site_placement_rank_form.save(commit=False)
			# app_availbility_instance = app_availability_form.save(commit=False)
			# here you can add more fields or change them the way you want, after that you will save them
			app_data_instance.personal_info = personal_info_instance
			site_placement_rank_instance.app_data = app_data_instance
			#app_availbility_instance.app_data = app_data_instance
			if not PersonalInfo.objects.filter(student_id = personal_info_instance.student_id).exists():
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
		return render(request, 'index.html', {})
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
