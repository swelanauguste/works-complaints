from django.urls import path

from . import views

urlpatterns = [
    path("", views.complaint_list, name="list"),
    path("detail/<slug:slug>/", views.complaint_detail, name="detail"),
    path("update/<slug:slug>/", views.complaint_update, name="update"),
    path("create/", views.complaint_create, name="create"),
    path(
        "create-complaint-photo/<slug:slug>/",
        views.create_complaint_photo,
        name="create-complaint-photo",
    ),
    path(
        "assign-technician/<slug:slug>/",
        views.assign_technician,
        name="assign-technician",
    ),
    path(
        "assign-engineer/<slug:slug>/",
        views.assign_engineer,
        name="assign-engineer",
    ),
    path(
        "add-acknowledgement-letter/<slug:slug>/",
        views.add_acknowledgement_letter,
        name="add-acknowledgement-letter",
    ),
    path(
        "change-status/<slug:slug>/",
        views.change_status,
        name="change-status",
    ),
    path(
        "change-priority/<slug:slug>/",
        views.change_priority,
        name="change-priority",
    ),
]

