from django.contrib import admin

from .models import ComplaintReview, EngineerReportDocument, TechnicalReportDocument

admin.site.register(TechnicalReportDocument)
admin.site.register(EngineerReportDocument)
admin.site.register(ComplaintReview)
