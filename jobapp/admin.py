from django.contrib import admin
from .models import *


admin.site.register(Category)

class ApplicantAdmin(admin.ModelAdmin):
    list_display = ('job','user','timestamp','status')
    
admin.site.register(Applicant,ApplicantAdmin)


class JobAdmin(admin.ModelAdmin):
    list_display = ('title','is_published','is_closed','timestamp')

admin.site.register(Job,JobAdmin)

class BookmarkJobAdmin(admin.ModelAdmin):
    list_display = ('job','user','timestamp')
admin.site.register(BookmarkJob,BookmarkJobAdmin)

class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('author_name', 'content',)
    search_fields = ('author_name', 'content',)

admin.site.register(Testimonial, TestimonialAdmin)

class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'tag', )
    list_filter = ('tag',)
    search_fields = ('name', 'description',)
admin.site.register(Course,CourseAdmin)

class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('course','user','roomid','timestamp')
    
admin.site.register(Enrollment,EnrollmentAdmin)