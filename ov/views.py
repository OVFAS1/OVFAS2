from django.shortcuts import render
from .models import Student,OutingForm,HostelBlock,HostelMess,Warden
from django.urls import reverse_lazy
from django.views.generic import ListView,CreateView,UpdateView,DeleteView
from .forms import form_outing,FilterForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponse
import datetime
import re
import xlwt
import xlrd


def check_warden(user):
    try:
        warden=Warden.objects.get(user=user)
        blocks=warden.hostelblock
    except:
        warden=None
        blocks=None
    return([warden,blocks])

def cal_weekends():
	d = datetime.date.today()
	w=[]
	while(d.weekday()!=6):
		d=d+datetime.timedelta(1)
	w.append(d.strftime("%Y-%m-%d"))
	w.append((d+datetime.timedelta(1)).strftime("%Y-%m-%d"))
	return w

# Create your views here.
def index(request):
    return render(request, 'ov/index.html')


def outingform(request):
    return render(request,'ov/outingform.html')


def registration(request):
    if(request.method=="POST"):
        registration_no=request.POST.get('registration_no').rstrip('\r')
        print(registration_no)
        registration_no=registration_no.upper()
        try:
            student=Student.objects.get(registration_no=registration_no)
            context={'student_name':student.name,
                        'reg_no':registration_no,
                        'weekends':cal_weekends(),
                        'hostel_block': HostelBlock.objects.all(),
                        'hostel_mess':HostelMess.objects.all()}
            return render(request,'ov/outingform.html',context)
        except:
            context={"error_message":"Invalid registration number"}
            return render(request,'ov/registration.html',context)
        

    return render(request,'ov/registration.html')


def studentimport(request):
    if request.method=="POST":
        csv_file = request.FILES["csv_file"]
        if not csv_file.name.endswith('.csv'):
            context={"error_message":["File is not csv type"]}
            return render(request, 'ov/studentimport.html', context)
        if csv_file.multiple_chunks():
            context={"error_message":["Uploaded file is too big."]}
            return render(request, 'ov/studentimport.html', context)
        file_data = csv_file.read().decode("utf-8")
        lines = file_data.split("\n")[1:]
        updated=[]
        for line in lines:
            inf=''
            fields = line.split(",")
            if('' in fields):
                fields.remove('')
            if(len(fields)==2):
                registration_no=fields[0].rstrip('\r').upper()
                name=fields[1].rstrip('\r').title()
                try:
                    student=Student.objects.get(registration_no=registration_no)
                    inf="Registration number already exists"
                    updated.append(inf)
                except:
                    validate=re.match(r'\d{2}[a-zA-Z]{3}\d{4}',registration_no)
                    if(validate):
                        student=Student(registration_no=registration_no,name=name)
                        student.save()
                        inf="Registration number:--"+registration_no
                    else:
                        inf="Invalid registration number:--"+registration_no+" at line number:-"+str(lines.index(line)+1)
                    updated.append(inf)
            else:
                updated.append("Got unexpected garbage value or unprocessed value at line number:->"+str(lines.index(line)+1))

        updated.append("-----------------Processing Completed-----------------")
        context={"error_message":updated
        }
        return render(request, "ov/studentimport.html", context)    

    return render(request,'ov/studentimport.html')

def outing_form(request,reg_no):
    student=Student.objects.get(registration_no=reg_no)
    data={'reg_no':reg_no,
    'student_name':student.name,
    'weekends':cal_weekends(),
    'hostel_block': HostelBlock.objects.all(),
    'hostel_mess':HostelMess.objects.all(),
    'error_message':[],
    'success_message':[]}
    if("GET"==request.method):
        return render(request,"ov/outingform.html",data)
    else:
        registration_no=reg_no
        name=Student.objects.get(registration_no=registration_no).name
        mess_type=request.POST["mess-Select"]
        student_phone_number=request.POST["student-phn"]
        parent_phone_number=request.POST["parent-phn"]
        hostel_block=request.POST["hostel-select"]
        hostel_block=HostelBlock.objects.get(block_name=hostel_block)
        mess_type=HostelMess.objects.get(MessName=mess_type)
        date_of_outing=request.POST['date']
        time_of_leaving=request.POST["t_leave"]
        time_of_arrival=request.POST["t_arrival"]
        visiting_address=request.POST["Visiting_address"]
        purpose_of_leaving=request.POST["pur_visiting"]
        permanent_address=request.POST["Permanent_address"]
        datetime_leave=date_of_outing+" "+time_of_leaving
        datetime_arrival=date_of_outing+" "+time_of_arrival
        limit_leav=date_of_outing+" 08:00"
        limit_arrv=date_of_outing+" 18:30"
        limit_leav=datetime.datetime.strptime(limit_leav,"%Y-%m-%d %H:%M")
        limit_arrv=datetime.datetime.strptime(limit_arrv,"%Y-%m-%d %H:%M")
        datetime_leave=datetime.datetime.strptime(datetime_leave,"%Y-%m-%d %H:%M")
        datetime_arrival=datetime.datetime.strptime(datetime_arrival,"%Y-%m-%d %H:%M")
        time_gap=datetime_arrival-datetime_leave
        if(len(parent_phone_number)!=10 or len(student_phone_number)!=10):
            data['error_message'].append("Phone number should be of length 10")    
        if(parent_phone_number==student_phone_number):
            data['error_message'].append("Parent phone number and student phone number should not be same")
        if((datetime_leave-limit_leav)<datetime.timedelta(0)):
            data['error_message'].append("leaving time should be after 8:00 AM")
        if((limit_arrv-datetime_arrival)<datetime.timedelta(0)):
            data['error_message'].append("Arrival time should be prior to 6:30 PM")
        if(time_gap<datetime.timedelta(0, 3600) and time_gap<datetime.timedelta(0, 37800)):
            data['error_message'].append("Time Gap between Arrival and leave should be greater than 1 hours and less than 9 hours")
        if(len(data['error_message'])!=0):
            return render(request,"ov/outingform.html",data)
        else:
            try: 
                prev_form=OutingForm.objects.get(registration_no=registration_no,date_of_outing=date_of_outing)
            except:
                prev_form=None
            if(prev_form):
                data['error_message'].append("You already filled the outing form on this day")
                return render(request,"ov/outingform.html",data)
            form=OutingForm(registration_no=registration_no,name=name,mess_type=mess_type,student_phone_number=student_phone_number,parent_phone_number=parent_phone_number,hostel_block=hostel_block,date_of_outing=date_of_outing,time_of_leaving=time_of_leaving,time_of_arrival=time_of_arrival,viiting_address=visiting_address,purpose_of_leaving=purpose_of_leaving,permanent_address=permanent_address)   
            form.save()
            data['success_message'].append("Your application is sent for the approval.Please wait for the SMS or Email Conformation")
            return render(request,"ov/outingform.html",data) 


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return render(request, 'ov/wardenview.html')
            else:
                return render(request, 'om/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'ov/login.html', {'error_message': 'Invalid login'})
    return render(request, 'ov/login.html')


def logout_user(request):
    logout(request)
    return render(request, 'ov/login.html')

@login_required
def WardenView(request):
    return render(request,'ov/wardenview.html')


def OutingApproval(request):
    forms=OutingForm.objects.filter(is_approved=False)
    p_ids=[i.id for i in forms]
    p_ids=str(p_ids)    
    context={
        'forms':forms,
        'p_ids':p_ids,
    }
    return render(request,'ov/outingformview.html',context)


def OutingDApproval(request):
    forms=OutingForm.objects.filter(is_approved=True)
    context={
        'forms':forms
    }
    return render(request,'ov/outingformdap.html',context)

def approve(request):
    pk=request.GET.get('user')
    pk=int(pk)
    print(pk)
    form=OutingForm.objects.get(pk=pk)
    form.is_approved=True
    form.save()
    return render(request,'ov/pp.html',{'pk':pk})

def dapprove(request):
    pk=request.GET.get('user')
    pk=int(pk)
    print(pk)
    form=OutingForm.objects.get(pk=pk)
    form.is_approved=False
    form.save()
    return render(request,'ov/pp.html',{'pk':pk})
    
def approveall(request):
    dates=cal_weekends()
    forms=OutingForm.objects.filter(is_approved=False,date_of_outing__in=dates)
    count=0
    for i in forms:
        i.is_approved=True
        i.save()
        count=count+1
    forms=OutingForm.objects.filter(is_approved=True)
    p_ids=[i.id for i in forms]
    p_ids=str(p_ids)    
    context={
        'forms':forms,
        'count':count,
        'p_ids':p_ids,
    }
    return render(request,'ov/outingformdap.html',context)

def dapproveall(request):
    dates=cal_weekends()
    forms=OutingForm.objects.filter(is_approved=True,date_of_outing__in=dates)
    count=0
    for i in forms:
        i.is_approved=False
        i.save()
        count=count+1
    forms=OutingForm.objects.filter(is_approved=False)
    p_ids=[i.id for i in forms]
    p_ids=str(p_ids)    
    context={
        'forms':forms,
        'count':count,
        'p_ids':p_ids,
    }
    return render(request,'ov/outingformview.html',context)

def filter_form(request):
    dates=cal_weekends()
    form = FilterForm(request.POST or None)
    if form.is_valid():
        object_list=OutingForm.objects.filter(is_approved=False)
        m1=request.POST.get('hostelblock')
        m2=request.POST.get('date_of_outing')
        if(m1=='' and m2==''):
            context={
                'form':form,
                'forms':OutingForm.objects.filter(is_approved=False,date_of_outing__in=dates),
                'error_message':"Please choose some options",    
            }
            return render(request,'ov/outingformview.html',context)    
        elif(m1=='' and m2!=''):
            m2=dates[int(m2)]
            object_list=OutingForm.objects.filter(is_approved=False,date_of_outing=m2)
        elif(m1!='' and m2==''):
            hostel_block=HostelBlock.objects.get(pk=int(m1))
            object_list=OutingForm.objects.filter(is_approved=False,date_of_outing__in=dates,hostel_block=hostel_block)
        elif(m1!='' and m2!=''):
            m2=dates[int(m2)]
            hostel_block=HostelBlock.objects.get(pk=int(m1))
            object_list=OutingForm.objects.filter(is_approved=False,date_of_outing=m2,hostel_block=hostel_block)
        p_ids=[i.id for i in object_list]
        p_ids=str(p_ids)
        context={
                'form':form,
                'forms':object_list,
                'error_message':"Activated Filter",
                'p_ids':p_ids,    
            }
        return render(request,'ov/outingformview.html',context)
    else:
        object_list=OutingForm.objects.filter(is_approved=False)
        p_ids=[i.id for i in object_list]
        p_ids=str(p_ids)
        context={
            'form':form,
            'forms':OutingForm.objects.filter(is_approved=False,date_of_outing__in=dates),
            'p_ids':p_ids,
        }
        return render(request,'ov/outingformview.html',context)
    


def export(request,p_ids):
    data=eval(p_ids)
    object_list=[]
    for i in data:
        object_list.append(OutingForm.objects.get(id=i))
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="OutingForms.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('OutingForms')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['Reg No.','Name','Leaving Time','Entry Time','Signature']
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    font_style = xlwt.XFStyle()
    rows=object_list
    for i in rows:
        row=[i.registration_no,i.name]
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)
    wb.save(response)
    return response
    





