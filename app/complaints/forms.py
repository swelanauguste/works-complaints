from django import forms

from .models import (
    AcknowledgementLetter,
    AssignInvestigator,
    ChangePriority,
    ChangeStatus,
    Complaint,
    ComplaintPhoto,
    User,
)


class ChangePriorityForm(forms.ModelForm):
    class Meta:
        model = ChangePriority
        fields = [
            "priority",
        ]
        widgets = {
            "complaint": forms.HiddenInput(),
            "comment": forms.Textarea(attrs={"rows": 5}),
            "priority": forms.Select(attrs={"onchange": "this.form.submit();"}),
        }


class ChangeStatusForm(forms.ModelForm):
    class Meta:
        model = ChangeStatus
        fields = [
            "status",
        ]
        widgets = {
            "complaint": forms.HiddenInput(),
            "comment": forms.Textarea(attrs={"rows": 5}),
            "status": forms.Select(attrs={"onchange": "this.form.submit();"}),
        }


class AssignInvestigatorForm(forms.ModelForm):
    class Meta:
        model = AssignInvestigator
        fields = ["investigators", "comment"]
        widgets = {
            "complaint": forms.HiddenInput(),
            "comment": forms.Textarea(attrs={"rows": 5}),
        }

    def __init__(self, *args, **kwargs):
        super(AssignInvestigatorForm, self).__init__(*args, **kwargs)
        # Filter users based on roles 'admin', 'investigator', 'engineer'
        self.fields["investigators"].queryset = User.objects.filter(
            role__in=["admin", "engineer"]
        )


class AcknowledgementLetterForm(forms.ModelForm):
    class Meta:
        model = AcknowledgementLetter
        fields = ["letter", "comment"]
        widgets = {
            "complaint": forms.HiddenInput(),
            "comment": forms.Textarea(attrs={"rows": 5}),
        }


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


class ComplaintPhotoForm(forms.ModelForm):
    photos = MultipleFileField(label="Select files", required=False)
    comment = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = ComplaintPhoto
        fields = ["photos", "comment"]
        widgets = {
            "complaint": forms.HiddenInput(),
            "comment": forms.Textarea(attrs={"rows": 5}),
        }


class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = "__all__"
        exclude = ["slug", "created_at", "category", "created_by", "updated_by"]
        widgets = {
            "complaint": forms.Textarea(attrs={"rows": 5}),
            "date": forms.DateInput(attrs={"type": 'date'}),
        }


# class ComplaintInvestigatorForm(forms.ModelForm):
#     class Meta:
#         model = ComplaintInvestigator
#         fields = "__all__"
#         exclude = ["created_at", "created_by"]
#         widgets = {
#             "complaint": forms.HiddenInput(),
#             "investigator": forms.Select(attrs={"onchange": "this.form.submit()"}),
#         }
