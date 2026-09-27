# Currency: partitions og BVA

Dette dokument samler vores testdata, før vi skriver unit tests.
Den samlede fremgangsmåde står i [testplanen](currency_test_plan.md).

- **Equivalence Partitioning:** Del input i grupper, som forventes behandlet ens.
- **Boundary Value Analysis (BVA):** Test værdier omkring en defineret grænse.

Vi undersøger tre inputs: **basisvaluta**, **beløb** og **destinationsvaluta**.

```python
converter = Currency("DKK")       # Basisvaluta
converter.convert(100, "USD")     # Beløb og destinationsvaluta
```

## 1. Regler brugt i testene

Vi bruger forslagene fra planen som grundlag for disse testcases:

| Input | Forventning |
|---|---|
| Beløbet er 0 | Gyldigt, resultatet bliver 0 |
| Negativt beløb | ValueError |
| Mere end to decimaler | ValueError; input må ikke bare afrundes |
| Samme valuta | Gyldigt, kurs 1 giver samme beløb |
| Ugyldigt lokalt input | ValueError før et API-kald |

Det er projektets valgte regler. Testene undersøger dem, også hvis den
nuværende kode endnu ikke håndhæver dem.

## 2. Partitions: valutakoder

Tabellen bruges for både basisvaluta og destinationsvaluta.
Hold det andet valutainput og beløbet gyldigt, når ét input undersøges.

| Gruppe | Eksempler | Forventning |
|---|---|---|
| Understøttet kode med tre store bogstaver | `"DKK"`, `"USD"`, `"EUR"` | Gyldigt |
| Understøttet kode med små bogstaver | `"dkk"` | Omdannes til `"DKK"`, som klassen allerede understøtter |
| Ikke-tom kode med færre end tre tegn | `"DK"` | Fejl |
| Kode med flere end tre tegn | `"DKKK"` | Fejl |
| Tom kode | `""` | Fejl |
| Tre tegn med et tal | `"D1K"` | Fejl |
| Tre tegn med et mellemrum | `"D K"` | Fejl |
| Tre bogstaver, men valutaen understøttes ikke | En kode, som vores testklient melder som ukendt | Fejl |
| Manglende værdi | `None` | Fejl |
| Forkert datatype | `123` | Fejl |

**Korrekt format er ikke det samme som en understøttet valuta.** Tre
bogstaver kan bestå formatkontrollen, selv om tjenesten ikke kender koden.
For ukendt basisvaluta simulerer vi en klientfejl. For en ukendt destination
kan vi lade API-svaret mangle den ønskede valuta.

## 3. Partitions: beløb

### Positive beløb med højst to decimaler

| Gruppe | Eksempel | Forventning |
|---|---|---|
| Positivt heltal | `100` | Gyldigt |
| Positivt tal med én decimal | `10.5` | Gyldigt |
| Positivt tal med to decimaler | `10.25` | Gyldigt |

### Nul, negative beløb og decimalpræcision

| Gruppe | Eksempel | Forventning |
|---|---|---|
| Nul | `0` | Gyldigt |
| Negativt beløb med højst to decimaler | `-1` | ValueError |
| Positivt beløb med mere end to decimaler | `10.251` | ValueError |

### Negative testkandidater

Beløbet skal være et endeligt tal. Disse inputs forventes afvist med ValueError:

| Gruppe | Eksempel | Forventning |
|---|---|---|
| Tekst | `"abc"` | Fejl |
| Manglende værdi | `None` | Fejl |
| Bool-værdi | `True` | Fejl |
| Positiv uendelighed | `float("inf")` | Fejl |
| Negativ uendelighed | `float("-inf")` | Fejl |
| Ikke et tal, NaN | `float("nan")` | Fejl |

## 4. BVA: valutakodens længde

Kravet er præcis tre tegn, som skal være bogstaver.

| Under grænsen: 2 tegn | På grænsen: 3 tegn | Over grænsen: 4 tegn |
|---|---|---|
| `"DK"`: ugyldigt | `"DKK"`: gyldigt | `"DKKK"`: ugyldigt |

Disse tre cases køres både for basisvaluta og destinationsvaluta.
Forkerte tegn, fx `"D1K"`, undersøges særskilt gennem partitions.

## 5. BVA: beløbets nedre grænse

Vi tillader 0 og afviser negative beløb i disse tests.
Med højst to decimaler bruger vi skridt på 0.01:

| Under grænsen | På grænsen | Over grænsen |
|---|---|---|
| `-0.01`: ugyldigt | `0.00`: gyldigt | `0.01`: gyldigt |

Der er **ingen angivet maksimumværdi** i opgaven. Derfor laver vi ikke en
opdigtet øvre BVA. Meget store værdier og overflow kræver en særskilt regel.

## 6. BVA: antal decimaler

Vi forventer, at mere end to decimaler bliver afvist:

| Én decimal | To decimaler | Tre decimaler |
|---|---|---|
| `10.5`: gyldigt | `10.25`: gyldigt | `10.251`: ugyldigt |

Her undersøger vi grænsen for **præcision**, ikke for beløbets størrelse.
Numeriske værdier som `1.230` og `1.23` er ens i Python. Vi kan ikke bruge
ekstra nuller som bevis for, at et float-input har for mange decimaler.

## 7. API-svar som testscenarier

API-svaret er også input til vores beregning. Vi styrer det med en stub/mock
i unit tests. Det er scenarier for afhængigheden, ikke flere beløbsgrænser.

| Scenarie | Eksempel | Forventning |
|---|---|---|
| Destinationen findes | USD har kurs 0.15 | Brug USD-kursen |
| Flere valutaer findes | USD og EUR har forskellige kurser | Vælg den ønskede valuta |
| Destinationen mangler | Vi ønsker USD, men kun EUR findes | Fejl |
| Tomt resultat | `{"data": {}}` | Fejl |

De præcise beregninger får faste forventede værdier, fx **100 × 0.15 = 15.00**.
Vi tester også afrunding, fx **10 × 0.13456 → 1.35**.
Disse kurser er testdata, ikke aktuelle valutakurser.

## 8. Samlet positiv testliste

Hver case er `(amount, base_currency, destination_currency, stub_rate, expected)`.
Kurserne er opdigtede og kommer fra en mock, ikke fra internettet.

```python
valid_cases = [
    (100, "DKK", "USD", 0.15, 15.00),
    (10.5, "DKK", "USD", 2, 21.00),
    (10.25, "DKK", "USD", 2, 20.50),
    (10, "DKK", "USD", 0.13456, 1.35),
    (0.01, "DKK", "USD", 0.15, 0.00),
    (0, "DKK", "USD", 0.15, 0.00),
    (25, "DKK", "DKK", 1, 25.00),
    (100, "dkk", "usd", 0.15, 15.00),
    (100, "EUR", "USD", 1.1, 110.00),
    (100, "USD", "EUR", 0.9, 90.00),
]
```

Hvert svar har også en anden valuta med en anden kurs. Det kontrollerer,
at convert() vælger destinationsvalutaen og ikke blot den første kurs.
Mocken kontrollerer også, at latest() kaldes én gang med korrekt basisvaluta.

## 9. Samlet negativ testliste

### Ugyldige valutakoder

```python
invalid_codes = ["DK", "DKKK", "", "D1K", "D K", None, 123]
```

Alle syv værdier testes både som basisvaluta og som destination. Det giver
14 tests. Det øvrige input er gyldigt. Forventning: ValueError uden API-kald.

### Ugyldige beløb

```python
invalid_amounts = [
    -1, -0.01, 10.251, "abc", None, True,
    float("inf"), float("-inf"), float("nan"),
]
```

Brug DKK til USD. Forventning: ValueError uden API-kald.

### Manglende data og opsætning

| Case | Fast svar eller opsætning | Forventning |
|---|---|---|
| USD mangler | Kun EUR findes i data | ValueError |
| Ingen valutaer | data er tomt | ValueError |
| Ukendt basisvaluta ZZZ | Klienten rejser ApiError | Fejlen sendes videre |
| API-nøglen mangler | Miljøvariablen fjernes, .env-indlæsning er erstattet | ValueError før API-kald |

ZZZ er kun valgt som ukendt i testklienten; det kræver intet live opslag.

## 10. Testfiler og kørsel

- [Unit tests med mock](currency_unit_tests/test_currency_with_mock.py): 37 cases med AAA og parametrisering.
- [Eksisterende forbindelsestest](test_api_connection.py): bevares som separat test mod det rigtige API.

Kør kun de nye unit tests fra projektets rodmappe:

```bash
.venv/bin/python -m pytest -q Lesson5/Ex:02/test/currency_api_tests/currency_unit_tests
```

De bruger en fake nøgle, læser ikke .env og blokerer rigtige HTTP-kald.
Timeout, øvrige API-fejl og currencies()-metoden er fortsat mulige senere udvidelser.
