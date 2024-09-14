from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic import CreateView, DetailView, ListView
from django.views.generic.edit import FormMixin

from .forms import ComplaintForm, ComplaintInvestigatorForm
from .models import Complaint, ComplaintInvestigator, Zone


@login_required
def complaint_list(request):
    # Get all complaints
    complaints = Complaint.objects.all()
    zones = Zone.objects.all()
    # Search functionality
    search_query = request.GET.get("search", "")
    if search_query:
        complaints = complaints.filter(
            Q(name__icontains=search_query)
            | Q(email__icontains=search_query)
            | Q(address__icontains=search_query)
            | Q(complaint__icontains=search_query)
        )

    # Filtering by Foreign Keys (Zone and Category in this case)
    zone_filter = request.GET.get("zone", None)
    if zone_filter:
        complaints = complaints.filter(zone__id=zone_filter)

    # category_filter = request.GET.get("category", None)
    # if category_filter:
    #     complaints = complaints.filter(category__id=category_filter)

    # Sorting functionality
    sort_by = request.GET.get("sort", "created_at")  # Default sorting by created_at
    order = request.GET.get("order", "asc")  # Default order is ascending
    if order == "desc":
        sort_by = f"-{sort_by}"
    complaints = complaints.order_by(sort_by)

    # Pagination (optional)
    page = request.GET.get("page", 1)
    paginator = Paginator(complaints, 25)  # Show 10 complaints per page
    complaints = paginator.get_page(page)

    context = {
        "object_list": complaints,
        "search_query": search_query,
        "zone_filter": zone_filter,
        # "category_filter": category_filter,
        "zones": zones,
        "sort_by": sort_by,
        "order": order,
    }

    return render(request, "complaints/complaint_list.html", context)


@login_required
def complaint_detail(request, slug):
    # Get the specific complaint
    complaint = get_object_or_404(Complaint, slug=slug)
    complaint_investigator = ComplaintInvestigator.objects.filter(
        complaint=complaint
    ).first()

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


class ComplaintInvestigatorCreateView(CreateView):
    model = ComplaintInvestigator
    fields = "__all__"
    # success_url = "/complaints/success"
