**English** · [Dansk](Step-9-da) · [Bahasa Melayu](Step-9-ms)

# Step 9: Resilience against network failures

## What you gain

You learn to retry: `retry(func, retries=7, description=None)` repeats a call that raises, waits between attempts, logs a warning and raises RetriesExhaustedError at the end. `login()`, `book_class()` and `get_my_bookings()` are wrapped with it, so a site that drops requests does not stop the run.

## Where it is in the code

`src/snack_and_lift/application/retry.py`

## Screenshot

![Step 9: Resilience against network failures](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/049-snack-and-lift/raw/branch/main/docs/images/step-9.png)

[Previous: 8](Step-8) · [Home](Home)
