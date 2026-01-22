from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from leads.views import LeadViewSet, search_businesses_view, analyze_lead_view, dashboard_view

router = routers.DefaultRouter()
router.register(r'leads', LeadViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/search/', search_businesses_view),
    path("api/analyze/<int:pk>/", analyze_lead_view),
    path("dashboard/", dashboard_view, name="dashboard"),
]