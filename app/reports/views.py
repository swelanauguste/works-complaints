from complaints.models import Complaint
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, ListView

from .forms import (
    ComplaintReviewForm,
    EngineerReportDocumentForm,
    TechnicalReportDocumentForm,
)
from .models import ComplaintReview, EngineerReportDocument, TechnicalReportDocument
from .utils import send_approval_email, send_non_approval_email


@login_required
def complaint_review(request, slug):
    # Get the specific complaint
    complaint = get_object_or_404(Complaint, slug=slug)

    if request.method == "POST":
        form = ComplaintReviewForm(request.POST)
        if form.is_valid():
            complaint_review = form.save(commit=False)
            complaint_review.complaint = complaint
            complaint_review.created_by = request.user
            complaint_review.save()
            cc_email = form.cleaned_data['cc']
            print(cc_email, "email")
            review = form.cleaned_data["review"]
            if review:
                send_approval_email.after_response(complaint, cc_email)
            else:
                send_non_approval_email.after_response(complaint)
            # Redirect to the complaint detail page after saving all photos
            return redirect(reverse_lazy("detail", kwargs={"slug": slug}))
    else:
        form = ComplaintReviewForm()

    context = {
        "form": form,
        "complaint": complaint,
    }

    return render(request, "reports/complaint_review_form.html", context)


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

    return render(request, "reports/report_document_form.html", context)


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
                document_instance = EngineerReportDocument(
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

    return render(request, "reports/report_document_form.html", context)
