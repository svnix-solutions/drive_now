import frappe
from frappe import _

@frappe.whitelist()
def get_dashboard_data():
    """Get dashboard data for customer"""
    customer = frappe.session.user
    
    # Get recent rides
    recent_rides = frappe.get_all("Ride", 
        filters={"customer_email": customer},
        fields=["name", "pickup_address", "drop_off_address", "status", "total_amount", "creation"],
        order_by="creation desc",
        limit=3
    )
    
    # Get ride statistics
    total_rides = frappe.db.count("Ride", {"customer_email": customer})
    
    return {
        "recent_rides": recent_rides,
        "total_rides": total_rides,
        "active_ride": None  # TODO: Get active ride if any
    }


@frappe.whitelist()
def get_ride_history(status=None, from_date=None, to_date=None, limit=20, start=0):
    """Get customer's ride history"""
    customer = frappe.session.user
    
    filters = {"customer_email": customer}
    if status:
        filters["status"] = status
    if from_date:
        filters["creation"] = [">=", from_date]
    if to_date:
        if "creation" in filters:
            filters["creation"] = ["between", [from_date, to_date]]
        else:
            filters["creation"] = ["<=", to_date]
    
    rides = frappe.get_all("Ride",
        filters=filters,
        fields=["*"],
        order_by="creation desc",
        limit=limit,
        start=start
    )
    
    return rides


@frappe.whitelist()
def get_profile():
    """Get customer profile"""
    user = frappe.get_doc("User", frappe.session.user)
    
    # Get ride statistics
    total_rides = frappe.db.count("Ride", {"customer_email": frappe.session.user})
    total_spent = frappe.db.sql("""
        SELECT SUM(total_amount) 
        FROM `tabRide` 
        WHERE customer_email = %s AND status = 'Completed'
    """, frappe.session.user)[0][0] or 0
    
    return {
        "firstName": user.first_name,
        "lastName": user.last_name,
        "email": user.email,
        "phone": user.mobile_no,
        "address": "",
        "stats": {
            "totalRides": total_rides,
            "totalSpent": total_spent,
            "avgRating": 4.5,  # TODO: Calculate from actual ratings
            "savedMoney": 50   # TODO: Calculate CO2 savings
        }
    }


@frappe.whitelist()
def search_places(query):
    """Search for places/locations"""
    # This is a mock implementation
    # In production, you'd integrate with Google Places API or similar
    mock_places = [
        {
            "id": 1,
            "name": f"{query} Location 1",
            "address": f"123 {query} Street, City",
            "latitude": 12.9716,
            "longitude": 77.5946
        },
        {
            "id": 2,
            "name": f"{query} Location 2", 
            "address": f"456 {query} Avenue, City",
            "latitude": 12.9726,
            "longitude": 77.5956
        }
    ]
    
    return mock_places


@frappe.whitelist()
def get_fare_estimate(pickup_latitude, pickup_longitude, drop_latitude, drop_longitude, vehicle_type):
    """Calculate fare estimate"""
    # Mock fare calculation
    # In production, you'd calculate based on distance, time, demand, etc.
    
    import math
    
    # Calculate approximate distance using Haversine formula
    lat1, lon1 = float(pickup_latitude), float(pickup_longitude)
    lat2, lon2 = float(drop_latitude), float(drop_longitude)
    
    R = 6371  # Earth's radius in kilometers
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    distance = R * c
    
    # Base fare calculation
    base_fare = 50
    per_km_rate = {"standard": 12, "premium": 18, "luxury": 25}.get(vehicle_type, 12)
    
    total_fare = base_fare + (distance * per_km_rate)
    duration = max(distance * 3, 10)  # Rough estimate: 3 minutes per km
    
    return {
        "distance": round(distance, 1),
        "duration": round(duration, 0),
        "fare": round(total_fare, 0)
    }


@frappe.whitelist()
def book_ride(pickup_address, pickup_latitude, pickup_longitude, 
              drop_off_address, drop_off_latitude, drop_off_longitude, 
              vehicle_type, scheduled_time=None):
    """Book a new ride"""
    
    # Calculate fare
    fare_data = get_fare_estimate(pickup_latitude, pickup_longitude, 
                                  drop_off_latitude, drop_off_longitude, vehicle_type)
    
    # Create ride document
    ride = frappe.get_doc({
        "doctype": "Ride",
        "customer_email": frappe.session.user,
        "pickup_address": pickup_address,
        "pickup_latitude": pickup_latitude,
        "pickup_longitude": pickup_longitude,
        "drop_off_address": drop_off_address,
        "drop_off_latitude": drop_off_latitude,
        "drop_off_longitude": drop_off_longitude,
        "vehicle_type": vehicle_type,
        "total_amount": fare_data["fare"],
        "distance": fare_data["distance"],
        "duration": fare_data["duration"],
        "status": "Draft",
        "scheduled_time": scheduled_time
    })
    
    ride.insert()
    frappe.db.commit()
    
    return {"ride_id": ride.name, "message": "Ride booked successfully"}


@frappe.whitelist()
def get_ride_tracking(ride_id):
    """Get real-time ride tracking data"""
    ride = frappe.get_doc("Ride", ride_id)
    
    # Check if user has permission to view this ride
    if ride.customer_email != frappe.session.user:
        frappe.throw(_("You don't have permission to view this ride"), frappe.PermissionError)
    
    # Mock live updates
    updates = [
        {"id": 1, "message": "Ride confirmed", "timestamp": ride.creation},
        {"id": 2, "message": "Driver assigned", "timestamp": ride.modified},
    ]
    
    ride_data = ride.as_dict()
    ride_data["updates"] = updates
    
    return ride_data


@frappe.whitelist()
def cancel_ride(ride_id, reason):
    """Cancel a ride"""
    ride = frappe.get_doc("Ride", ride_id)
    
    # Check permissions
    if ride.customer_email != frappe.session.user:
        frappe.throw(_("You don't have permission to cancel this ride"), frappe.PermissionError)
    
    if ride.status not in ["Draft", "Confirmed"]:
        frappe.throw(_("Cannot cancel ride with status: {0}").format(ride.status))
    
    ride.status = "Cancelled"
    ride.cancellation_reason = reason
    ride.save()
    frappe.db.commit()
    
    return {"message": "Ride cancelled successfully"}


@frappe.whitelist()
def rate_ride(ride_id, rating, feedback=None):
    """Rate and provide feedback for a completed ride"""
    ride = frappe.get_doc("Ride", ride_id)
    
    # Check permissions
    if ride.customer_email != frappe.session.user:
        frappe.throw(_("You don't have permission to rate this ride"), frappe.PermissionError)
    
    if ride.status != "Completed":
        frappe.throw(_("Can only rate completed rides"))
    
    ride.customer_rating = rating
    ride.customer_feedback = feedback
    ride.save()
    frappe.db.commit()
    
    return {"message": "Rating submitted successfully"}


@frappe.whitelist()
def update_profile(firstName, lastName, email, phone, address):
    """Update customer profile"""
    user = frappe.get_doc("User", frappe.session.user)
    
    user.first_name = firstName
    user.last_name = lastName
    user.mobile_no = phone
    # Note: Email changes need admin approval in Frappe
    
    user.save(ignore_permissions=True)
    frappe.db.commit()
    
    return {"message": "Profile updated successfully"}


@frappe.whitelist()
def get_payment_methods():
    """Get customer's payment methods"""
    # Mock data - in production you'd integrate with payment gateway
    return [
        {
            "id": 1,
            "type": "card",
            "details": "**** **** **** 1234",
            "isDefault": True
        }
    ]