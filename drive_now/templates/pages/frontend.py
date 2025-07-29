import frappe
import json
import os

def get_context(context):
    # Allow access for logged in users and guests (for PWA installation)
    # Authentication will be handled by the Vue.js app
    context.no_cache = 1
    context.show_sidebar = False
    
    # IMPORTANT: Render without base template for standalone PWA
    context.base_template_path = "templates/blank_base.html"
    
    # Pass CSRF token for API calls
    if frappe.session.user != "Guest":
        context.csrf_token = frappe.sessions.get_csrf_token()
    else:
        context.csrf_token = ""
    
    # Load asset manifest to get current build filenames
    app_path = frappe.get_app_path("drive_now")
    manifest_path = os.path.join(app_path, "public", "frontend", ".vite", "manifest.json")
    
    # Default assets in case manifest doesn't exist
    context.main_js = "/assets/drive_now/frontend/assets/main.js"
    context.main_css = "/assets/drive_now/frontend/assets/main.css"
    context.vendor_js = "/assets/drive_now/frontend/assets/vendor.js"
    context.vendor_css = "/assets/drive_now/frontend/assets/vendor.css"
    
    try:
        if os.path.exists(manifest_path):
            with open(manifest_path, 'r') as f:
                manifest = json.load(f)
                
                # Get the main entry point
                if "index.html" in manifest:
                    entry = manifest["index.html"]
                    if "file" in entry:
                        context.main_js = f"/assets/drive_now/frontend/{entry['file']}"
                    if "css" in entry:
                        for css in entry["css"]:
                            context.main_css = f"/assets/drive_now/frontend/{css}"
                    if "imports" in entry:
                        for imp in entry["imports"]:
                            if imp in manifest and "file" in manifest[imp]:
                                context.vendor_js = f"/assets/drive_now/frontend/{manifest[imp]['file']}"
                                if "css" in manifest[imp]:
                                    for css in manifest[imp]["css"]:
                                        context.vendor_css = f"/assets/drive_now/frontend/{css}"
    except Exception as e:
        frappe.log_error(f"Error loading asset manifest: {e}", "Frontend Assets")