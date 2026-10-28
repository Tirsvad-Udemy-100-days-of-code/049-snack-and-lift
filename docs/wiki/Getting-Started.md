**English** · [Dansk](Getting-Started-da) · [Bahasa Melayu](Getting-Started-ms)

# Getting started

## Requirements

Python 3.13 or newer, Chrome or Chromium, and (optional) Docker.

## Install

```bash
python -m venv .venv
```

```bash
source .venv/bin/activate
```

```powershell
.venv\Scripts\Activate.ps1
```

```bash
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

## Your account

The bot contains no password. Register once by hand on the site (run with `--keep-open`, so the `chrome_profile` folder keeps the site's data), then give the bot the account:

```bash
export SNACK_AND_LIFT_EMAIL="yourname@test.com"
export SNACK_AND_LIFT_PASSWORD="your password"
```

```powershell
$env:SNACK_AND_LIFT_EMAIL = "yourname@test.com"
$env:SNACK_AND_LIFT_PASSWORD = "your password"
```

## The account file

Instead of setting variables by hand, put the same lines in a file `.env.gym` in the project folder (`SNACK_AND_LIFT_EMAIL=...` and `SNACK_AND_LIFT_PASSWORD=...`). The bot reads it at start; `--env-file PATH` names another file, and a real environment variable wins over the file. Git ignores `.env.gym`: never commit it. The optional `SNACK_AND_LIFT_ADMIN_EMAIL` and `SNACK_AND_LIFT_ADMIN_PASSWORD` hold the practice site's admin account; the bot loads them but does not use them yet.

## Run and test

```bash
snack-and-lift
```

```bash
python -m pytest
```

Useful options: `--headless`, `--keep-open`, `--first-tuesday-only` (steps 3 and 4), `--retries N`, `--profile-dir DIR`, `--screenshot-dir DIR`.

## Exit codes

0 done, 1 a step failed (also when every retry failed), 2 credentials missing, 3 the My Bookings page does not match the bookings made.

## Taking the screenshots (maintainer)

The site keeps its data in the browser profile, so a container run needs an account that exists in that profile. Use `--env-file` for the credentials (never write them on the command line or into the repository) and a volume for the profile and the screenshots:

```bash
docker build -t snack-and-lift .
docker run --rm --env-file my.env -v snack-profile:/app/chrome_profile -v "$PWD/docs/images:/app/screenshots" snack-and-lift --headless --screenshot-dir /app/screenshots
```
