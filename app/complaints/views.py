from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, ListView

from .forms import (
    AcknowledgementLetterForm,
    AssignEngineerForm,
    AssignTechnicianForm,
    ChangePriorityForm,
    ChangeStatusForm,
    ComplaintForm,
    ComplaintPhotoForm,
)
from .models import (
    AcknowledgementLetter,
    AssignEngineer,
    AssignTechnician,
    ChangePriority,
    ChangeStatus,
    Complaint,
    ComplaintPhoto,
    Zone,
)
from .utils import send_engineer_assigned_email, send_technician_assigned_email


@login_required
def change_status(request, slug):
    # Get the specific complaint
    complaint = get_object_or_404(Complaint, slug=slug)

    if request.method == "POST":
        form = ChangeStatusForm(request.POST)
        if form.is_valid():
            status_change = form.save(commit=False)
            status_change.complaint = complaint
            status_change.created_by = request.user
            status_change.save()

            # Redirect back to the complaint detail page or the page you want
            return redirect(reverse_lazy("detail", kwargs={"slug": slug}))

    # No need to handle the 'GET' request or render a template,
    # since the form is being posted and handled via another page.
    return redirect(reverse_lazy("detail", kwargs={"slug": slug}))


@login_required
def change_priority(request, slug):
    # Get the specific complaint
    complaint = get_object_or_404(Complaint, slug=slug)

    if request.method == "POST":
        form = ChangePriorityForm(request.POST)
        if form.is_valid():
            priority_change = form.save(commit=False)
            priority_change.complaint = complaint
            priority_change.created_by = request.user
            priority_change.save()

            # Redirect back to the complaint detail page or the page you want
            return redirect(reverse_lazy("detail", kwargs={"slug": slug}))

    # No need to handle the 'GET' request or render a template,
    # since the form is being posted and handled via another page.
    return redirect(reverse_lazy("detail", kwargs={"slug": slug}))


@login_required
def assign_technician(request, slug):
    # Get the specific complaint
    complaint = get_object_or_404(Complaint, slug=slug)

    if request.method == "POST":
        form = AssignTechnicianForm(request.POST)
        if form.is_valid():
            assign = form.save(commit=False)
            assign.complaint = complaint
            assign.created_by = request.user  # Ensure created_by is assigned
            assign.save()
            messages.info(request, f"This complaint was assign to {assign.technician}")
            send_technician_assigned_email.after_response(
                assign.technician, assign.complaint
            )
            # form.save_m2m()
            # Redirect to the complaint detail page
            return redirect(reverse_lazy("detail", kwargs={"slug": slug}))
    return redirect(reverse_lazy("detail", kwargs={"slug": slug}))


@login_required
def assign_engineer(request, slug):
    # Get the specific complaint
    complaint = get_object_or_404(Complaint, slug=slug)

    if request.method == "POST":
        form = AssignEngineerForm(request.POST)
        if form.is_valid():
            assign = form.save(commit=False)
            assign.complaint = complaint
            assign.created_by = request.user  # Ensure created_by is assigned
            assign.save()
            messages.info(request, f"This complaint was assign to {assign.engineer}")
            send_engineer_assigned_email.after_response(
                assign.engineer, assign.complaint
            )
            # messages.info(request, f"An email was sent to {assign.engineer} at {assign.engineer.email}")
            # form.save_m2m()
            # Redirect to the complaint detail page
            return redirect(reverse_lazy("detail", kwargs={"slug": slug}))
    return redirect(reverse_lazy("detail", kwargs={"slug": slug}))


@login_required
def add_acknowledgement_letter(request, slug):
    # Get the specific complaint
    complaint = get_object_or_404(Complaint, slug=slug)

    if request.method == "POST":
        form = AcknowledgementLetterForm(request.POST, request.FILES)
        if form.is_valid():
            letter = form.save(commit=False)
            letter.complaint = complaint
            letter.created_by = request.user  # Ensure created_by is assigned
            letter.save()
            # Redirect to the complaint detail page
            return redirect(reverse_lazy("detail", kwargs={"slug": slug}))
    else:
        form = AcknowledgementLetterForm(initial={"complaint": complaint})

    context = {
        "form": form,
        "complaint": complaint,
    }

    return render(request, "complaints/acknowledgement_letter_form.html", context)


@login_required
def create_complaint_photo(request, slug):
    # Get the specific complaint
    complaint = get_object_or_404(Complaint, slug=slug)

    if request.method == "POST":
        form = ComplaintPhotoForm(request.POST, request.FILES)
        files = request.FILES.getlist("photos")  # Get the list of uploaded files
        if form.is_valid():
            comment = form.cleaned_data["comment"]
            for file in files:
                # Create a new ComplaintPhoto for each file
                photo_instance = ComplaintPhoto(
                    complaint=complaint,
                    comment=comment,
                    photo=file,  # Save each file individually
                )
                photo_instance.save()
            # Redirect to the complaint detail page after saving all photos
            return redirect(reverse_lazy("detail", kwargs={"slug": slug}))
    else:
        form = ComplaintPhotoForm()

    context = {
        "form": form,
        "complaint": complaint,
    }

    return render(request, "complaints/complaint_photo_form.html", context)


@login_required
def complaint_list(request):
    # Get all complaints
    complaints = Complaint.objects.all().order_by("-created_at")
    zones = Zone.objects.all()
    # Search functionality
    search_query = request.GET.get("search", "")
    if search_query:
        complaints = complaints.filter(
            Q(name__icontains=search_query)
            | Q(email__icontains=search_query)
            | Q(address__icontains=search_query)
            | Q(complaint__icontains=search_query)
            | Q(phone__icontains=search_query)
            | Q(ref__iexact=search_query)
        )

    # Filtering by Foreign Keys (Zone and Category in this case)
    zone_filter = request.GET.get("zone", None)
    if zone_filter:
        complaints = complaints.filter(zone__id=zone_filter)

    # category_filter = request.GET.get("category", None)
    # if category_filter:
    #     complaints = complaints.filter(category__id=category_filter)

    # # Sorting functionality
    # sort_by = request.GET.get("sort", "created_at")  # Default sorting by created_at
    # order = request.GET.get("order", "desc")  # Default order is ascending
    # if order == "desc":
    #     sort_by = f"-{sort_by}"
    # complaints = complaints.order_by('sort_by')

    # Pagination (optional)
    page = request.GET.get("page", 1)
    paginator = Paginator(complaints, 18)  # Show 10 complaints per page
    complaints = paginator.get_page(page)

    context = {
        "object_list": complaints,
        "search_query": search_query,
        "zone_filter": zone_filter,
        # "category_filter": category_filter,
        "zones": zones,
        # "sort_by": sort_by,
        # "order": order,
    }

    return render(request, "complaints/complaint_list.html", context)


@login_required
def complaint_detail(request, slug):
    # Get the specific complaint using the slug
    complaint = get_object_or_404(Complaint, slug=slug)
    # Fetch related data with safe null handling
    assigned_engineer = None
    assigned_technician = None
    status = None
    priority = None

    try:
        assigned_engineer = AssignEngineer.objects.filter(complaint=complaint).first()
        assigned_technician = AssignTechnician.objects.filter(
            complaint=complaint
        ).first()
        status = ChangeStatus.objects.filter(complaint=complaint).first()
        priority = ChangePriority.objects.filter(complaint=complaint).first()
    except Exception as e:
        pass

    # Extract the actual engineer and technician from the assignment objects
    engineer = assigned_engineer.engineer if assigned_engineer else None
    technician = assigned_technician.technician if assigned_technician else None

    # Fetch related data if necessary
    photos = complaint.photos.all()  # Assuming Complaint has a related Photo model
    letters = complaint.letters.all()

    # Initialize forms with existing data
    change_status_form = ChangeStatusForm(
        initial={"complaint": complaint, "status": status.status if status else None}
    )
    change_priority_form = ChangePriorityForm(
        initial={
            "complaint": complaint,
            "priority": priority.priority if priority else None,
        }
    )
    assign_engineer_form = AssignEngineerForm(
        initial={"complaint": complaint, "engineer": engineer}
    )
    assign_technician_form = AssignTechnicianForm(
        initial={"complaint": complaint, "technician": technician}
    )

    context = {
        "complaint": complaint,
        "photos": photos,
        "letters": letters,
        "assigned_engineer": assigned_engineer,
        "assigned_technician": assigned_technician,
        "change_status_form": change_status_form,
        "change_priority_form": change_priority_form,
        "assign_engineer_form": assign_engineer_form,
        "assign_technician_form": assign_technician_form,
    }

    return render(request, "complaints/complaint_detail.html", context)


@login_required
def complaint_create(request):
    if request.method == "POST":
        form = ComplaintForm(request.POST)
        if form.is_valid():
            # Save the complaint
            complaint = form.save()

            # Redirect to the detail page of the created complaint or some success URL
            return redirect(reverse("detail", kwargs={"slug": complaint.slug}))
    else:
        form = ComplaintForm()

    context = {"form": form}

    return render(request, "complaints/complaint_form.html", context)


class ComplaintPhotoCreateView(CreateView):
    model = ComplaintPhoto
    form_class = ComplaintPhotoForm
    # success_url = "/complaints/success"


# class ComplaintInvestigatorCreateView(CreateView):
#     model = ComplaintInvestigator
#     fields = "__all__"
#     # success_url = "/complaints/success"
