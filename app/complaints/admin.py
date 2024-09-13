from django.contrib import admin

from .models import (
    Category,
    Complaint,
    ComplaintComment,
    ComplaintInvestigator,
    Report,
    ReportComment,
    Zone,
)

admin.site.register(Complaint)
admin.site.register(ComplaintComment)
admin.site.register(Report)
admin.site.register(ReportComment)
admin.site.register(Zone)
admin.site.register(ComplaintInvestigator)
admin.site.register(Category)
