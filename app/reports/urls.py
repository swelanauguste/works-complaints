from django.urls import path

from . import views

urlpatterns = [
    path(
        "add-technical-report-document/<slug:slug>",
        views.add_technical_report_document,
        name="add-technical-report-document",
    ),
    path(
        "add-engineer-report-document/<slug:slug>",
        views.add_engineering_assistant_report_document,
        name="add-engineering-assistant-report-document",
    ),
    path(
        "add-engineer-report-document/<slug:slug>",
        views.add_engineer_report_document,
        name="add-engineer-report-document",
    ),
    path(
        "complaint-review/<slug:slug>/",
        views.complaint_review,
        name="complaint-review",
    ),
]
