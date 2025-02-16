from django.contrib import admin

from .models import (
    ComplaintReview,
    EngineeringAssistantReportDocument,
    EngineerReportDocument,
    Programme,
    TechnicalReportDocument,
)

admin.site.register(TechnicalReportDocument)
admin.site.register(EngineerReportDocument)
admin.site.register(ComplaintReview)
admin.site.register(Programme)
admin.site.register(EngineeringAssistantReportDocument)
