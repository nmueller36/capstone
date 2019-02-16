from django import forms
from .models import PersonalInfo, AppData, AppAvailability, SitePlacementRank

class PersonalInfoForm (forms.ModelForm):
    class Meta:
        model = PersonalInfo
        widgets = {
            'text'
        }

class AppDataForm (forms.ModelForm):
    class Meta:
        model = AppData

class SitePlacementRankForm (forms.ModelForm):
    class Meta:
        model = SitePlacementRank

class AppAvailabilityForm (forms.ModelForm):
    class Meta:
        model = AppAvailability
