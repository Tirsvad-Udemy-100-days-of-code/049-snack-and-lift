[English](Step-7) · **Dansk** · [Bahasa Melayu](Step-7-ms)

# Trin 7: Bekræft på siden My Bookings

## Hvad du får ud af det

Du lærer at kontrollere dit eget arbejde fra en anden kilde: `get_my_bookings()` læser siden My Bookings (bookinger og venteliste) og `verify_bookings()` sammenligner med det botten gjorde. Resultatet er SUCCESS eller MISMATCH (exitkode 3).

## Hvor det er i koden

`src/snack_and_lift/application/verification.py`

## Skærmbillede

![Trin 7: Bekræft på siden My Bookings](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/049-snack-and-lift/raw/branch/main/docs/images/step-7.png)

> Dette billede er en illustration: botten kørte mod projektets lokale testsider (`tests/e2e/fixtures`), ikke mod det rigtige gym-site. En kørsel med en rigtig konto og `--screenshot-dir` (se [Kom i gang](Getting-Started-da)) erstatter det.

[Forrige: 6](Step-6-da) · [Forside](Home-da) · [Næste: 8](Step-8-da)
