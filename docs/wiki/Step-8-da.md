[English](Step-8) · **Dansk** · [Bahasa Melayu](Step-8-ms)

# Trin 8: Kvalitetssikring med tidsrejse

## Hvad du får ud af det

Du lærer at datoer er den almindelige fejlkilde: sidens admin-knap "advance 3 days" flytter dens ur. Botten læser dagsetiketterne ("Today", "Tomorrow", "Thu, Aug 14") i stedet for at antage en dato, så den også virker efter et tidshop.

## Hvor det er i koden

`src/snack_and_lift/domain/day_label.py`

## Skærmbillede

![Trin 8: Kvalitetssikring med tidsrejse](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/049-snack-and-lift/raw/branch/main/docs/images/step-8.png)

> Dette billede er taget før en rettelse: siden My Bookings viser også bookinger fra tidligere kørsler uden for tidsplanens næste 7 dage, og kontrollen endte så i MISMATCH. Kontrollen sammenligner nu kun kørslens dage og skriver de øvrige bookinger som "Also booked (not checked)", så samme kørsel ender i SUCCESS.

[Forrige: 7](Step-7-da) · [Forside](Home-da) · [Næste: 9](Step-9-da)
