from django import forms
from .models import PersonalInfo, AppData, AppAvailability, SitePlacementRank

class PersonalInfoForm (forms.ModelForm):
    class Meta:
        model = PersonalInfo
        fields = '__all__'

class AppDataForm (forms.ModelForm):
    class Meta:
        model = AppData
        fields = '__all__'

class SitePlacementRankForm (forms.ModelForm):
    class Meta:
        model = SitePlacementRank
        fields = '__all__'

class AppAvailabilityForm (forms.ModelForm):
    class Meta:
        model = AppAvailability
        fields = '__all__'
