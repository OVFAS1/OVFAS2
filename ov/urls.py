from django.contrib import admin
from django.urls import path,include
from django.contrib.auth import views as auth_views
from . import views


app_name="ov"

urlpatterns = [

    path('admin/', admin.site.urls),
    path('',views.index,name="index"),
    path('outingform/',views.outingform,name='outingform'),
    path('registration/',views.registration,name='registration'),
    path('studentimport/',views.studentimport,name='student-import'),
    path('outingform_filled/<str:reg_no>',views.outing_form,name='outingfill'),
    path('login/',views.login_user,name='login'),
    path('wardenview/',views.WardenView,name='warden'),
    path('outingapproval/',views.OutingApproval,name="outing-approval"),
    path('outingdapproval/',views.OutingDApproval,name="outing-dapproval"),
    path('approve/',views.approve,name="approve"),
    path('dapprove/',views.dapprove,name="dapprove"),
    path('approveall/',views.approveall,name="approveall"),
    path('dapproveall/',views.dapproveall,name="dapproveall"),
    path('applyfilter/',views.filter_form,name="filter-forms"),
    path('exportouting/<str:p_ids>',views.export,name="export-outing"),




    
    
   



]
