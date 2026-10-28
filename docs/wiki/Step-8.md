**English** · [Dansk](Step-8-da) · [Bahasa Melayu](Step-8-ms)

# Step 8: Time travel quality assurance

## What you gain

You learn that dates are the usual bug: the site's admin control "advance 3 days" moves its clock. The bot reads the day labels ("Today", "Tomorrow", "Thu, Aug 14") instead of assuming a date, so it works after a time jump too.

## Where it is in the code

`src/snack_and_lift/domain/day_label.py`

## Screenshot

![Step 8: Time travel quality assurance](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/049-snack-and-lift/raw/branch/main/docs/images/step-8.png)

> This image is an illustration: the bot ran against the project's local test pages (`tests/e2e/fixtures`), not against the live gym site. A run with a real account and `--screenshot-dir` (see [Getting started](Getting-Started)) replaces it.

[Previous: 7](Step-7) · [Home](Home) · [Next: 9](Step-9)
