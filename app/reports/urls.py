from django.urls import path

from .views import add_engineer_report_document, add_technical_report_document

urlpatterns = [
    path(
        "add-technical-report-document/<slug:slug>",
        add_technical_report_document,
        name="add-technical-report-document",
    ),
    path(
        "add-engineer-report-document/<slug:slug>",
        add_engineer_report_document,
        name="add-engineer-report-document",
    ),
    # path(
    #     "engineer-report-document-create/",
    #     EngineerReportDocumentDocumentCreateView.as_view(),
    #     name="engineer-report-document-create",
    # ),
]
