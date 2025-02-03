from django import forms

from .models import (
    AcknowledgementLetter,
    AssignAssistantEngineer,
    AssignEngineer,
    AssignTechnician,
    ChangePriority,
    ChangeStatus,
    Complaint,
    ComplaintComment,
    ComplaintPhoto,
    User,
)


class ComplaintCommentForm(forms.ModelForm):
    class Meta:
        model = ComplaintComment
        fields = ["comment"]
        widgets = {
            "comment": forms.Textarea(
                attrs={"rows": 3, "placeholder": "Add a comment..."}
            ),
        }


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


class AssignTechnicianForm(forms.ModelForm):
    class Meta:
        model = AssignTechnician
        fields = [
            "technician",
        ]
        widgets = {
            "complaint": forms.HiddenInput(),
            "technician": forms.Select(attrs={"onchange": "this.form.submit();"}),
        }

    def __init__(self, *args, **kwargs):
        super(AssignTechnicianForm, self).__init__(*args, **kwargs)
        # Filter users based on roles 'technician'
        self.fields["technician"].queryset = User.objects.filter(
            role__in=["technician"]
        )


class AssignAssistantEngineerForm(forms.ModelForm):
    class Meta:
        model = AssignAssistantEngineer
        fields = [
            "assistant_engineer",
        ]
        widgets = {
            "complaint": forms.HiddenInput(),
            "assistant_engineer": forms.Select(
                attrs={"onchange": "this.form.submit();"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super(AssignAssistantEngineerForm, self).__init__(*args, **kwargs)
        # Filter users based on roles 'admin', 'investigator', 'engineer'
        self.fields["engineer"].queryset = User.objects.filter(role__in=["assistant"])


class AssignEngineerForm(forms.ModelForm):
    class Meta:
        model = AssignEngineer
        fields = [
            "engineer",
        ]
        widgets = {
            "complaint": forms.HiddenInput(),
            "engineer": forms.Select(attrs={"onchange": "this.form.submit();"}),
        }

    def __init__(self, *args, **kwargs):
        super(AssignEngineerForm, self).__init__(*args, **kwargs)
        # Filter users based on roles 'admin', 'investigator', 'engineer'
        self.fields["engineer"].queryset = User.objects.filter(role__in=["engineer"])


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
            "date": forms.DateInput(attrs={"type": "date"}),
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
