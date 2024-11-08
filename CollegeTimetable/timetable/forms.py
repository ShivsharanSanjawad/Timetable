from django import forms
from .models import Branch, Division, Batch, Subject, Teacher, Room, StudentElective, Timetable, ConflictResolution

class BranchForm(forms.ModelForm):
    class Meta:
        model = Branch
        fields = ['name']

class DivisionForm(forms.ModelForm):
    class Meta:
        model = Division
        fields = ['name', 'branch']

class BatchForm(forms.ModelForm):
    class Meta:
        model = Batch
        fields = ['name', 'division']

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name', 'branch', 'is_lab', 'is_mandatory', 'is_elective', 'lectures_per_week']

class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['name', 'subjects']

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['name', 'capacity', 'is_lab']

class StudentElectiveForm(forms.ModelForm):
    class Meta:
        model = StudentElective
        fields = ['student_name', 'elective']

class TimetableForm(forms.ModelForm):
    class Meta:
        model = Timetable
        fields = ['division', 'day', 'time_slot', 'subject', 'teacher', 'room']

class ConflictResolutionForm(forms.ModelForm):
    class Meta:
        model = ConflictResolution
        fields = ['timetable_entry', 'conflict_type', 'resolution_status', 'notes']