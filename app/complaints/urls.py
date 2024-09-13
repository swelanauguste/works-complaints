from django.urls import path

from . import views

urlpatterns = [
    path("", views.ComplaintListView.as_view(), name="list"),
    path("create/", views.ComplaintCreateView.as_view(), name="create"),
    path(
        "investigator/create/",
        views.ComplaintInvestigatorCreateView.as_view(),
        name="complaint-investigator-create",
    ),
    path("detail/<slug:slug>/", views.complaint_detail, name="detail"),
]
