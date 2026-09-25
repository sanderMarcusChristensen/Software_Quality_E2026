class Temperature:
    """Convert temperatures using the scale names 'C', 'F', and 'K'."""

    def __init__(self, measure, scale):
        if scale not in ("C", "F", "K"):
            raise ValueError("Scale must be 'C', 'F', or 'K'.")
        if isinstance(measure, bool) or not isinstance(measure, (int, float)):
            raise ValueError("Measure must be a number.")
        if round(measure, 2) != measure:
            raise ValueError("Measure can have at most two decimal places.")

        self.measure = measure
        self.scale = scale

    def convert(self, destination_scale):
        if destination_scale not in ("C", "F", "K"):
            raise ValueError("Destination scale must be 'C', 'F', or 'K'.")

        # No conversion is needed when both scales are the same.
        if self.scale == destination_scale:
            return round(self.measure, 2)

        # Each pair of scales points to the method that converts between them.
        conversions = {
            ("C", "F"): self.celsius_to_fahrenheit,
            ("C", "K"): self.celsius_to_kelvin,
            ("F", "C"): self.fahrenheit_to_celsius,
            ("F", "K"): self.fahrenheit_to_kelvin,
            ("K", "C"): self.kelvin_to_celsius,
            ("K", "F"): self.kelvin_to_fahrenheit,
        }

        conversion_method = conversions[(self.scale, destination_scale)]
        result = conversion_method()

        return round(result, 2)

    def celsius_to_fahrenheit(self):
        return self.measure * 9 / 5 + 32

    def celsius_to_kelvin(self):
        return self.measure + 273.15

    def fahrenheit_to_celsius(self):
        return (self.measure - 32) * 5 / 9

    def fahrenheit_to_kelvin(self):
        return (self.measure - 32) * 5 / 9 + 273.15

    def kelvin_to_celsius(self):
        return self.measure - 273.15

    def kelvin_to_fahrenheit(self):
        return (self.measure - 273.15) * 9 / 5 + 32
