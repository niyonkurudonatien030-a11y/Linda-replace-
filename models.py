from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # Use email as a contact field; production registration must verify ownership.
    email = models.EmailField(unique=True)
    headline = models.CharField(max_length=180, blank=True)
    location = models.CharField(max_length=120, blank=True)
    is_verified_professional = models.BooleanField(default=False)  # Set only after reviewed evidence.

    def __str__(self):
        return self.username

class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="posts")
    body = models.TextField(max_length=5000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_hidden = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Post {self.pk} by {self.author}"

class Opportunity(models.Model):
    class Kind(models.TextChoices):
        JOB = "JOB", "Job"
        INTERNSHIP = "INTERNSHIP", "Internship"
        SCHOLARSHIP = "SCHOLARSHIP", "Scholarship"
        RESEARCH = "RESEARCH", "Research"
        FUNDING = "FUNDING", "Funding"

    publisher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="opportunities")
    title = models.CharField(max_length=180)
    kind = models.CharField(max_length=20, choices=Kind.choices)
    organisation = models.CharField(max_length=180)
    location = models.CharField(max_length=120, blank=True)
    description = models.TextField(max_length=10000)
    application_url = models.URLField(blank=True)
    deadline = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_open = models.BooleanField(default=True)

    class Meta:
        ordering = ["-created_at"]

class Report(models.Model):
    class Status(models.TextChoices):
        OPEN = "OPEN", "Open"
        REVIEWING = "REVIEWING", "Reviewing"
        ACTIONED = "ACTIONED", "Actioned"
        DISMISSED = "DISMISSED", "Dismissed"

    reporter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reports")
    target_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reports_against")
    reason = models.CharField(max_length=80)
    details = models.TextField(max_length=3000, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.OPEN)
    created_at = models.DateTimeField(auto_now_add=True)
    reviewer_note = models.TextField(blank=True)

class Appeal(models.Model):
    class Status(models.TextChoices):
        RECEIVED = "RECEIVED", "Received"
        IN_REVIEW = "IN_REVIEW", "In review"
        UPHELD = "UPHELD", "Restriction upheld"
        RESTORED = "RESTORED", "Access restored"
        NEEDS_INFO = "NEEDS_INFO", "More information needed"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="appeals")
    subject = models.CharField(max_length=180)
    explanation = models.TextField(max_length=5000)
    requested_resolution = models.CharField(max_length=500)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.RECEIVED)
    created_at = models.DateTimeField(auto_now_add=True)
    staff_response = models.TextField(blank=True)
