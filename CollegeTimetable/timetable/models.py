from django.db import models

class Branch(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Division(models.Model):
    name = models.CharField(max_length=10)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.branch.name} - {self.name}"

class Batch(models.Model):
    name = models.CharField(max_length=10)
    division = models.ForeignKey(Division, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.division} - {self.name}"

class Subject(models.Model):
    name = models.CharField(max_length=100)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    is_lab = models.BooleanField(default=False)
    is_mandatory = models.BooleanField(default=True)
    is_elective = models.BooleanField(default=False)
    lectures_per_week = models.IntegerField(default=3)

    def __str__(self):
        return f"{self.name} ({self.branch.name})"

class Teacher(models.Model):
    name = models.CharField(max_length=100)
    subjects = models.ManyToManyField(Subject)

    def __str__(self):
        return self.name

class Room(models.Model):
    name = models.CharField(max_length=50)
    capacity = models.IntegerField()
    is_lab = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class StudentElective(models.Model):
    student_name = models.CharField(max_length=100)
    elective = models.ForeignKey(Subject, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.student_name} - {self.elective.name}"

class Timetable(models.Model):
    division = models.ForeignKey(Division, on_delete=models.CASCADE)
    day = models.CharField(max_length=10)
    time_slot = models.CharField(max_length=20)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.division} - {self.day} - {self.time_slot}"

class ConflictResolution(models.Model):
    timetable_entry = models.ForeignKey(Timetable, on_delete=models.CASCADE)
    conflict_type = models.CharField(max_length=50)
    resolution_status = models.CharField(max_length=20)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Conflict: {self.timetable_entry} - {self.conflict_type}"