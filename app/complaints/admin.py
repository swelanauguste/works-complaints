from django.contrib import admin

from .models import (
    AcknowledgementLetter,
    AssignEngineer,  # Category,
    AssignTechnician,
    ChangePriority,
    ChangeStatus,
    Complaint,
    ComplaintComment,
    ComplaintPhoto,
)

admin.site.register(ComplaintPhoto)
admin.site.register(ComplaintComment)
admin.site.register(AcknowledgementLetter)
# admin.site.register(Category)
admin.site.register(ChangeStatus)
admin.site.register(ChangePriority)


class ComplaintAdmin(admin.ModelAdmin):
    list_display = ["ref", "zone", "phone", "address", "created_at", "form"]
    list_editable = ["zone", "form"]


admin.site.register(Complaint, ComplaintAdmin)


class AssignEngineerAdmin(admin.ModelAdmin):
    list_display = [
        "complaint",
        "engineer",
        "created_by",
    ]
    list_editable = [
        "engineer",
    ]


admin.site.register(AssignEngineer, AssignEngineerAdmin)


class AssignTechnicianAdmin(admin.ModelAdmin):
    list_display = [
        "complaint",
        "technician",
        "created_by",
    ]
    list_editable = [
        "technician",
    ]


admin.site.register(AssignTechnician, AssignTechnicianAdmin)
