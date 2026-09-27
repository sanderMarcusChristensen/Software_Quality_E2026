# Testplan: Length, Weight og Temperature

Vi planlægger med **black-box**, **Equivalence Partitioning** og **BVA**.
Derefter bruger vi pytest, parametrisering og AAA til unit tests.

- **Partitions:** Grupper af input med samme forventede behandling.
- **BVA:** Værdier omkring en grænse.
- **Positive tests:** Gyldigt input skal give den korrekte konvertering.
- **Negative tests:** Ugyldigt input skal give en fejl.

## Length og Weight: regler og partitions

Length konverterer centimeter/inches. Weight konverterer kilogram/pounds.
Begge accepterer `"Metric"` og `"Imperial"`.

Vi har valgt en projektregel om, at målet skal være positivt og have højst
to decimaler. Positivkravet stod ikke udtrykkeligt i den oprindelige opgave.
Der er ingen angivet øvre grænse.

| Inputgruppe | Eksempel | Forventning |
|---|---|---|
| Positivt heltal | `1` | Gyldigt |
| Positivt tal med én decimal | `50.5` | Gyldigt |
| Positivt tal med to decimaler | `1000.25` | Gyldigt |
| Nul | `0` | Fejl |
| Negativt tal | `-1` | Fejl |
| Mere end to decimaler | `1.234` | Fejl |
| Ikke-numerisk input | `"abc"` | Fejl |
| Ukendt, tomt eller ikke-tekstligt system | `"Unknown"`, `""`, `123` | Fejl |

### BVA: nedre grænse for begge klasser

| Under grænsen | På grænsen | Over grænsen |
|---|---|---|
| `0.00`: ugyldigt | `0.01`: gyldigt | `0.02`: gyldigt |

## Testcases: Length

Hver case er `(measure, system)`.

### Positive cases

```python
(0.01, "Metric"), (0.02, "Metric"), (1, "Metric"),
(50.5, "Metric"), (1000.25, "Metric"),
(0.01, "Imperial"), (1, "Imperial"), (2.54, "Imperial")
```

### Negative cases

```python
(0, "Metric"), (-0.01, "Metric"), (-1, "Imperial"),
(1.234, "Metric"), ("abc", "Metric"),
(1, "Unknown"), (1, ""), (1, 123)
```

## Testcases: Weight

Hver case er `(measure, system)`.

### Positive cases

```python
(0.01, "Metric"), (0.02, "Metric"), (1, "Metric"),
(50.5, "Metric"), (1000.25, "Metric"),
(0.01, "Imperial"), (1, "Imperial"), (2.5, "Imperial")
```

### Negative cases

```python
(0, "Metric"), (-0.01, "Metric"), (-1, "Imperial"),
(1.234, "Metric"), ("abc", "Metric"),
(1, "Unknown"), (1, ""), (1, 123)
```

## Temperature: regler og partitions

Start- og destinationsskala kan være `"C"`, `"F"` eller `"K"`.
Vi tester alle seks konverteringer: C → F, C → K, F → C, F → K, K → C og K → F.

| Inputgruppe | Eksempel | Forventning |
|---|---|---|
| Negativt heltal | `-10` | Gyldigt |
| Nul | `0` | Gyldigt |
| Positivt heltal | `25` | Gyldigt |
| Én decimal | `25.5` | Gyldigt |
| To decimaler | `25.55` | Gyldigt |
| Mere end to decimaler | `25.555` | Fejl |
| Ikke-numerisk input | `"abc"` | Fejl |
| Ukendt skala | `"X"` | Fejl |
| Tom skala | `""` | Fejl |
| Ikke-tekstlig skala | `123` | Fejl |

### BVA: decimalpræcision

| Én decimal | To decimaler | Tre decimaler |
|---|---|---|
| `25.5`: gyldigt | `25.55`: gyldigt | `25.555`: ugyldigt |

Der er ingen numerisk nedre eller øvre temperaturgrænse i opgaveteksten.
Konvertering til samme skala, fx C → C, er ikke fastlagt i planen og er
udeladt fra disse testcases.

## Testcases: Temperature

Hver case er `(measure, starting_scale, destination_scale)`.

### Positive cases

```python
(-10, "C", "F"), (25.55, "C", "K"),
(32, "F", "C"), (25.5, "F", "K"),
(273.15, "K", "C"), (0, "K", "F")
```

### Negative cases

```python
(25.555, "C", "F"), ("abc", "C", "F"),
(25, "X", "F"), (25, "", "F"), (25, 123, "F"),
(25, "C", "X"), (25, "C", ""), (25, "C", 123)
```
