# Copyright (c) 2025, Drive Now Team and contributors
# For license information, please see license.txt

from frappe.model.document import Document


class RideItem(Document):
    def validate(self):
        self.calculate_amount()
        
    def calculate_amount(self):
        if self.qty and self.rate:
            self.amount = self.qty * self.rate