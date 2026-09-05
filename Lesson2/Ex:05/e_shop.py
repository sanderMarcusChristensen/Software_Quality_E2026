def calculate_discount_for_eshop(amount):

    if not isinstance(amount, (int, float)):
        raise ValueError("Amount must be a number")

    if amount <= 0:
        raise ValueError("Amount must be greater than 0")

    if amount < 0.1:
        raise ValueError("Amount must be at least 0.1 kr")

    if amount <= 300:
        return 0.0
    elif amount <= 800:
        return 0.05
    else:
        return 0.10