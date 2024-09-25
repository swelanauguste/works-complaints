from django.contrib import admin

from .models import ComplaintReview, EngineerReportDocument, TechnicalReportDocument, Programme

admin.site.register(TechnicalReportDocument)
admin.site.register(EngineerReportDocument)
admin.site.register(ComplaintReview)
admin.site.register(Programme)