[English](Step-9) · **Dansk** · [Bahasa Melayu](Step-9-ms)

# Trin 9: Robusthed mod netværksfejl

## Hvad du får ud af det

Du lærer at prøve igen: `retry(func, retries=7, description=None)` gentager et kald der kaster en fejl, venter mellem forsøgene, logger en advarsel og kaster RetriesExhaustedError til sidst. `login()`, `book_class()` og `get_my_bookings()` er pakket ind i den, så en side der taber forespørgsler ikke stopper kørslen.

## Hvor det er i koden

`src/snack_and_lift/application/retry.py`

## Skærmbillede

![Trin 9: Robusthed mod netværksfejl](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/049-snack-and-lift/raw/branch/main/docs/images/step-9.png)

[Forrige: 8](Step-8-da) · [Forside](Home-da)
