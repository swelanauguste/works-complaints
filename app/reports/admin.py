from django.contrib import admin

from .models import EngineerReportDocument, TechnicalReportDocument

admin.site.register(TechnicalReportDocument)
admin.site.register(EngineerReportDocument)
