from django.contrib import admin

from .models import AcknowledgementLetter  # ComplaintComment,
from .models import (
    AssignEngineer,
    AssignTechnician,
    Category,
    ChangePriority,
    ChangeStatus,
    Complaint,
    ComplaintPhoto,
)

admin.site.register(Complaint)
admin.site.register(ComplaintPhoto)
admin.site.register(AssignEngineer)
# admin.site.register(ComplaintComment)
admin.site.register(AcknowledgementLetter)
admin.site.register(Category)
admin.site.register(ChangeStatus)
admin.site.register(ChangePriority)
admin.site.register(AssignTechnician)
