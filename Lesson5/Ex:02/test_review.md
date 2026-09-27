# Kritisk gennemgang af kode og tests

Dato: 27. september 2026.

## Konklusion

113 tests består, men det er ikke dokumentation for, at alle krav er dækket.
Gennemgangen fandt både manglende testdækning og konkrete problemer i koden.
Produktionskode og eksisterende tests er ikke ændret under gennemgangen.
Bevidste kodefejl blev kun indført i midlertidige kopier af projektet.

## 1. Temperaturtestene kan overse forkerte formler

F til C testes kun med 32 F. Udtrykket (32 - 32) er nul, så en forkert
multiplikationsfaktor bagefter ændrer ikke resultatet.

K til C testes kun med 273.15 K. Her er resultatet også nul.

Bevis: Begge følgende ændringer lod alle 113 tests bestå, hver for sig:

- F til C: erstat (measure - 32) * 5 / 9 med (measure - 32) * 9 / 5.
- K til C: erstat measure - 273.15 med (measure - 273.15) * 2.

Forbedring: Tilføj blandt andet 212 F -> 100 C og 300 K -> 26.85 C.
Brug flere forskellige input til hver af de seks konverteringer.
De eksisterende forventede resultater er korrekte; inputvalget er for smalt.

## 2. Uendelighed slipper gennem valideringen

Length(float('inf'), 'Metric').convert() returnerer inf.
Weight(float('inf'), 'Metric').convert() returnerer inf.
Temperature(float('inf'), 'C').convert('F') returnerer inf.

Det er ikke en almindelig måling med højst to decimaler. Kontrollen af antal
decimaler opdager det ikke, fordi round(inf, 2) stadig er inf.

Forbedring: Afvis ikke-endelige tal med en tydelig fejl, og test inf, -inf
og NaN. Der mangler også tests for bool og None i måleklasserne.
Store endelige værdier kan desuden give overflow; den ønskede fejlregel
skal beskrives, før vi laver en grænsetest for det.

## 3. Grade lukker ikke forbindelsen eksplicit

Med sqlite3 styrer 'with connection' transaktionen. Det lukker ikke i sig
selv forbindelsen. Grade.convert() bruger denne konstruktion uden close().

Bevis: En forbindelse opsamlet under convert() kunne stadig udføre
SELECT 1, efter metoden havde returneret. Eventuel senere oprydning af
Python-objektet er ikke det samme som eksplicit lukning i metoden.

Forbedring: Luk forbindelsen med try/finally eller contextlib.closing,
både ved succes og ved fejl. Tilpas stubben til close(), hvis det kræves.
Fixture-funktionen lukker sine egne backup-forbindelser, men ikke dem,
som Grade opretter. Sletning af en åben databasefil er også platformsafhængig.

## 4. Integrationstestene tester ikke setup-scriptet

Testene kopierer den eksisterende grades.db. De tester derfor den gemte
tabel og SQL-opslaget, men ikke om setup_grades.py kan bygge den korrekt.

Bevis: En ændring fra ('12', 'A+') til ('12', 'WRONG') i en midlertidig
kopi af setup-scriptet lod stadig alle 113 tests bestå. Scriptet bliver
ikke kørt af testene, og den eksisterende database ændres derfor ikke.

Forbedring: Test opbygning af en ny database samt genkørsel af setup.
Kontrollér de forventede rækker uafhængigt af scriptets grade_pairs.
Lad setup kunne modtage en teststi og undgå ændringer i databasen ved import.

## 5. Stub-testenes begrænsning er vigtig

Stubben returnerer et valgt svar uanset SQL og søgeparametre. Derfor viser
en grøn test, at Grade håndterer svaret korrekt. Den beviser ikke, at et
bestemt input vælger den rigtige række eller retning i databasen.

Bevis: Fjern WHERE-betingelsen og de tilhørende SQL-parametre:

- Alle 33 stub-tests består.
- 27 af de 34 integrationstests fejler.

Det er en forventet forskel mellem de to testtyper. Integrationstestene
giver her konkret ekstra sikkerhed. Der er én dublet af ('11', 'Denmark')
i stub-testene, så antallet 33 svarer ikke til 33 forskellige cases.

## 6. Databasen garanterer ikke en entydig omvendt mapping

danish_grade er PRIMARY KEY. american_grade er kun NOT NULL og kan derfor
forekomme flere gange. To danske karakterer kan få samme amerikanske værdi.
fetchone() vælger så blot én række ved omvendt konvertering.

Bevis i en separat database: ('00', 'F') og ('-3', 'F') kunne begge indsættes.
Den eksisterende projektdatabase har de seks aftalte par og ingen dubletter.

Forbedring: Hvis projektet fortsat kræver en-til-en-mapping, bør databasen
håndhæve UNIQUE på american_grade. Test også denne databasebegrænsning.
Alternativt skal vi definere, hvordan flere mulige resultater håndteres.

## 7. Krav og testdesign skal beskrives mere præcist

- Positive Length- og Weight-mål er en aftalt projektregel. Den stod ikke
  i den oprindelige opgavetekst. Vi skal kunne skelne egne regler fra krav.
- Temperature bruger en dictionary, ikke en bogstavelig switch/match.
  Det var vores aftalte løsning til Python 3.9. Hvis underviseren kræver
  selve switch-konstruktionen, er dette stadig en afvigelse fra opgaven.
- Hele tal, positive tal og tal med to decimaler er delvist overlappende
  grupper. Testplanen bør skelne mellem fortegn og antal decimaler.
- At tælle decimaler i numeriske Python-værdier er ikke det samme som at
  tælle tegn i brugerinput: 1.230 og 1.23 er samme float-værdi.
- Karakterer er diskrete værdier. '00', '02' og '04' er ikke et sammenhængende
  gyldigt interval. Naboværdierne i planen er nyttige ugyldige eksempler,
  men bestået/ikke-bestået er ikke en beregning udført af Grade.
- Grade accepterer også visse tal gennem str(grade): 10 kan findes, men 2
  bliver til '2' og matcher ikke '02'. Kravet til normalisering er uafklaret.
- Same-scale Temperature-konverteringer findes i koden, men er ikke testet,
  fordi den oprindelige opgave kun beskriver de seks konverteringer.
- Nogle ugyldige tests accepterer både TypeError og ValueError. Det kan
  skjule en utilsigtet Python-fejl. En fast aftale om fejltyper vil styrke dem.

## 8. Currency er endnu ikke dækket af testpakken

Der er endnu ingen pytest-tests for Currency, hverken med stub eller mod
API'et. 113 grønne tests siger derfor intet om denne klasse. API-arbejdet
er et udestående trin, ikke en verificeret del af afleveringen.

## Hvad gennemgangen faktisk bekræftede

- Alle 22 forventede resultater i Length-, Weight- og Temperature-testene
  blev genberegnet med Decimal-regning og stemmer med konverteringsformlerne.
- En bevidst ændring af længdefaktoren fra 2.54 til 2.50 blev opdaget:
  3 tests fejlede.
- Integrationstestene opdager en SQL-forespørgsel, som ignorerer inputtet.
- Den faktiske database indeholder præcis de seks aftalte mappings.
- Integrationstesten med SQL-lignende input består med parametriseret SQL.
- Hele den uændrede testpakke blev genkørt: 113 bestået.

## Foreslået rækkefølge

1. Tilføj temperaturcases, som opdager forkerte faktorer.
2. Tilføj tests for ikke-endelige målinger og eksplicit lukning af forbindelser.
3. Ret de beviste validerings- og forbindelsesproblemer.
4. Test setup-scriptet og databasens krav om entydige mappings.
5. Præcisér de åbne krav og opdatér testplanerne.
6. Lav Currency-tests som det næste selvstændige trin.

Mutationerne ovenfor er målrettede eksempler, ikke en fuldstændig
mutationstest eller et bevis for, at alle øvrige fejl bliver opdaget.
