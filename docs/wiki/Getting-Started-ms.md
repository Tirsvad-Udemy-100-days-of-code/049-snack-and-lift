[English](Getting-Started) · [Dansk](Getting-Started-da) · **Bahasa Melayu**

# Mula menggunakan

## Keperluan

Python 3.13 atau lebih baharu, Chrome atau Chromium, dan (pilihan) Docker.

## Pemasangan

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

## Akaun anda

Bot tidak mengandungi kata laluan. Daftar sekali secara manual di laman (jalankan dengan `--keep-open` supaya folder `chrome_profile` menyimpan data laman), kemudian beri bot akaun itu:

```bash
export SNACK_AND_LIFT_EMAIL="yourname@test.com"
export SNACK_AND_LIFT_PASSWORD="your password"
```

```powershell
$env:SNACK_AND_LIFT_EMAIL = "yourname@test.com"
$env:SNACK_AND_LIFT_PASSWORD = "your password"
```

## Fail akaun

Daripada menetapkan pemboleh ubah secara manual, letakkan baris yang sama dalam fail `.env.gym` di folder projek (`SNACK_AND_LIFT_EMAIL=...` dan `SNACK_AND_LIFT_PASSWORD=...`). Bot membacanya semasa bermula; `--env-file PATH` menamakan fail lain, dan pemboleh ubah persekitaran sebenar mengatasi fail. Git mengabaikan `.env.gym`: jangan sekali-kali commit. `SNACK_AND_LIFT_ADMIN_EMAIL` dan `SNACK_AND_LIFT_ADMIN_PASSWORD` yang pilihan menyimpan akaun admin laman latihan; bot memuatkannya tetapi belum menggunakannya.

## Jalankan dan uji

```bash
snack-and-lift
```

```bash
python -m pytest
```

Pilihan berguna: `--headless`, `--keep-open`, `--first-tuesday-only` (langkah 3 dan 4), `--retries N`, `--profile-dir DIR`, `--screenshot-dir DIR`.

## Kod keluar

0 selesai, 1 satu langkah gagal (juga apabila semua percubaan gagal), 2 kelayakan tiada, 3 halaman My Bookings tidak sepadan dengan tempahan yang dibuat.

## Mengambil tangkapan skrin (penyelenggara)

Laman menyimpan datanya dalam profil pelayar, jadi larian dalam bekas memerlukan akaun yang wujud dalam profil itu. Gunakan `--env-file` untuk kelayakan (jangan pada baris arahan atau dalam repositori) dan volume untuk profil serta tangkapan skrin:

```bash
docker build -t snack-and-lift .
docker run --rm --env-file my.env -v snack-profile:/app/chrome_profile -v "$PWD/docs/images:/app/screenshots" snack-and-lift --headless --screenshot-dir /app/screenshots
```
