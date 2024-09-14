from django.urls import path

from . import views

urlpatterns = [
    path("", views.complaint_list, name="list"),
    path("create/", views.complaint_create, name="create"),
    path(
        "investigator/create/",
        views.ComplaintInvestigatorCreateView.as_view(),
        name="complaint-investigator-create",
    ),
    path("detail/<slug:slug>/", views.complaint_detail, name="detail"),
]
