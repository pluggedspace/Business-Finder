from django.contrib import admin
from django.utils.html import format_html
from .models import Lead

@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    # Display fields in list view
    list_display = [
        'name', 
        'category', 
        'phone', 
        'rating', 
        'source',
        'needs_preview',
        'created_at',
        'website_link'
    ]
    
    # Fields that can be searched
    search_fields = [
        'name', 
        'category', 
        'phone', 
        'address',
        'source'
    ]
    
    # Filters for the sidebar
    list_filter = [
        'source',
        'category',
        'rating',
        'created_at'
    ]
    
    # Fields that are read-only
    readonly_fields = [
        'created_at',
        'linkedin_data_preview',
        'osm_data_preview',
        'needs_display'
    ]
    
    # Fieldsets for the detail/edit view
    fieldsets = (
        ('Basic Information', {
            'fields': (
                'name', 
                'category', 
                'source',
                'rating',
                'created_at'
            )
        }),
        ('Contact Information', {
            'fields': (
                'phone',
                'website',
                'address'
            )
        }),
        ('Additional Data', {
            'fields': (
                'needs_display',
                'linkedin_data_preview',
                'osm_data_preview',
            ),
            'classes': ('collapse',)  # Makes this section collapsible
        }),
    )
    
    # Pagination
    list_per_page = 25
    
    # Ordering
    ordering = ['-created_at']  # Newest first
    
    # Custom methods for display
    def website_link(self, obj):
        if obj.website:
            return format_html('<a href="{}" target="_blank">{}</a>', obj.website, 'Visit Website')
        return "-"
    website_link.short_description = 'Website'
    
    def needs_preview(self, obj):
        if obj.needs and len(obj.needs) > 0:
            # Show first 2 needs as preview
            preview = ', '.join(str(need) for need in obj.needs[:2])
            if len(obj.needs) > 2:
                preview += f' ... (+{len(obj.needs) - 2} more)'
            return preview
        return "-"
    needs_preview.short_description = 'Needs Preview'
    
    def linkedin_data_preview(self, obj):
        if obj.linkedin_data:
            # Show a preview of linkedin data
            import json
            return format_html('<pre>{}</pre>', json.dumps(obj.linkedin_data, indent=2))
        return "No LinkedIn data"
    linkedin_data_preview.short_description = 'LinkedIn Data'
    
    def osm_data_preview(self, obj):
        if obj.osm_data:
            # Show a preview of OSM data
            import json
            return format_html('<pre>{}</pre>', json.dumps(obj.osm_data, indent=2))
        return "No OSM data"
    osm_data_preview.short_description = 'OSM Data'
    
    def needs_display(self, obj):
        if obj.needs:
            needs_list = ''.join([f'<li>{need}</li>' for need in obj.needs])
            return format_html(f'<ul>{needs_list}</ul>')
        return "No needs identified"
    needs_display.short_description = 'Needs'

# Optional: If you want to customize the admin site header and title
admin.site.site_header = 'Leads Management System'
admin.site.site_title = 'Leads Admin'
admin.site.index_title = 'Welcome to Leads Administration'