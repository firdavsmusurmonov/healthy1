from django.db import models
from account.models import Customuser, Profession


class Schedule(models.Model):
    STATUS_CHOICES = (
        ('upcoming', 'Upcoming'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled')
    )
    user = models.ForeignKey(Customuser, related_name="schedule_user", null=True, blank=True, on_delete=models.SET_NULL)
    doctor = models.ForeignKey(Customuser, related_name="schedule_doctor", null=True, blank=True,
                               on_delete=models.SET_NULL)
    profession = models.ForeignKey(Profession, related_name="schedule_profession", null=True, blank=True,
                                   on_delete=models.CASCADE)
    start_datetime = models.DateTimeField(null=True, blank=True)
    desc = models.TextField()
    status = models.CharField(choices=STATUS_CHOICES, max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return str(self.user)
