from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from .models import RecruitmentApplication


class WorkWithUsPageTests(TestCase):
    def test_work_with_us_page_renders(self):
        response = self.client.get(reverse("work_with_us"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Work With Us")
        self.assertContains(response, "JOIN OUR TEAM")
        self.assertContains(
            response, "We do not have any advertised openings at the moment"
        )

    def test_invalid_cv_upload_is_rejected(self):
        response = self.client.post(
            reverse("work_with_us"),
            {
                "full_name": "Asha Njeri",
                "phone": "+254700000000",
                "email": "asha@example.com",
                "area_of_interest": "Hospitality and guest service",
                "position_applied_for": "Server",
                "experience": "Two years in hospitality",
                "personal_statement": "I am committed to warm service.",
                "consent": "on",
                "cv": SimpleUploadedFile(
                    "resume.exe", b"not-a-pdf", content_type="application/x-msdownload"
                ),
            },
            follow=True,
        )

        self.assertContains(response, "Please check the highlighted fields")
        self.assertEqual(RecruitmentApplication.objects.count(), 0)

    def test_oversized_cv_upload_is_rejected(self):
        oversized_file = SimpleUploadedFile(
            "resume.pdf",
            b"x" * (6 * 1024 * 1024),
            content_type="application/pdf",
        )

        response = self.client.post(
            reverse("work_with_us"),
            {
                "full_name": "Asha Njeri",
                "phone": "+254700000000",
                "email": "asha@example.com",
                "area_of_interest": "Restaurant service",
                "position_applied_for": "Waiter",
                "experience": "Two years in hospitality",
                "personal_statement": "I am committed to warm service.",
                "consent": "on",
                "cv": oversized_file,
            },
            follow=True,
        )

        self.assertContains(response, "Please check the highlighted fields")
        self.assertEqual(RecruitmentApplication.objects.count(), 0)

    def test_valid_application_is_saved(self):
        response = self.client.post(
            reverse("work_with_us"),
            {
                "full_name": "Asha Njeri",
                "phone": "+254700000000",
                "email": "asha@example.com",
                "area_of_interest": "Hospitality and guest service",
                "position_applied_for": "Server",
                "experience": "Two years in hospitality",
                "personal_statement": "I am committed to warm service.",
                "consent": "on",
            },
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(RecruitmentApplication.objects.count(), 1)
        application = RecruitmentApplication.objects.get()
        self.assertEqual(application.status, "New")
        self.assertEqual(application.full_name, "Asha Njeri")
