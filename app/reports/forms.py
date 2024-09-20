from django import forms

from .models import EngineerReportDocument, TechnicalReportDocument


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class TechnicalReportDocumentForm(forms.ModelForm):
    documents = MultipleFileField(label="Select files", required=False)
    comment = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = TechnicalReportDocument
        fields = ["report_date", "documents", "comment"]
        widgets = {
            "report": forms.HiddenInput(),
            "comment": forms.Textarea(attrs={"rows": 5}),
            "report_date": forms.DateInput(attrs={"type": "date"}),
        }


class EngineerReportDocumentForm(forms.ModelForm):
    documents = MultipleFileField(label="Select files", required=False)
    comment = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = EngineerReportDocument
        fields = ["report_date", "documents", "comment"]
        widgets = {
            "report": forms.HiddenInput(),
            "comment": forms.Textarea(attrs={"rows": 5}),
            "report_date": forms.DateInput(attrs={"type": "date"}),
        }
