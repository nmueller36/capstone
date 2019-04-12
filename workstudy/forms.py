from django import forms
from .models import PersonalInfo, AppData, AppAvailability, SitePlacementRank, SiteInfo, SiteAvailability
from django.forms import modelformset_factory
import datetime


class PersonalInfoForm (forms.ModelForm):
    class Meta:
        model = PersonalInfo
        fields = '__all__'

class AppDataForm (forms.ModelForm):
    class Meta:
        model = AppData
        fields = '__all__'
        # exclude field(s) that the users should not see on the page
        exclude = ('personal_info', 'placement')


    def __init__(self, *args, **kwargs):
        # calling the mothership to initialize all its variables before updating the form
        super(AppDataForm, self).__init__(*args, **kwargs)
        # grab the current year
        current_year = datetime.datetime.now().year

        #updates year in semester in March of every year
        fall_semester = "Fall {}".format(current_year)
        spring_semester = "Spring {}".format(current_year+1)

        # set the grad_year to be pre-filled with the years ahead
        self.fields['grad_year'] = forms.ChoiceField(
            choices = [(year, year) for year in range(current_year, current_year + 8)]
        )
        self.fields['semester'] = forms.ChoiceField(
            choices = [
                ("spring " + str(current_year), "Spring " + str(current_year)),
                ("fall " + str(current_year), "Fall " + str(current_year)),
                ("spring " + str(current_year + 1), "Spring " + str(current_year + 1))
            ]
        )

        self.fields['grad_year'].label = "Graduation Year"

        # change the default label for the car field in the AppData model
        # alternatively, you can just add verbose_name=u"Do you have a car?"
        #self.fields['car'].label = "Do you have a car?"


        # make the fields required, for some reason it was not set before
        self.fields['car'].required = True
        self.fields['work_study'].required = True
        self.fields['carpool'].required = True
        self.fields['foreign_lang'].required = True
        self.fields['clearances'].required = True
        self.fields['ccec_ws'].required = True
        self.fields['remain_at_site'].required = True
        self.fields['keep_schedule'].required = True
    #    self.fields['placement'].required = True

'''AppAvailabilityModelFormset = modelformset_factory(
    AppAvailability,
    fields=('day', 'start_time', 'end_time',),

    extra=1,
    widgets={'day': forms.TextInput(attrs={
        'class': 'form-control',

    }),
    'start_time' : forms.TextInput(attrs={

    }),
    'end_time' : forms.TextInput(attrs={

    })
    }

    )'''


class SitePlacementRankForm (forms.ModelForm):
    class Meta:
        model = SitePlacementRank
        fields = '__all__'
        exclude = ('app_data',)

    def __init__(self, *args, **kwargs):
        # calling the mothership to initialize all its variables before updating the form
        super(SitePlacementRankForm, self).__init__(*args, **kwargs)

class AppAvailabilityForm (forms.ModelForm):
    class Meta:
        model = AppAvailability
        fields = '__all__'
        exclude = ('app_data',)

    def __init__(self, *args, **kwargs):
        super(AppAvailabilityForm, self).__init__(*args, **kwargs)

        self.fields['start_time'] = forms.TimeField(widget=forms.TimeInput(format='%H:%M'))
        self.fields['end_time'] = forms.TimeField(widget=forms.TimeInput(format='%H:%M'))


#AppAvailabilityModelFormset = modelformset_factory(
#AppAvailability,
#fields=('day', 'start_time', 'end_time'),
#extra=1,
#widgets={'day': forms.TextInput(attrs={
#    'class': 'form-control',
#})
#}
#)

class SiteInfoForm (forms.ModelForm):
    class Meta:
        model = SiteInfo
        fields = '__all__'

    def __init__(self, *args, **kwargs):

        super(SiteInfoForm, self).__init__(*args, **kwargs)


class SiteAvailabilityForm (forms.ModelForm):
    class Meta:
        model = SiteAvailability
        fields = '__all__'
        exclude = ('site_info',)

        def __init__(self, *args, **kwargs):

            super(SiteInfoForm, self).__init__(*args, **kwargs)

            self.fields['start_time'] = forms.TimeField(widget=forms.TimeInput(format='%H:%M'))
            self.fields['end_time'] = forms.TimeField(widget=forms.TimeInput(format='%H:%M'))
