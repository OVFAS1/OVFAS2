from django.db import models
from django.contrib.admin.widgets import AdminDateWidget
from django.core.validators import RegexValidator
import os
from django.contrib.auth.models import Permission,User
import datetime



def cal_weekends():
	d = datetime.date.today()
	w=[]
	while(d.weekday()!=6):
		d=d+datetime.timedelta(1)
	w.append(('0',d.strftime("%Y-%m-%d")))
	w.append(('1',(d+datetime.timedelta(1)).strftime("%Y-%m-%d")))
	return tuple(w)



class HostelBlock(models.Model):
    block_name=models.CharField(max_length=100)

    def __str__(self):
        return(self.block_name)

class OutingForm(models.Model):
    reg_no_regex = RegexValidator(regex=r'\d{2}[a-zA-Z]{3}\d{4}', message="Registation number should be like 17BCE1007")
    registration_no=models.CharField(validators=[reg_no_regex],max_length=9)
    name=models.CharField(max_length=100)
    mess_type=models.CharField(max_length=100)
    phone_regex = RegexValidator(regex=r'^\d{10}$', message="Phone number should be up to 10 digits only")
    student_phone_number=models.CharField(validators=[phone_regex],max_length=13,default='')
    parent_phone_number=models.CharField(validators=[phone_regex],max_length=13,default='')
    hostel_block=models.ForeignKey(HostelBlock,on_delete=models.SET_NULL,null=True)
    date_of_outing=models.DateField(null=True)
    time_of_leaving=models.TimeField(blank=False)
    time_of_arrival=models.TimeField(blank=False)
    viiting_address=models.TextField()
    purpose_of_leaving=models.CharField(max_length=250)
    permanent_address=models.TextField()
    is_approved=models.BooleanField(default=False)
    def __str__(self):
        return(self.registration_no)

class Student(models.Model):
    reg_no_regex = RegexValidator(regex=r'\d{2}[a-zA-Z]{3}\d{4}', message="Plese give valid registration number")
    registration_no=models.CharField(validators=[reg_no_regex],max_length=9,primary_key=True)
    name=models.CharField(max_length=100)

    def __str__(self):
        return(self.registration_no)



class HostelMess(models.Model):
    MessName=models.CharField(max_length=50,blank=False)

    def __str__(self):
        return (self.MessName)


class visibility(models.Model):
    outing_form=models.BooleanField(default=False)
    

class Warden(models.Model):
    hostelblock=models.ForeignKey(HostelBlock,on_delete=models.CASCADE)
    user=models.OneToOneField(User, unique=True,on_delete=models.CASCADE)
    name=models.CharField(max_length=50,blank=True)

    def __str__(self):
        return (self.name+' ('+str(self.hostelblock)+')')

        


datechoice=cal_weekends()

class Filter(models.Model):
    hostelblock=models.ForeignKey(HostelBlock,on_delete=models.CASCADE,null=True,blank=True)
    date_of_outing=models.CharField(max_length=50,choices=datechoice,null=True,blank=True)
    