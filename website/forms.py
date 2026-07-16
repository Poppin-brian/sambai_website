import os
import re

from django import forms
from django.core.exceptions import ValidationError

from .models import RecruitmentApplication


def _sanitize_filename(value: str) -> str:
    value = os.path.basename(value).strip().lower()
    value = re.sub(r"[^a-z0-9._-]+", "-", value)
    value = re.sub(r"-+", "-", value).strip(".-")
    return value or "document"


class InquiryForm(forms.Form):
    INQUIRY_CHOICES = [
        ("Guest Spaces", "Guest Spaces"),
        ("Restaurant", "Restaurant"),
        ("Bar & Beverages", "Bar & Beverages"),
        ("Events & Gatherings", "Events & Gatherings"),
        ("Directions / Location", "Directions / Location"),
        ("General Inquiry", "General Inquiry"),
    ]

    full_name = forms.CharField(
        label="Full name",
        max_length=120,
        widget=forms.TextInput(attrs={"placeholder": "Your name"}),
    )
    phone = forms.CharField(
        label="Phone number",
        max_length=40,
        widget=forms.TextInput(attrs={"placeholder": "+254 ..."}),
    )
    email = forms.EmailField(
        label="Email address",
        required=False,
        widget=forms.EmailInput(attrs={"placeholder": "you@example.com"}),
    )
    preferred_date = forms.DateField(
        label="Preferred date",
        required=False,
        widget=forms.DateInput(attrs={"type": "date"}),
    )
    number_of_people = forms.IntegerField(
        label="Number of people",
        required=False,
        min_value=1,
        widget=forms.NumberInput(attrs={"placeholder": "Optional"}),
    )
    inquiry_type = forms.ChoiceField(
        label="Inquiry type",
        choices=[("", "Select an inquiry type"), *INQUIRY_CHOICES],
    )
    message = forms.CharField(
        label="Message",
        widget=forms.Textarea(
            attrs={"rows": 5, "placeholder": "Tell us what you need"}
        ),
    )


class RecruitmentApplicationForm(forms.ModelForm):
    honey = forms.CharField(required=False, widget=forms.HiddenInput())

    class Meta:
        model = RecruitmentApplication
        fields = [
            "full_name",
            "phone",
            "email",
            "area_of_interest",
            "position_applied_for",
            "experience",
            "personal_statement",
            "cv",
            "consent",
        ]
        labels = {
            "full_name": "Full name",
            "phone": "Phone number",
            "email": "Email address",
            "area_of_interest": "Area of interest",
            "position_applied_for": "Position applied for (optional)",
            "experience": "Relevant experience",
            "personal_statement": "Short personal statement",
            "cv": "CV upload (optional)",
            "consent": "I consent to The Hive retaining my information for recruitment purposes.",
        }
        widgets = {
            "full_name": forms.TextInput(attrs={"placeholder": "Your full name"}),
            "phone": forms.TextInput(attrs={"placeholder": "+254 ..."}),
            "email": forms.EmailInput(attrs={"placeholder": "you@example.com"}),
            "area_of_interest": forms.Select(attrs={"placeholder": "Select an area"}),
            "position_applied_for": forms.TextInput(attrs={"placeholder": "Optional"}),
            "experience": forms.Textarea(
                attrs={"rows": 4, "placeholder": "Describe your relevant experience"}
            ),
            "personal_statement": forms.Textarea(
                attrs={"rows": 4, "placeholder": "Tell us a bit about yourself"}
            ),
            "cv": forms.ClearableFileInput(attrs={"accept": ".pdf,.doc,.docx"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["area_of_interest"].choices = [
            ("", "Select an area of interest"),
            ("Hospitality and guest service", "Hospitality and guest service"),
            ("Restaurant service", "Restaurant service"),
            ("Kitchen support", "Kitchen support"),
            ("Housekeeping and maintenance", "Housekeeping and maintenance"),
            ("Events support", "Events support"),
            ("Security and general operations", "Security and general operations"),
        ]
        self.fields["consent"].required = True

    def clean_honey(self):
        if self.cleaned_data.get("honey"):
            raise ValidationError("Spam detected")
        return self.cleaned_data.get("honey")

    def clean_cv(self):
        cv = self.cleaned_data.get("cv")
        if not cv:
            return None

        allowed_types = {
            "application/pdf",
            "application/msword",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        }
        if cv.content_type not in allowed_types:
            raise ValidationError("Please upload a PDF, DOC, or DOCX file.")

        if cv.size > 5 * 1024 * 1024:
            raise ValidationError("Please upload a file smaller than 5 MB.")

        sanitized_name = _sanitize_filename(cv.name)
        if sanitized_name != cv.name:
            cv.name = sanitized_name
        return cv

    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data.get("consent"):
            self.add_error(
                "consent",
                "You must confirm that you allow The Hive to retain your information.",
            )
        return cleaned_data
