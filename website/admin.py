from django.contrib import admin

from .models import RecruitmentApplication


@admin.register(RecruitmentApplication)
class RecruitmentApplicationAdmin(admin.ModelAdmin):
    list_display = ("full_name", "email", "area_of_interest", "status", "submitted_at")
    list_filter = ("status", "area_of_interest", "submitted_at")
    search_fields = (
        "full_name",
        "email",
        "phone",
        "position_applied_for",
        "area_of_interest",
    )
    readonly_fields = ("submitted_at",)
