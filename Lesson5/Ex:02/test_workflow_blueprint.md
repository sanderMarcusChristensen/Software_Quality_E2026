# Vores testforløb – forslag til en blueprint

## Formål

Dokumentet beskriver, hvordan vi har arbejdet med tests i konverteringsopgaven.
Målet er at få feedback fra underviseren på rækkefølgen og vores valg, så vi
kan bruge erfaringerne som udgangspunkt for test af andre systemer.

Det er et forslag til en arbejdsproces, ikke en færdig regel om, hvordan
alle systemer skal testes.

## Overblik over vores flow

**Krav og afklaringer → partitions → BVA → konkrete testcases → unit tests
→ undersøg fejl → integrationstests → vurder dækning og næste skridt**

Vi begyndte med Length, Weight og Temperature. Derefter brugte vi samme
tilgang til Grade, men delte testene i to:

1. Unit tests med en database-stub.
2. Narrow integration tests med en rigtig SQLite-database.

Klasserne var allerede skrevet, da vi begyndte testarbejdet. Forløbet har
derfor ikke været klassisk test-driven development, hvor testen skrives
før den funktionalitet, der skal implementeres.

## 1. Forstå kravene og afklar egne valg

Vi tog udgangspunkt i opgavens beskrivelse af input, output og konverteringer.
Før testcases kan få et forventet resultat, skal vi vide, hvad gyldig og
ugyldig adfærd betyder.

Eksempler på valg i vores projekt:

- Length og Weight skal have et positivt mål. Det blev en projektregel;
  den oprindelige opgave angav ikke denne nedre grænse.
- Måleklasserne skal afvise input med mere end to decimaler.
- Vi satte ingen vilkårlig øvre grænse, når opgaven ikke angav en.
- Vi lavede vores egen karaktertabel, fordi lærerens tabel ikke var tilgængelig.
- Karakterer behandles som tekst, så eksempelvis "02" beholder sit nul.

**Det, vi vil genbruge:** Skriv både krav og egne antagelser ned. En test
skal have en begrundelse for sit forventede resultat.

## 2. Equivalence Partitioning: opdel input i grupper

Vi brugte black-box-design: Vi valgte testdata ud fra den forventede adfærd
og inputreglerne, frem for at lade kodens if-sætninger bestemme testene.

Vi opdelte input i grupper, som forventes at blive behandlet på samme måde,
og valgte repræsentative værdier fra grupperne.

Eksempler:

| Område | Gyldige eksempler | Ugyldige eksempler |
|---|---|---|
| Length og Weight | Positivt mål, kendt system | Nul, negativt mål, ukendt system |
| Temperature | Tal med højst to decimaler, kendte skalaer | Ukendt skala, ikke-numerisk mål |
| Grade | Karakter og land med en understøttet mapping | Ukendt karakter, tom værdi, ukendt land |

Vi tog højde for flere inputparametre. En gyldig karakter kan eksempelvis
være ugyldig sammen med et bestemt land: "A" er amerikansk input, ikke dansk.

## 3. Boundary Value Analysis: undersøg grænser

Når vi havde en defineret grænse, valgte vi værdier omkring den.

For Length og Weight blev den valgte nedre grænse:

- 0.00: ugyldig.
- 0.01: gyldig.
- 0.02: gyldig.

Karakterer kræver en anden overvejelse. "00", "02" og "04" er enkelte
tilladte værdier; alle tal imellem er ikke gyldige. Vi tog derfor både
understøttede karakterer og ugyldige naboværdier med.

"00" er gyldigt input til konvertering, selv om karakteren betyder
ikke-bestået. Grade-klassen oversætter karakteren og beregner ikke selv,
om en elev har bestået.

**Det, vi vil genbruge:** Brug BVA, hvor der findes en meningsfuld orden og
grænse. Afklar med underviseren, hvordan teknikken bedst bruges på diskrete
værdier som karakterer og på et krav om antal decimaler.

## 4. Lav konkrete positive og negative testcases

Vi samlede værdierne fra partitions og BVA i to grupper:

- Positive cases: gyldigt input skal give et bestemt resultat.
- Negative cases: ugyldigt input skal give den aftalte fejl.

En testcase skal beskrive input og forventet output eller fejl. Eksempel:

| Input | Forventning |
|---|---|
| Length: 1 inch | 2.54 cm |
| Temperature: 32 F til C | 0 C |
| Grade: "12", "Denmark" | "A+" efter projektets mapping |
| Grade: "ABC", "Denmark" | Fejl: karakteren findes ikke |

Forventningerne skrives som faste værdier i testene. Vi skal ikke bruge
metoden, der testes, til at beregne dens eget forventede resultat.

## 5. Skriv unit tests med pytest og AAA

Vi skrev først unit tests for Length, Weight og Temperature. De har ingen
database eller API, så deres beregninger kan testes direkte.

Vi brugte:

- `@pytest.mark.parametrize` som data provider, så én testfunktion kan
  afprøve flere inputs og forventede resultater.
- `pytest.raises` til at kontrollere forventede fejl.
- AAA til at gøre hver tests forløb tydeligt.

AAA betyder:

1. **Arrange:** Forbered input, objekt og forventning.
2. **Act:** Kald den funktion, der skal undersøges.
3. **Assert:** Kontrollér resultatet eller fejlen.

`conftest.py` sørger i vores projekt for, at pytest kan importere klasserne
fra deres placering i kode-mapperne.

## 6. Undersøg fejl, før noget bliver rettet

De første konverteringstests viste, at nogle input blev accepteret, selv om
vores plan sagde, at de skulle afvises. Eksempelvis blev input med mere end
to decimaler afrundet i stedet for at udløse en fejl.

Vi tilføjede validering i klasserne efter at have sammenholdt fejlene med
vores aftalte regler.

**Det, vi vil genbruge:** En fejlet test skal undersøges. Fejlen kan ligge i
koden, testens forventning eller et uklart krav. Et grønt resultat er ikke
i sig selv en grund til at ændre en forventning.

## 7. Grade: unit tests med en stub

Grade afhænger af en database. Vi begyndte derfor med at erstatte forbindelsen
med en lille `DatabaseStub`, som returnerer faste svar.

- En række som `("A+",)` efterligner et fundet resultat.
- `None` efterligner et opslag, der ikke finder noget.

Stubben indeholder ingen SQL-motor og finder ikke selv karakteren.
Testen vælger dens svar. Vi undersøger, om Grade returnerer det fundne
resultat og håndterer manglende resultater og ugyldige lande.

En pytest-fixture bruger `monkeypatch` til at udskifte forbindelsen.
`monkeypatch` gendanner automatisk den oprindelige funktion efter hver test.

**Begrænsning:** Disse tests viser ikke, om SQL-opslaget finder den rigtige
række. Den del kræver den rigtige database.

## 8. Grade: narrow integration tests mod SQLite

Derefter testede vi samarbejdet mellem Grade, SQLite-driveren og en rigtig
database med tabellen og karakterparrene.

Vi valgte SQLite, fordi opgaven tillader frit valg af DBMS, og vores database
kan ligge i én lokal fil. Der er ingen MySQL-server i løsningen.

Hver test bruger en frisk kopi af projektets `grades.db`:

1. **Setup:** Kopier databasen til en midlertidig fil.
2. **Test:** Kald Grade mod kopien med rigtig SQL.
3. **Teardown:** Slet kopien, også hvis testen fejler.

På den måde kan en test eksempelvis tømme sin tabel uden at påvirke næste
test eller projektets database. Vi bruger pytest-fixtures til setup og
teardown og AAA inde i selve testfunktionerne.

Vi tester blandt andet alle karakterpar i begge retninger, opslag uden
resultat og en tom tabel.

**Afgrænsning:** Dette tester kun samarbejdet omkring databasen. Det er
ikke en end-to-end-test af et helt program med brugergrænseflade. Testene
kopierer en eksisterende database og afprøver ikke selve setup-scriptet.

## 9. Det næste arbejde

Currency mangler samme opdeling: isolerede tests med faste API-svar og tests
mod det rigtige API. Her skal vi også tage stilling til skiftende kurser,
API-nøgle, netværksfejl og reproducerbare forventninger.

Vi har heller ikke gennemført en systematisk white-box-testdesignfase,
hvor vi bruger kodens grene og kontrolflow til at finde yderligere cases.
At vi har læst koden under fejlsøgning er ikke i sig selv sådan en fase.

## Forslag til en genbrugelig blueprint

1. Beskriv krav, input, output og åbne spørgsmål.
2. Find relevante partitions og grænser.
3. Vælg repræsentative cases, grænseværdier og ekstreme inputs.
4. Angiv forventet resultat eller fejl for hver case.
5. Skriv isolerede unit tests med AAA og parametrisering.
6. Brug test doubles, hvor unit tests ellers ville kræve eksterne systemer.
7. Test derefter de relevante integrationer med isolerede testdata.
8. Undersøg fejl og afklar, om krav, kode eller test skal ændres.
9. Vurder, hvilke fejl testene stadig kan overse, og suppler efter behov.

Processen kan gentages, når krav ændres eller nye fejl bliver fundet.
Black-box og white-box er teknikker til testdesign; unit og integration
beskriver, hvor meget af systemet en test undersøger. De er ikke gensidigt
udelukkende kategorier.

## Spørgsmål til underviseren

1. Er rækkefølgen fra partitions og BVA til unit tests og derefter integration
   passende til denne opgave?
2. Er vores skelnen mellem opgavens krav og egne valideringsregler tydelig nok?
3. Hvordan bør vi anvende BVA på en diskret karakterskala og decimalpræcision?
4. Giver stub-testene og integrationstestene den ønskede opdeling af ansvar?
5. Er en frisk SQLite-kopi pr. test en passende form for data-isolation?
6. Opfylder stubben opgavens formulering om at mocke afhængigheder, eller
   forventes der også mocks, som kontrollerer kald og argumenter?
7. Hvornår bør vi supplere med white-box-design og måling af dækning?
8. Hvad mangler der i denne blueprint, før den kan bruges i næste projekt?
