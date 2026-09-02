# Calculates the discount for an order of printer cartridges.
# Rules:
# - Minimum order: 5 units. Anything below 5 is an invalid order.
# - Orders >= 100 get a 20% discount.
# - Orders < 100 (but >= 5) get no discount.
# Returns the discount rate as a decimal (0.0 or 0.2).
# Raises ValueError if the order is invalid.  


def calculate_discount(quantity):

    # Validate input check = erorr mesg if it's not an integer
    if not isinstance(quantity, int):
        raise ValueError("Quantity must be an integer")

    if quantity < 5:
        raise ValueError("Minimum order quantity is 5")

    if quantity >= 100:
        return 0.2

    return 0.0