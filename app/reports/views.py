from complaints.models import Complaint
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, ListView

from .forms import EngineerReportDocumentForm, TechnicalReportDocumentForm
from .models import EngineerReportDocument, TechnicalReportDocument


@login_required
def add_technical_report_document(request, slug):
    # Get the specific complaint
    complaint = get_object_or_404(Complaint, slug=slug)

    if request.method == "POST":
        form = TechnicalReportDocumentForm(request.POST, request.FILES)
        files = request.FILES.getlist("documents")  # Get the list of uploaded files
        if form.is_valid():
            comment = form.cleaned_data["comment"]
            for file in files:
                # Create a new ComplaintPhoto for each file
                document_instance = TechnicalReportDocument(
                    complaint=complaint,
                    comment=comment,
                    document=file,  # Save each file individually
                )
                document_instance.save()
            # Redirect to the complaint detail page after saving all photos
            return redirect(reverse_lazy("detail", kwargs={"slug": slug}))
    else:
        form = TechnicalReportDocumentForm()

    context = {
        "form": form,
        "complaint": complaint,
    }

    return render(request, "report/report_document_form.html", context)


@login_required
def add_engineer_report_document(request, slug):
    # Get the specific complaint
    complaint = get_object_or_404(Complaint, slug=slug)

    if request.method == "POST":
        form = EngineerReportDocumentForm(request.POST, request.FILES)
        files = request.FILES.getlist("documents")  # Get the list of uploaded files
        if form.is_valid():
            comment = form.cleaned_data["comment"]
            for file in files:
                # Create a new ComplaintPhoto for each file
                document_instance = TechnicalReportDocument(
                    complaint=complaint,
                    comment=comment,
                    document=file,  # Save each file individually
                )
                document_instance.save()
            # Redirect to the complaint detail page after saving all photos
            return redirect(reverse_lazy("detail", kwargs={"slug": slug}))
    else:
        form = EngineerReportDocumentForm()

    context = {
        "form": form,
        "complaint": complaint,
    }

    return render(request, "report/report_document_form.html", context)
