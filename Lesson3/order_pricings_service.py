

class OrderPricingService:

    def __init__(self, discount_service, shipping_service):
        self.discount_service = discount_service
        self.shipping_service = shipping_service

    def calculate_total(self, country_code, subtotal):
        discount = self.discount_service.get_discount(subtotal)
        shipping = self.shipping_service.get_shipping_costs(country_code, subtotal)
        return subtotal - discount + shipping