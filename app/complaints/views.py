from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic import CreateView, DetailView, ListView
from django.views.generic.edit import FormMixin

from .forms import ComplaintForm, ComplaintInvestigatorForm
from .models import Complaint, ComplaintInvestigator


class ComplaintListView(ListView):
    model = Complaint
    paginate_by = 10


def complaint_detail(request, slug):
    # Get the specific complaint
    complaint = get_object_or_404(Complaint, slug=slug)
    complaint_investigator = ComplaintInvestigator.objects.filter(
        complaint=complaint
    ).last()

    if request.method == "POST":
        # Process form submission
        form = ComplaintInvestigatorForm(request.POST)
        if form.is_valid():
            # Assign the current complaint and created_by to the form
            investigator = form.save(commit=False)
            investigator.complaint = complaint
            investigator.created_by = request.user  # Assuming the user is logged in
            investigator.save()

            # Redirect to the current complaint's detail page after successful submission
            return redirect(reverse("detail", kwargs={"slug": slug}))
    else:
        # Display the form with the current complaint pre-filled
        form = ComplaintInvestigatorForm(initial={"complaint": complaint})

    context = {
        "object": complaint,
        "ci_form": form,
        "complaint_investigator": complaint_investigator,
    }

    return render(request, "complaints/complaint_detail.html", context)


class ComplaintCreateView(CreateView):
    model = Complaint
    form_class = ComplaintForm


class ComplaintInvestigatorCreateView(CreateView):
    model = ComplaintInvestigator
    fields = "__all__"
    # success_url = "/complaints/success"
