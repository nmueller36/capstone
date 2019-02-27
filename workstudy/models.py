from django.db import models

MONTHS = (
	# ('choice set in the model', 'human-readable format of the choice for the website')
	('january', 'January'),
	('february', 'February'),
	('march', 'March'),
	('april', 'April'),
	('may', 'May'),
	('june', 'June'),
	('july', 'July'),
	('august', 'August'),
	('september', 'September'),
	('october', 'October'),
	('november', 'November'),
	('december', 'December'),
)

RANKING = (
	# choices for Site Placement Ranking
	('one', '1'),
	('two','2'),
	('three', '3'),
	('four', '4'),
	('five', '5'),
	('six', '6'),

)



# Create your models here.
class PersonalInfo(models.Model): #main table that contains information that will be used for multiple tables
	student_id     = models.IntegerField(primary_key = True, verbose_name= "Student ID")
	first_name     = models.CharField(max_length=256, verbose_name= "First Name")
	preferred_name = models.CharField(max_length=256, verbose_name= "Preferred Name")
	last_name      = models.CharField(max_length=256, verbose_name= "Last Name")
	pronouns       = models.CharField(max_length=256)
	email          = models.CharField(max_length=256)
	def __str__(self):
		return self.first_name + " " + self.last_name + " (" + self.email + ")"

class AppData(models.Model): #student application that will be filled out each semester. will sort by semester
	personal_info   = models.ForeignKey(PersonalInfo, on_delete=models.CASCADE, blank=True, null=True)
	semester        = models.CharField(max_length=100, verbose_name= u"Semester (example: 'Spring 2019' or 'Fall 2018' )")
	timeStamp       = models.DateTimeField(auto_now_add=True)
	phone_num       = models.CharField(max_length=256, null=True, verbose_name= u"Phone Number") #should I make this an int?
	grad_month      = models.CharField(max_length=256, choices=MONTHS, verbose_name= u"Graduation Month")
	grad_year       = models.IntegerField(null=True)
	work_study      = models.NullBooleanField(verbose_name= u"Do you qualify for federal work study?")
	for_class       = models.NullBooleanField(verbose_name= u"Is this for a class?")
	what_class      = models.CharField(max_length=256, null=True, verbose_name= u"If so, what class is it for?")
	car             = models.NullBooleanField(verbose_name= u"Do you have a car?")
	carpool         = models.NullBooleanField(verbose_name=u"Are you willing to be a carpool driver?")
	wanted_hours    = models.IntegerField(verbose_name= u"How many total hours a week would you like to work?")
	major           = models.CharField(max_length=256, null=True)
	foreign_lang    = models.NullBooleanField(verbose_name= u"Are you fluent in a foreign language?")
	languages       = models.CharField(max_length=256, null=True, verbose_name= u"What languages?")
	clearances      = models.NullBooleanField(verbose_name= u"Do you have clearances? (Child Abuse, FBI Fingerprints, State Police)")
	prior_work      = models.CharField(max_length=1000, null=True)
	ccec_ws         = models.NullBooleanField(verbose_name= u"Have you previously worked through the CCEC?")
	previous_site   = models.CharField(max_length=256, null=True, verbose_name= "If so, what site did you work at?")
	remain_at_site  = models.NullBooleanField(verbose_name= u"Would you like to remain at your current site?")
	keep_schedule   = models.NullBooleanField(verbose_name= u"Would you like to keep your same schedule?")
	hear_about_ccec = models.CharField(max_length=256, null=True, verbose_name= u"How did you hear about the CCEC?")
	placement       = models.NullBooleanField() #will not be on the application, for office workers to mark that this student has been placed at a site
	def __str__(self):
		return self.personal_info.first_name + " " + self.personal_info.last_name + " (" + self.personal_info.email + ")" + " " + self.semester


class SitePlacementRank(models.Model): #section of application that will rank where the student would like to be placed
	app_data         = models.ForeignKey(AppData, on_delete=models.CASCADE, blank=True, null=True)
	after_school     = models.IntegerField(null=True, verbose_name=u"After School" ,choices = RANKING)
	medical          = models.IntegerField(null=True, choices = RANKING)
	community_center = models.IntegerField(null=True,verbose_name= u"Community Center", choices = RANKING)
	charity_org      = models.IntegerField(null=True, verbose_name= u"Charity Organization", choices = RANKING)
	hospice          = models.IntegerField(null=True, choices = RANKING)
	other            = models.IntegerField(null=True, choices = RANKING)
	def __str__(self):
		return self.personal_info.first_name + " " + self.personal_info.last_name + " (" + self.personal_info.email + ")" + " " + self.semester


class AppAvailability(models.Model): #where student will enter their availility to work on application
	app_data   = models.ForeignKey(AppData, on_delete=models.CASCADE, blank=True, null=True)
	day        = models.CharField(max_length=256, null=True)
	start_time = models.IntegerField(null=True)
	end_time   = models.IntegerField(null=True)


class SiteInfo(models.Model): #important information regarding the sites that can take work study students
	site_name   = models.CharField(max_length=256, primary_key = True)
	address     = models.CharField(max_length=256, null=True)
	description = models.CharField(max_length=10000)
	supervisor  = models.CharField(max_length=256, null=True)
	supervisor_email = models.CharField(max_length=256, null=True)
	supervisor_phone = models.CharField(max_length=256, null=True)
	second_contact = models.CharField(max_length=256, null=True)
	second_contact_email = models.CharField(max_length=256, null=True)
	second_contact_number = models.CharField(max_length=256, null=True)
	clearances_needed    = models.CharField(max_length=256, null=True)
	comments             = models.CharField(max_length=10000, null=True)


class StudentPlacement(models.Model): #once a ccec worker finds a placement for the student, it will be added to this table with additional information
	personal_info   = models.ForeignKey(PersonalInfo, on_delete=models.CASCADE, blank=True, null=True)
	app_data        = models.ForeignKey(AppData, on_delete=models.CASCADE, blank=True, null=True)
	site_info       = models.ForeignKey(SiteInfo, on_delete=models.CASCADE, blank=True, null=True)
	driver          = models.CharField(max_length=256,null=True)
	total_hours     = models.IntegerField(null=True)
	started         = models.CharField(max_length=256, null=True)
	fbi_fingerprint = models.CharField(max_length=256, null=True)
	child_abuse     = models.CharField(max_length=256, null=True)
	state_police    = models.CharField(max_length=256, null=True)
	physical        = models.CharField(max_length=256, null=True)
	ppd             = models.CharField(max_length=256, null=True)
	comments        = models.CharField(max_length=10000, null=True)


class StudentSchedule(models.Model): # where a student's work study schedule will be enetered
	student_placement  = models.ForeignKey(StudentPlacement, on_delete=models.CASCADE, blank=True, null=True)
	day                = models.CharField(max_length=256, null=True)
	start_time         = models.IntegerField(null=True)
	end_time           = models.IntegerField(null=True)

class SiteAvailability(models.Model): # dates and times when sites can take work study students
	site_info  = models.ForeignKey(SiteInfo, on_delete=models.CASCADE, blank=True, null=True)
	day        = models.CharField(max_length=256, null=True)
	start_time = models.IntegerField(null=True)
	end_time   = models.IntegerField(null=True)
