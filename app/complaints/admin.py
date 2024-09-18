from django.contrib import admin

from .models import Category, Complaint, ComplaintPhoto, Zone, AcknowledgementLetter, AssignInvestigator, ChangeStatus, ChangePriority  # ComplaintComment,

admin.site.register(Complaint)
admin.site.register(ComplaintPhoto)
admin.site.register(AssignInvestigator)
# admin.site.register(ComplaintComment)
admin.site.register(AcknowledgementLetter)
admin.site.register(Zone)
admin.site.register(Category)
admin.site.register(ChangeStatus)
admin.site.register(ChangePriority)
