from django.db import models

class Lead(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=100, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    rating = models.FloatField(blank=True, null=True)
    source = models.CharField(max_length=100, default="api")  # rapidapi/osm/linkedin

    linkedin_data = models.JSONField(default=dict)  # Company info
    osm_data = models.JSONField(default=dict)       # Geocoding info

    needs = models.JSONField(default=list)  # AI analysis
    created_at = models.DateTimeField(auto_now_add=True)