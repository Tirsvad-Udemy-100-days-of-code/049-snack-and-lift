[English](Step-9) · [Dansk](Step-9-da) · **Bahasa Melayu**

# Langkah 9: Ketahanan terhadap kegagalan rangkaian

## Apa yang anda peroleh

Anda belajar mencuba semula: `retry(func, retries=7, description=None)` mengulang panggilan yang gagal, menunggu antara percubaan, mencatat amaran dan melempar RetriesExhaustedError di akhir. `login()`, `book_class()` dan `get_my_bookings()` dibalut dengannya, jadi laman yang menjatuhkan permintaan tidak menghentikan larian.

## Di mana dalam kod

`src/snack_and_lift/application/retry.py`

## Tangkapan skrin

![Langkah 9: Ketahanan terhadap kegagalan rangkaian](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/049-snack-and-lift/raw/branch/main/docs/images/step-9.png)

> Imej ini ialah ilustrasi: bot dijalankan terhadap halaman ujian tempatan projek (`tests/e2e/fixtures`), bukan laman gim sebenar. Larian dengan akaun sebenar dan `--screenshot-dir` (lihat [Mula menggunakan](Getting-Started-ms)) menggantikannya.

[Sebelumnya: 8](Step-8-ms) · [Utama](Home-ms)
