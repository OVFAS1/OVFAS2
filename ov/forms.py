from django import forms
from django.contrib.auth.models import User
import datetime
from .models import Student,OutingForm,Filter


def cal_weekends():
	d = datetime.date.today()
	w=[]
	while(d.weekday()!=6):
		d=d+datetime.timedelta(1)
	w.append(d.strftime("%Y-%m-%d"))
	w.append((d+datetime.timedelta(1)).strftime("%Y-%m-%d"))
	return w

class StudentForm(forms.ModelForm):
    class Meta:
        model=Student
        fields=['registration_no']
        
class form_outing(forms.ModelForm):
    class Meta:
        model=OutingForm
        fields='__all__'
        



class FilterForm(forms.ModelForm):

    class Meta:
        model=Filter
        fields=['hostelblock','date_of_outing']


    def __init__(self, *args, **kwargs):
        super(FilterForm, self).__init__(*args, **kwargs)
    
        self.fields['date_of_outing'].queryset =cal_weekends()