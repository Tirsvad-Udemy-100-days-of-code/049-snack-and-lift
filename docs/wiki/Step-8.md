**English** · [Dansk](Step-8-da) · [Bahasa Melayu](Step-8-ms)

# Step 8: Time travel quality assurance

## What you gain

You learn that dates are the usual bug: the site's admin control "advance 3 days" moves its clock. The bot reads the day labels ("Today", "Tomorrow", "Thu, Aug 14") instead of assuming a date, so it works after a time jump too.

## Where it is in the code

`src/snack_and_lift/domain/day_label.py`

## Screenshot

![Step 8: Time travel quality assurance](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/049-snack-and-lift/raw/branch/main/docs/images/step-8.png)

> This screenshot needs a run with a real gym account. The maintainer adds it with `--screenshot-dir` (see [Getting started](Getting-Started)); until then the file `docs/images/step-8.png` is missing and the image above does not show.

[Previous: 7](Step-7) · [Home](Home) · [Next: 9](Step-9)
