from django.db import models


class RecruitmentApplication(models.Model):
    STATUS_CHOICES = [
        ("New", "New"),
        ("Under Review", "Under Review"),
        ("Shortlisted", "Shortlisted"),
        ("Closed", "Closed"),
    ]

    full_name = models.CharField(max_length=120)
    phone = models.CharField(max_length=40)
    email = models.EmailField()
    area_of_interest = models.CharField(max_length=120)
    position_applied_for = models.CharField(max_length=120, blank=True)
    experience = models.TextField()
    personal_statement = models.TextField()
    cv = models.FileField(upload_to="recruitment_cvs/%Y/%m/", blank=True, null=True)
    consent = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="New")
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Recruitment application"
        verbose_name_plural = "Recruitment applications"
        ordering = ["-submitted_at"]

    def __str__(self):
        return f"{self.full_name} ({self.status})"
