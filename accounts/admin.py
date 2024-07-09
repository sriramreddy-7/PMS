from django.contrib import admin
from .models import Profile, StudentProfile, InstituteProfile, RecruiterProfile,JobOpening,JobApplication,Request,Skill
from .models import StudentDocument


admin.site.register(Profile)
admin.site.register(StudentProfile)
admin.site.register(InstituteProfile)
admin.site.register(RecruiterProfile)
admin.site.register(JobOpening)
admin.site.register(JobApplication)
admin.site.register(Request)
admin.site.register(Skill)
admin.site.register(StudentDocument)