import frappe

def create_ride_items():
    items = [
        {
            "item_code": "HOURLY-DRIVE",
            "item_name": "Hourly Drive",
            "item_group": "Services",
            "stock_uom": "Unit",
            "is_stock_item": 0,
            "is_sales_item": 1,
            "description": "Hourly drive service"
        },
        {
            "item_code": "WEEKLY-DRIVE",
            "item_name": "Weekly Drive",
            "item_group": "Services", 
            "stock_uom": "Unit",
            "is_stock_item": 0,
            "is_sales_item": 1,
            "description": "Weekly drive service package"
        },
        {
            "item_code": "MONTHLY-DRIVE",
            "item_name": "Monthly Drive",
            "item_group": "Services",
            "stock_uom": "Unit", 
            "is_stock_item": 0,
            "is_sales_item": 1,
            "description": "Monthly drive service package"
        }
    ]
    
    for item_data in items:
        if not frappe.db.exists("Item", item_data["item_code"]):
            item = frappe.get_doc({
                "doctype": "Item",
                **item_data
            })
            item.insert()
            print(f"Created item: {item_data['item_name']}")
        else:
            print(f"Item already exists: {item_data['item_name']}")
    
    frappe.db.commit()