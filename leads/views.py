from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Lead
from .serializers import LeadSerializer
from .services.search import search_businesses
from .services.ai import analyze_business
from .services.pipeline import enrich_businesses

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator



class LeadViewSet(viewsets.ModelViewSet):
    queryset = Lead.objects.all().order_by('-created_at')
    serializer_class = LeadSerializer


@api_view(["GET"])
def search_businesses_view(request):
    query = request.GET.get("query")   # required
    country = request.GET.get("country")  # required

    if not query or not country:
        return Response({"error": "query and country are required"}, status=400)

    # Call pipeline with correct params
    results = enrich_businesses(query, country)

    leads = []
    for r in results:
        # Create new lead for every result (no deduplication)
        lead = Lead.objects.create(
            name=r["name"],
            category=r.get("category", "")[:100],  # Truncate to fit CharField
            address=r.get("address", ""),
            website=r.get("website", ""),
            phone=r.get("phone", ""),
            rating=r.get("rating"),
            linkedin_data=r.get("linkedin", {}),
            osm_data=r.get("osm", {}),
            source=r.get("source", "api"),
        )
        print(f"✅ Created new lead: {lead.name}")
        leads.append(lead)

    serializer = LeadSerializer(leads, many=True)
    return Response({
        "results": serializer.data,
        "total_created": len(leads),
        "message": f"Created {len(leads)} new leads"
    })


# For function-based views, use csrf_exempt directly
@csrf_exempt
@api_view(["POST"])
def analyze_lead_view(request, pk):
    try:
        lead = Lead.objects.get(pk=pk)
    except Lead.DoesNotExist:
        return Response({"error": "Lead not found"}, status=404)

    result = analyze_business(lead)

    if isinstance(result, dict) and "needs" in result:
        lead.needs = result["needs"]
    else:
        lead.needs = [str(result)]
    lead.save()

    return Response({"id": lead.id, "name": lead.name, "needs": lead.needs})



def dashboard_view(request):
    query = request.GET.get("q", "")
    country = request.GET.get("country", "")

    leads = Lead.objects.all().order_by("-created_at")

    if query:
        leads = leads.filter(name__icontains=query)
    if country:
        leads = leads.filter(address__icontains=country)

    return render(request, "leads/dashboard.html", {"leads": leads, "query": query, "country": country})