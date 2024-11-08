from django.shortcuts import render, redirect
from django.views import View
from django.db.models import Q
from .models import Branch, Division, Batch, Subject, Teacher, Room, StudentElective, Timetable, ConflictResolution
from .forms import BranchForm, DivisionForm, BatchForm, SubjectForm, TeacherForm, RoomForm, StudentElectiveForm, TimetableForm, ConflictResolutionForm
import random

class LandingPageView(View):
    def get(self, request):
        return render(request, 'landing.html')

class BranchView(View):
    def get(self, request):
        branches = Branch.objects.all()
        form = BranchForm()
        return render(request, 'branch.html', {'branches': branches, 'form': form})

    def post(self, request):
        form = BranchForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('branch')

class DivisionView(View):
    def get(self, request):
        divisions = Division.objects.all()
        form = DivisionForm()
        return render(request, 'division.html', {'divisions': divisions, 'form': form})

    def post(self, request):
        form = DivisionForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('division')

class BatchView(View):
    def get(self, request):
        batches = Batch.objects.all()
        form = BatchForm()
        return render(request, 'batch.html', {'batches': batches, 'form': form})

    def post(self, request):
        form = BatchForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('batch')

class SubjectView(View):
    def get(self, request):
        subjects = Subject.objects.all()
        form = SubjectForm()
        return render(request, 'subject.html', {'subjects': subjects, 'form': form})

    def post(self, request):
        form = SubjectForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('subject')

class TeacherView(View):
    def get(self, request):
        teachers = Teacher.objects.all()
        form = TeacherForm()
        return render(request, 'teacher.html', {'teachers': teachers, 'form': form})

    def post(self, request):
        form = TeacherForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('teacher')

class RoomView(View):
    def get(self, request):
        rooms = Room.objects.all()
        form = RoomForm()
        return render(request, 'room.html', {'rooms': rooms, 'form': form})

    def post(self, request):
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('room')

class StudentElectiveView(View):
    def get(self, request):
        student_electives = StudentElective.objects.all()
        form = StudentElectiveForm()
        return render(request, 'student_elective.html', {'student_electives': student_electives, 'form': form})

    def post(self, request):
        form = StudentElectiveForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('student_elective')

class TimetableView(View):
    def get(self, request):
        timetable = Timetable.objects.all()
        form = TimetableForm()
        return render(request, 'timetable.html', {'timetable': timetable, 'form': form})

    def post(self, request):
        form = TimetableForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('timetable')

class ConflictResolutionView(View):
    def get(self, request):
        conflicts = ConflictResolution.objects.all()
        form = ConflictResolutionForm()
        return render(request, 'conflict_resolution.html', {'conflicts': conflicts, 'form': form})

    def post(self, request):
        form = ConflictResolutionForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('conflict_resolution')

class GenerateTimetableView(View):
    def get(self, request):
        self.generate_timetable()
        return redirect('timetable')

    def generate_timetable(self):
        # Clear existing timetable
        Timetable.objects.all().delete()
        ConflictResolution.objects.all().delete()

        divisions = Division.objects.all()
        subjects = Subject.objects.all()
        teachers = Teacher.objects.all()
        rooms = Room.objects.filter(is_lab=False)
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        time_slots = ['09:00-10:00', '10:00-11:00', '11:00-12:00', '12:00-13:00', '14:00-15:00', '15:00-16:00']

        for division in divisions:
            for day in days:
                for time_slot in time_slots:
                    subject = random.choice(subjects.filter(branch=division.branch))
                    teacher = random.choice(teachers.filter(subjects=subject))
                    room = random.choice(rooms)

                    # Check for conflicts
                    existing_entry = Timetable.objects.filter(
                        Q(division=division, day=day, time_slot=time_slot) |
                        Q(teacher=teacher, day=day, time_slot=time_slot) |
                        Q(room=room, day=day, time_slot=time_slot)
                    ).first()

                    if existing_entry:
                        # Create conflict resolution entry
                        ConflictResolution.objects.create(
                            timetable_entry=existing_entry,
                            conflict_type='Scheduling Conflict',
                            resolution_status='Unresolved',
                            notes=f'Conflict with new entry: Division {division}, Subject {subject}, Teacher {teacher}, Room {room}'
                        )
                    else:
                        # Create timetable entry
                        Timetable.objects.create(
                            division=division,
                            day=day,
                            time_slot=time_slot,
                            subject=subject,
                            teacher=teacher,
                            room=room
                        )

        self.assign_labs()

    def assign_labs(self):
        lab_rooms = Room.objects.filter(is_lab=True)
        batches = Batch.objects.all()
        lab_subjects = Subject.objects.filter(is_lab=True)

        for batch in batches:
            lab_subjects_filtered = lab_subjects.filter(branch=batch.division.branch)
            if lab_subjects_filtered.exists():
                lab_subject = random.choice(lab_subjects_filtered)
            else:
                # Handle the case where no subjects are found
                lab_subject = None  # or some fallback logic
            lab_room = random.choice(lab_rooms)
            day = random.choice(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'])
            time_slot = random.choice(['09:00-11:00', '11:00-13:00', '14:00-16:00'])

            # Check for conflicts
            existing_entry = Timetable.objects.filter(
                Q(division=batch.division, day=day, time_slot=time_slot) |
                Q(room=lab_room, day=day, time_slot=time_slot)
            ).first()

            if existing_entry:
                # Create conflict resolution entry
                ConflictResolution.objects.create(
                    timetable_entry=existing_entry,
                    conflict_type='Lab Scheduling Conflict',
                    resolution_status='Unresolved',
                    notes=f'Conflict with new lab entry: Batch {batch}, Subject {lab_subject}, Room {lab_room}'
                )
            else:
                # Create timetable entry for lab
                Timetable.objects.create(
                    division=batch.division,
                    day=day,
                    time_slot=time_slot,
                    subject=lab_subject,
                    teacher=random.choice(Teacher.objects.filter(subjects=lab_subject)),
                    room=lab_room
                )