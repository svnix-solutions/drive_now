# Copyright (c) 2025, Drive Now Team and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import now_datetime, add_to_date
import random
import string


class Ride(Document):
    def validate(self):
        self.validate_scheduled_time()
        self.calculate_total_amount()
        self.validate_driver_assignment()
        
    def validate_scheduled_time(self):
        if self.booking_type == "Scheduled" and self.scheduled_time:
            if self.scheduled_time < now_datetime():
                frappe.throw("Scheduled time cannot be in the past")
                
    def calculate_total_amount(self):
        if not self.total_amount:
            base = self.base_price or 0
            distance = self.distance_price or 0
            usage = self.usage_price or 0
            peak_rate = self.peak_hour_rate or 1.0
            
            self.total_amount = (base + distance + usage) * peak_rate
            
    def validate_driver_assignment(self):
        if self.status in ["In Progress", "Completed"] and not self.supplier:
            frappe.throw("Driver must be assigned before starting the ride")
            
    def before_insert(self):
        if not self.customer_otp:
            self.generate_otp()
            
    def generate_otp(self):
        self.customer_otp = ''.join(random.choices(string.digits, k=4))
        
    def on_update(self):
        if self.has_value_changed("status"):
            self.handle_status_change()
            
    def handle_status_change(self):
        if self.status == "Confirmed":
            self.send_confirmation_notification()
        elif self.status == "In Progress":
            self.send_ride_started_notification()
        elif self.status == "Completed":
            self.send_ride_completed_notification()
            
    def send_confirmation_notification(self):
        # Send notification to customer about ride confirmation
        pass
        
    def send_ride_started_notification(self):
        # Send notification to customer that ride has started
        pass
        
    def send_ride_completed_notification(self):
        # Send notification to customer that ride is completed
        pass
        
    @frappe.whitelist()
    def verify_otp(self, otp):
        if self.customer_otp == otp:
            return True
        return False
        
    @frappe.whitelist()
    def assign_driver(self, supplier):
        self.supplier = supplier
        self.save()
        return {"message": "Driver assigned successfully"}
        
    @frappe.whitelist()
    def update_status(self, status):
        allowed_transitions = {
            "Draft": ["Confirmed", "Cancelled"],
            "Confirmed": ["In Progress", "Cancelled"],
            "In Progress": ["Completed"],
            "Completed": [],
            "Cancelled": []
        }
        
        current_status = self.status
        if status in allowed_transitions.get(current_status, []):
            self.status = status
            self.save()
            return {"message": f"Status updated to {status}"}
        else:
            frappe.throw(f"Cannot change status from {current_status} to {status}")