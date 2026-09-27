from currency import Currency


def test_api_connection():
    """Kræver internet og en gyldig API-nøgle. Bruger ét API-kald."""
    # Arrange
    converter = Currency("DKK")

    # Act
    result = converter.convert(100, "USD")

    # Assert: et positivt beløb viser, at API-svaret kunne bruges.
    assert result > 0
