from django import forms

from .models import Complaint, ComplaintInvestigator


class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = "__all__"
        exclude = ["slug", "created_at", "category"]
        widgets = {
            "complaint": forms.Textarea(attrs={"rows": 5}),
        }


class ComplaintInvestigatorForm(forms.ModelForm):
    class Meta:
        model = ComplaintInvestigator
        fields = "__all__"
        exclude = ["created_at", "created_by"]
        widgets = {
            "complaint": forms.HiddenInput(),
            "investigator": forms.Select(attrs={"onchange": "this.form.submit()"}),
        }
