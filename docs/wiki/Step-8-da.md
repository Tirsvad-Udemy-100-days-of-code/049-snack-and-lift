[English](Step-8) · **Dansk** · [Bahasa Melayu](Step-8-ms)

# Trin 8: Kvalitetssikring med tidsrejse

## Hvad du får ud af det

Du lærer at datoer er den almindelige fejlkilde: sidens admin-knap "advance 3 days" flytter dens ur. Botten læser dagsetiketterne ("Today", "Tomorrow", "Thu, Aug 14") i stedet for at antage en dato, så den også virker efter et tidshop.

## Hvor det er i koden

`src/snack_and_lift/domain/day_label.py`

## Skærmbillede

![Trin 8: Kvalitetssikring med tidsrejse](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/049-snack-and-lift/raw/branch/main/docs/images/step-8.png)

> Dette er en rigtig kørsel. Siden My Bookings viser også bookinger fra tidligere kørsler uden for tidsplanens næste 7 dage, så kontrollen melder dem som uventede og ender med MISMATCH. Det er en kendt fejl i kontrollen, som skal rettes.

[Forrige: 7](Step-7-da) · [Forside](Home-da) · [Næste: 9](Step-9-da)
