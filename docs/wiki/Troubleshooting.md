**English** · [Dansk](Troubleshooting-da) · [Bahasa Melayu](Troubleshooting-ms)

# Troubleshooting

| Symptom | Cause and fix |
| --- | --- |
| Exit code 2 | `SNACK_AND_LIFT_EMAIL` or `SNACK_AND_LIFT_PASSWORD` is not set. |
| Login fails 7 times, then exit 1 | Wrong e-mail or password, or the account is not in this `chrome_profile` (the site keeps accounts in the browser). Register again with `--keep-open`. |
| Exit code 3 and MISMATCH | The My Bookings page does not list what the bot booked. Run again; check whether a class was full. |
| Warnings "attempt 2 of 7" | The site's failure rate is on; this is the retry at work (step 9). |
| Chrome warns about the password | Chrome flags weak passwords such as `12346`; choose another. |
| No window in Docker | The container is headless by design; use `--screenshot-dir`. |
