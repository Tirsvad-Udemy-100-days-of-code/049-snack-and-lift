[English](Step-8) · [Dansk](Step-8-da) · **Bahasa Melayu**

# Langkah 8: Jaminan kualiti dengan perjalanan masa

## Apa yang anda peroleh

Anda belajar bahawa tarikh ialah punca pepijat biasa: kawalan admin laman "advance 3 days" menggerakkan jamnya. Bot membaca label hari ("Today", "Tomorrow", "Thu, Aug 14") dan bukannya menganggap tarikh, jadi ia berfungsi selepas lompatan masa juga.

## Di mana dalam kod

`src/snack_and_lift/domain/day_label.py`

## Tangkapan skrin

![Langkah 8: Jaminan kualiti dengan perjalanan masa](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/049-snack-and-lift/raw/branch/main/docs/images/step-8.png)

> Ini ialah larian sebenar. Halaman My Bookings turut menyenaraikan tempahan daripada larian terdahulu di luar 7 hari jadual seterusnya, jadi semakan melaporkannya sebagai tidak dijangka dan berakhir dengan MISMATCH. Ini kecacatan yang diketahui pada semakan dan akan dibaiki.

[Sebelumnya: 7](Step-7-ms) · [Utama](Home-ms) · [Seterusnya: 9](Step-9-ms)
