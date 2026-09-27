# Testplan: Grade med en database-stub

## Formål og fremgangsmåde

Vi tester `convert(grade, country)` isoleret fra SQLite-databasen.

1. Find gyldige og ugyldige input med **Equivalence Partitioning**.
2. Undersøg relevante naboværdier med **BVA**.
3. Brug en **stub** til at levere faste database-svar.
4. Skriv pytest-tests med **AAA** og **parametrisering**.

En stub leverer et valgt svar uden at udføre SQL. Det rigtige SQL-opslag
undersøges særskilt i vores integrationstests mod SQLite.

## Projektets karaktertabel

Dette er vores egen mapping til øvelsen. Vi tester alle par i begge retninger.

| Dansk karakter | Amerikansk karakter |
|---|---|
| `"00"` | `"F"` |
| `"02"` | `"D"` |
| `"04"` | `"C+"` |
| `"07"` | `"B"` |
| `"10"` | `"A"` |
| `"12"` | `"A+"` |

Karakteren er tekst, så `"02"` beholder sit nul. Landet angiver systemet for
**inputkarakteren**, ikke det ønskede resultat.

- `("12", "Denmark")` skal give `"A+"`.
- `("A", "USA")` skal give `"10"`.

## Gyldige partitions

| Gruppe | Eksempel | Forventet resultat |
|---|---|---|
| Understøttet dansk karakter | `("04", "Denmark")` | `"C+"` |
| Understøttet amerikansk karakter | `("B", "USA")` | `"07"` |

## Ugyldige partitions

Hver case nedenfor skal give en fejl. Et opslag uden resultat må ikke give
en tilfældig karakter.

### Karakteren

| Gruppe | Testcases: `(grade, country)` |
|---|---|
| Tal uden for projektskalaen | `("-5", "Denmark")`, `("13", "Denmark")` |
| Tal mellem understøttede karakterer | `("03", "Denmark")` |
| Karakter uden mapping | `("-3", "Denmark")`, `("C", "USA")` |
| Ukendt tekst | `("ABC", "Denmark")`, `("Z", "USA")` |
| Tom tekst | `("", "Denmark")` |
| Manglende værdi | `(None, "Denmark")` |
| Forkert datatype | `([], "Denmark")`, `(True, "Denmark")` |
| Karakter fra det andet system | `("A", "Denmark")`, `("12", "USA")` |

### Landet

| Gruppe | Testcase |
|---|---|
| Ukendt land | `("12", "Sweden")` |
| Tom tekst | `("12", "")` |
| Manglende værdi | `("12", None)` |
| Forkert datatype | `("12", 123)` |

## BVA og naboværdier

Karakterer er enkelte tilladte værdier. Alle tal mellem 0 og 12 er altså
ikke gyldige. Tabellen undersøger netop værdier omkring de valgte karakterer.
Landet er `"Denmark"` i alle disse cases.

| Område | Værdi under | Valgt karakter | Værdi over |
|---|---|---|---|
| Laveste understøttede karakter | `"-1"`: ugyldig | `"00"` → `"F"` | `"01"`: ugyldig |
| Laveste beståede karakter | `"01"`: ugyldig | `"02"` → `"D"` | `"03"`: ugyldig |
| Højeste understøttede karakter | `"11"`: ugyldig | `"12"` → `"A+"` | `"13"`: ugyldig |

**Ikke-bestået er ikke det samme som ugyldigt input:** Både `"00"` og `"02"`
skal konverteres. Klassen afgør ikke selv, om en elev har bestået.

Der er ingen afstand som +1 mellem amerikanske bogstavkarakterer. Vi tester
alle seks tilladte værdier og en ukendt værdi som `"Z"`, uden at bruge
alfabetets rækkefølge som BVA.

## Hvad skal stubben returnere?

| Database-situation | Stub-svar | Forventning til convert() |
|---|---|---|
| Opslaget finder en række | `("A+",)` | Returnér `"A+"` |
| Opslaget finder ingen række | `None` | Giv en fejl |

Stubben indeholder ingen ny konverteringslogik. Den returnerer det svar,
som den enkelte test har valgt.

## Afklaringer

- `-3` er en dansk karakter, men vores tabel understøtter den ikke.
- `"C"` har ingen mapping; projektet bruger `"C+"`.
- Tal som `4`, tekst som `"4"`, små bogstaver og ekstra mellemrum er ikke
  afklaret. De skal ikke automatisk regnes som ugyldige testcases.

## Sådan skrives testene

- **Arrange:** Vælg input og stub-svar; opret Grade-objektet.
- **Act:** Kald `convert()`.
- **Assert:** Kontrollér resultatet eller den forventede fejl.

Brug `pytest.mark.parametrize` til beslægtede cases og `pytest.raises` til
fejl. En fixture med `monkeypatch` erstatter forbindelsen og gendanner den
oprindelige funktion efter hver test.
