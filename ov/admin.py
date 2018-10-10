from django.contrib import admin
from ov.models import HostelBlock,OutingForm,Student,HostelMess,Warden

# Register your models here.

class outingformclass(admin.ModelAdmin):
    list_filter = ['hostel_block','is_approved']
    date_hierarchy = 'date_of_outing'


admin.site.register(HostelBlock)
admin.site.register(OutingForm,outingformclass)
admin.site.register(Student)
admin.site.register(HostelMess)
admin.site.register(Warden)


