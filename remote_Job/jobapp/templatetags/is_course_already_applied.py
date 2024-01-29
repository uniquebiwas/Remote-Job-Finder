from django import template

from jobapp.models import Enrollment

register = template.Library()


@register.simple_tag(name='is_course_already_applied')
def is_course_already_applied(course, user):
    applied = Enrollment.objects.filter(course=course, user=user)
    if applied:
        return True
    else:
        return False
