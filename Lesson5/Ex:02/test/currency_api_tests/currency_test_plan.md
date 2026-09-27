# Testplan for Currency

Se også [Currency: partitions og BVA](currency_partitions_and_bva.md), hvor inputgrupper og grænseværdier står samlet.

## Hvad vil vi undersøge?

Vi skal teste Currency på to måder, som opgaven kræver:

1. **Unit tests med faste API-svar:** Regner vores kode rigtigt?
2. **Narrow integration tests med det rigtige API:** Virker forbindelsen og samarbejdet?

Vi bruger currencyapi.com og pakken `currencyapicom`. Den oprindelige opgave
nævner freecurrencyapi.net; vi har altså valgt en anden leverandør.
Vi gemmer ingen data i en database.

## Rækkefølgen

### 1. Aftal reglerne

Før vi forventer en fejl i en test, skal vi vide, hvilket input der er ugyldigt.

| Spørgsmål | Regel brugt i unit tests |
|---|---|
| Må beløbet være 0? | Ja, resultatet bliver 0 |
| Må beløbet være negativt? | Nej i denne øvelse |
| Må beløbet have mere end to decimaler? | Nej, afvis det |
| Må basis- og destinationsvaluta være ens? | Ja, brug kurs 1 |

Valutakoder skal have tre bogstaver. Vi vil også undersøge små bogstaver,
ukendte koder og forkerte datatyper. Et beløb skal være et almindeligt,
endeligt tal; eksempelvis tekst og uendelighed er negative testkandidater.

Testene bruger nu reglerne ovenfor. Den nuværende kode kan stadig afvige;
et fejlet testresultat skal undersøges, før vi ændrer kode eller forventninger.

### 2. Lav partitions og BVA

**Partitions:** Gruppér input og vælg eksempler fra hver gruppe.

| Input | Eksempler |
|---|---|
| Gyldige valutakoder | `"DKK"`, `"USD"`, `"EUR"` |
| Små bogstaver | `"dkk"` |
| Forkert kodelængde | `"DK"`, `"DKKK"`, `""` |
| Forkerte tegn eller datatype | `"D1K"`, `"D K"`, `None`, `123` |
| Heltal, én decimal, to decimaler | `100`, `10.5`, `10.25` |
| Nul, negativt beløb og for mange decimaler | `0`, `-1`, `10.251` |
| Ugyldige beløb som testkandidater | `"abc"`, `None`, `True`, `inf`, `-inf`, `NaN` |

**BVA:** Undersøg grænserne.

- Kodelængde: 2, 3 og 4 tegn.
- Med 0 som mindste gyldige beløb: `-0.01`, `0.00`, `0.01`.
- Decimalpræcision: eksempler med 1, 2 og 3 decimaler.
- Der er ingen angivet øvre beløbsgrænse.

Præcision er ikke det samme som tekstlængde: `1.230` og `1.23` er samme float.
Test basisvaluta og destinationsvaluta hver for sig med øvrige inputs gyldige.

### 3. Skriv positive og negative testcases

Hver testcase får input og et forventet resultat eller en forventet fejl.
Her er nogle positive eksempler med **opdigtede testkurser**:

| Beløb | Fast kurs | Forventet beløb |
|---|---|---|
| 100 | 0.15 | 15.00 |
| 10.5 | 2 | 21.00 |
| 10.25 | 2 | 20.50 |
| 10 | 0.13456 | 1.35 |
| 0.01 | 0.15 | 0.00 |

Negative cases vælges fra partitionslisten. Vi tager også et API-svar uden
destinationsvalutaen med. Det skal give en fejl, ikke en opdigtet kurs.

### 4. Skriv unit tests med stub/mock

Vi erstatter API-klienten med et lille testobjekt, som giver et fast svar:

```python
{"data": {"USD": {"code": "USD", "value": 0.15}}}
```

Så tester vi, at `convert(100, "USD")` giver `15.00`.

Vi kontrollerer:

- At den rigtige destinationskurs vælges, også når svaret har flere valutaer.
- At beløbet ganges korrekt og afrundes til to decimaler.
- At klienten bliver kaldt med den rigtige basisvaluta.
- At ugyldigt input eller et manglende resultat giver den aftalte fejl.

Unit tests bruger en fake nøgle og en erstattet `load_dotenv()`, så de ikke
læser vores private `.env` eller kontakter internettet.

**Første omgang holdes lille:** Beregning, valg af kurs, aftalte inputfejl og
manglende resultat. Timeout, forkert nøgle, kvotefejl og ødelagte API-svar
kan tilføjes senere med simulerede fejl. `currencies()` kan også få en lille
test for, at den returnerer klientens valutaoplysninger.

### 5. Kør få integrationstests mod det rigtige API

Vi har allerede én forbindelsestest: 100 DKK til USD skal give et positivt beløb.
Den viser, om nøgle, klient og API kan fungere sammen.

Vi kan supplere med ét kig på svarets struktur: `data` skal findes, og kursens
`value` skal være et positivt, endeligt tal.

Vi starter med **happy path**. Vi bruger ikke en fast forventet live-kurs,
fordi kurser ændrer sig. Den præcise regning testes med de faste svar ovenfor.

`convert()` returnerer et beløb, ikke et HTTP-response. Statuskode og headers
kræver derfor en særskilt HTTP-test, hvis vi senere får brug for den.
Vi har intet krav om 200 ms svartid, og vi tester ingen POST/DELETE-kald.

## Teknikker og begreber

| Begreb | Betydning i vores opgave |
|---|---|
| Black-box | Vælg testcases ud fra krav og forventet adfærd |
| Equivalence Partitioning | Gruppér input, som forventes behandlet ens |
| BVA | Undersøg værdier omkring en defineret grænse |
| Happy path | Gyldigt input giver det forventede resultat |
| Negative testing | Undersøg ugyldige input og fejl |
| Test double | Fælles navn for en erstatning af en afhængighed i en test |
| Stub | Leverer et fast API-svar |
| Mock | Kan også kontrollere, hvilke kald og argumenter der blev brugt |
| Unit test | Tester vores kode isoleret fra det rigtige API |
| Narrow integration test | Tester samarbejdet med én rigtig ekstern tjeneste |
| Smoke-test | En lille test, som hurtigt undersøger, om opsætningen virker |
| Parametrisering / data provider | Kør samme testfunktion med flere inputs via `pytest.mark.parametrize` |
| Fixture | Fælles forberedelse og eventuel oprydning til tests |
| monkeypatch | Erstatter funktioner eller miljøvariabler og gendanner dem efter testen |
| AAA | Arrange: forbered. Act: udfør. Assert: kontrollér |

Ét mock-objekt kan både give faste svar og kontrollere kald. Vi behøver ikke
en separat stub-klasse og mock-server.

## Praktisk opdeling

- Unit tests: `test/currency_api_tests/currency_unit_tests/test_currency_with_mock.py`.
- Eksisterende integrationstest: `test/currency_api_tests/test_api_connection.py`.
- Alle tests følger AAA og er uafhængige af rækkefølgen.
- Fixtures/monkeypatch rydder op efter lokale ændringer.
- GET-kald opretter ingen serverdata, så der er ingen serverdata at slette.
- Live-tests bruger internet og API-kvote; kør dem særskilt fra unit tests.

**Status:** Testlisterne og unit tests er oprettet. Se [partitions og BVA](currency_partitions_and_bva.md) for alle cases. Næste skridt er at gennemgå testresultaterne.

## Dokumentation

- [Latest: kurser](https://currencyapi.com/docs/latest/)
- [Currencies: valutaoplysninger](https://currencyapi.com/docs/currencies/)
- [Python-klienten](https://github.com/everapihq/currencyapi-python)
