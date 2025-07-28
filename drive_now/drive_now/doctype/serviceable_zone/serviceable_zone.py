# Copyright (c) 2025, Drive Now Team and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import math


class ServiceableZone(Document):
    def validate(self):
        self.validate_zone_type()
        self.calculate_coverage_area()
        self.validate_boundaries()
        
    def validate_zone_type(self):
        if self.zone_type == "Circular":
            if not self.center_latitude or not self.center_longitude or not self.radius:
                frappe.throw("Center coordinates and radius are required for circular zones")
        elif self.zone_type == "Polygon":
            if not self.polygon_points or len(self.polygon_points) < 3:
                frappe.throw("At least 3 polygon points are required for polygon zones")
                
    def calculate_coverage_area(self):
        if self.zone_type == "Circular" and self.radius:
            # Area = π * r²
            self.coverage_area = math.pi * (self.radius ** 2)
        elif self.zone_type == "Polygon" and self.polygon_points:
            # Calculate polygon area using shoelace formula
            self.coverage_area = self.calculate_polygon_area()
            
    def calculate_polygon_area(self):
        """Calculate area of polygon using shoelace formula"""
        if not self.polygon_points or len(self.polygon_points) < 3:
            return 0
            
        n = len(self.polygon_points)
        area = 0.0
        
        for i in range(n):
            j = (i + 1) % n
            area += self.polygon_points[i].latitude * self.polygon_points[j].longitude
            area -= self.polygon_points[j].latitude * self.polygon_points[i].longitude
            
        # Convert to square kilometers (approximate)
        area = abs(area) / 2.0 * 111.32 * 111.32  # 1 degree ≈ 111.32 km
        return area
        
    def validate_boundaries(self):
        if self.zone_type == "Polygon":
            # Ensure polygon is closed
            if self.polygon_points and len(self.polygon_points) >= 3:
                first_point = self.polygon_points[0]
                last_point = self.polygon_points[-1]
                
                # Check if polygon is closed
                if (first_point.latitude != last_point.latitude or 
                    first_point.longitude != last_point.longitude):
                    # Auto-close the polygon
                    self.append("polygon_points", {
                        "latitude": first_point.latitude,
                        "longitude": first_point.longitude
                    })
                    
    @frappe.whitelist()
    def check_point_in_zone(self, latitude, longitude):
        """Check if a point is within this zone"""
        latitude = float(latitude)
        longitude = float(longitude)
        
        if self.zone_type == "Circular":
            return self.point_in_circle(latitude, longitude)
        elif self.zone_type == "Polygon":
            return self.point_in_polygon(latitude, longitude)
        return False
        
    def point_in_circle(self, lat, lng):
        """Check if point is within circular zone"""
        if not self.center_latitude or not self.center_longitude or not self.radius:
            return False
            
        # Calculate distance using Haversine formula
        R = 6371  # Earth's radius in km
        lat1_rad = math.radians(self.center_latitude)
        lat2_rad = math.radians(lat)
        delta_lat = math.radians(lat - self.center_latitude)
        delta_lng = math.radians(lng - self.center_longitude)
        
        a = (math.sin(delta_lat / 2) ** 2 + 
             math.cos(lat1_rad) * math.cos(lat2_rad) * 
             math.sin(delta_lng / 2) ** 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        distance = R * c
        
        return distance <= self.radius
        
    def point_in_polygon(self, lat, lng):
        """Check if point is within polygon zone using ray casting algorithm"""
        if not self.polygon_points or len(self.polygon_points) < 3:
            return False
            
        n = len(self.polygon_points)
        inside = False
        
        p1_lat = self.polygon_points[0].latitude
        p1_lng = self.polygon_points[0].longitude
        
        for i in range(1, n + 1):
            p2_lat = self.polygon_points[i % n].latitude
            p2_lng = self.polygon_points[i % n].longitude
            
            if lng > min(p1_lng, p2_lng):
                if lng <= max(p1_lng, p2_lng):
                    if lat <= max(p1_lat, p2_lat):
                        if p1_lng != p2_lng:
                            xinters = (lng - p1_lng) * (p2_lat - p1_lat) / (p2_lng - p1_lng) + p1_lat
                        if p1_lat == p2_lat or lat <= xinters:
                            inside = not inside
                            
            p1_lat = p2_lat
            p1_lng = p2_lng
            
        return inside
        
    @frappe.whitelist()
    def get_active_drivers(self):
        """Get list of active drivers in this zone"""
        active_drivers = []
        for driver in self.assigned_drivers:
            if driver.assignment_status == "Active":
                active_drivers.append({
                    "driver": driver.driver,
                    "driver_name": driver.driver_name,
                    "assignment_date": driver.assignment_date
                })
        return active_drivers