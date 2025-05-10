from django.contrib import admin
from django.utils.html import format_html
from .models import Job, Application, CustomUser

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('job_title', 'company_name', 'location', 'posted_by', 'posted_at')

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('job', 'applicant', 'applied_at', 'resume_link')
    search_fields = ('job__job_title', 'applicant__username')

    def resume_link(self, obj):
        if obj.resume:
            return format_html('<a href="{}" target="_blank">Download</a>', obj.resume.url)
        return "No resume uploaded."
    resume_link.short_description = "Resume"

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'address', 'contact_number')
    search_fields = ('username', 'email')
