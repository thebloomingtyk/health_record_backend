from django.db import models

class Room(models.Model):
    ROOM_CHOICES = [
        ("R1", "Room 1"),
        ("R2", "Room 2"),
        ("R3", "Room 3"),
        ("R4", "Room 4"),
        ("R5", "Room 5"),
    ]
    room_number = models.CharField(max_length=10, choices=ROOM_CHOICES) # TODO unique=True
    doctor_name = models.CharField(max_length=100)

    def __str__(self):
        return self.get_room_number_display()


class Consultation(models.Model):
    patient_name = models.CharField(max_length=100)
    patient_age = models.PositiveIntegerField()
    consultation_time = models.DateTimeField(auto_now_add=True)
    recommended_treatment = models.TextField()
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.doctor_name} - {self.patient_name} - {self.room}"

