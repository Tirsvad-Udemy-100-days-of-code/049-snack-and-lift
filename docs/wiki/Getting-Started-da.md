[English](Getting-Started) · **Dansk** · [Bahasa Melayu](Getting-Started-ms)

# Kom i gang

## Krav

Python 3.13 eller nyere, Chrome eller Chromium og (valgfrit) Docker.

## Installation

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

## Din konto

Botten indeholder ingen adgangskode. Opret en konto én gang i hånden på siden (kør med `--keep-open`, så mappen `chrome_profile` gemmer sidens data), og giv derefter botten kontoen:

```bash
export SNACK_AND_LIFT_EMAIL="yourname@test.com"
export SNACK_AND_LIFT_PASSWORD="your password"
```

```powershell
$env:SNACK_AND_LIFT_EMAIL = "yourname@test.com"
$env:SNACK_AND_LIFT_PASSWORD = "your password"
```

## Kontofilen

I stedet for at sætte variabler i hånden kan du skrive de samme linjer i en fil `.env.gym` i projektmappen (`SNACK_AND_LIFT_EMAIL=...` og `SNACK_AND_LIFT_PASSWORD=...`). Botten læser den ved start; `--env-file PATH` peger på en anden fil, og en rigtig miljøvariabel vinder over filen. Git ignorerer `.env.gym`: læg den aldrig i repositoriet. De valgfrie `SNACK_AND_LIFT_ADMIN_EMAIL` og `SNACK_AND_LIFT_ADMIN_PASSWORD` gemmer øvelsessidens admin-konto; botten indlæser dem, men bruger dem ikke endnu.

## Kør og test

```bash
snack-and-lift
```

```bash
python -m pytest
```

Nyttige indstillinger: `--headless`, `--keep-open`, `--first-tuesday-only` (trin 3 og 4), `--retries N`, `--profile-dir DIR`, `--screenshot-dir DIR`.

## Exitkoder

0 færdig, 1 et trin fejlede (også når alle forsøg fejlede), 2 loginoplysninger mangler, 3 siden My Bookings passer ikke med de bookinger der blev lavet.

## Skærmbilleder (vedligeholder)

Siden gemmer sine data i browserens profil, så en kørsel i en container kræver en konto der findes i den profil. Brug `--env-file` til loginoplysningerne (aldrig på kommandolinjen eller i repositoriet) og et volume til profilen og skærmbillederne:

```bash
docker build -t snack-and-lift .
docker run --rm --env-file my.env -v snack-profile:/app/chrome_profile -v "$PWD/docs/images:/app/screenshots" snack-and-lift --headless --screenshot-dir /app/screenshots
```
