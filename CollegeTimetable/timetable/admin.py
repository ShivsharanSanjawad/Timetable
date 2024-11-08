from django.contrib import admin
from .models import Branch, Division, Batch, Subject, Teacher, Room, StudentElective, Timetable, ConflictResolution

admin.site.register(Branch)
admin.site.register(Division)
admin.site.register(Batch)
admin.site.register(Subject)
admin.site.register(Teacher)
admin.site.register(Room)
admin.site.register(StudentElective)
admin.site.register(Timetable)
admin.site.register(ConflictResolution)