class Weight:
    """Convert between kilograms (Metric) and pounds (Imperial)."""

    def __init__(self, measure, system):
        if system not in ("Metric", "Imperial"):
            raise ValueError("System must be 'Metric' or 'Imperial'.")
        if isinstance(measure, bool) or not isinstance(measure, (int, float)):
            raise ValueError("Measure must be a number.")
        if measure <= 0:
            raise ValueError("Measure must be greater than zero.")
        if round(measure, 2) != measure:
            raise ValueError("Measure can have at most two decimal places.")

        self.measure = measure
        self.system = system

    def convert(self):
        if self.system == "Metric":
            # Kilograms to pounds: 1 pound = 0.45359237 kilograms.
            result = self.measure / 0.45359237
        else:
            # Pounds to kilograms.
            result = self.measure * 0.45359237

        return round(result, 2)
