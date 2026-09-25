class Length:
    """Convert between centimeters (Metric) and inches (Imperial)."""

    def __init__(self, measure, system):
        if system not in ("Metric", "Imperial"):
            raise ValueError("System must be 'Metric' or 'Imperial'.")
        if isinstance(measure, bool) or not isinstance(measure, (int, float)):
            raise ValueError("Measure must be a number.")
        if measure <= 0:
            raise ValueError("Measure must be greater than zero.")
        if round(measure, 2) != measure:
            raise ValueError("Measure can have at most two decimal places.")

        # Save the measure and its system for use in convert().
        self.measure = measure
        self.system = system

    def convert(self):
        if self.system == "Metric":
            # Centimeters to inches: 1 inch = 2.54 centimeters.
            result = self.measure / 2.54
        else:
            # Inches to centimeters.
            result = self.measure * 2.54

        return round(result, 2)
