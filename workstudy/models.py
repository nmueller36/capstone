from django.db import models

# Create your models here.
class PersonalInfo(models.Model):
	student_id = models.IntegerField(primary_key = True)
	first_name = models.CharField(max_length=256)
	last_name  = models.CharField(max_length=256)
	email      = models.CharField(max_length=256)

class AppData(models.Model):
	personal_info = models.ForeignKey(PersonalInfo, on_delete=models.CASCADE, blank=True, null=True)
	semester      = models.CharField(max_length=100)


class SiteInfo(models.Model):
	site_name   = models.CharField(max_length=256)
	address     = models.CharField(max_length=256)
	description = models.CharField(max_length=1000)
	supervisor  = models.CharField(max_length=256)
	supervisor_email = models.CharField(max_length=256)
	supervisor_phone = models.CharField(max_length=256)
	second_contact = models.CharField(max_length=256)
	second_contact_email = models.CharField(max_length=256)

class AppAvailability(models.Model):
	app_data   = models.ForeignKey(AppData, on_delete=models.CASCADE, blank=True, null=True)
	day        = models.CharField(max_length=100)
	start_time = models.IntegerField()
	end_time   = models.IntegerField()

class StudentPlacement(models.Model):
	personal_info = models.ForeignKey(PersonalInfo, on_delete=models.CASCADE, blank=True, null=True)
	site_info     = models.ForeignKey(SiteInfo, on_delete=models.CASCADE, blank=True, null=True)
	semester      = models.CharField(max_length=100)

class StudentSchedule(models.Model):
	personal_info = models.ForeignKey(PersonalInfo, on_delete=models.CASCADE, blank=True, null=True)
	semester      = models.CharField(max_length=100)



class SiteAvailability(models.Model):
	site_info  = models.ForeignKey(SiteInfo, on_delete=models.CASCADE, blank=True, null=True)
	day        = models.CharField(max_length=100)
	start_time = models.IntegerField()
	end_time   = models.IntegerField()
