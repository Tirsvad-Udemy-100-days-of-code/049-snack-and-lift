[English](Troubleshooting) · **Dansk** · [Bahasa Melayu](Troubleshooting-ms)

# Fejlfinding

| Symptom | Årsag og løsning |
| --- | --- |
| Exitkode 2 | `SNACK_AND_LIFT_EMAIL` eller `SNACK_AND_LIFT_PASSWORD` er ikke sat. |
| Login fejler 7 gange, derefter exit 1 | Forkert e-mail eller adgangskode, eller kontoen findes ikke i denne `chrome_profile` (siden gemmer konti i browseren). Opret den igen med `--keep-open`. |
| Exitkode 3 og MISMATCH | Siden My Bookings viser ikke det botten bookede. Kør igen; tjek om et hold var fyldt. |
| Advarsler "attempt 2 of 7" | Sidens fejlrate er slået til; det er retry der arbejder (trin 9). |
| Chrome advarer om adgangskoden | Chrome markerer svage adgangskoder som `12346`; vælg en anden. |
| Intet vindue i Docker | Containeren er headless med vilje; brug `--screenshot-dir`. |
