[English](Troubleshooting) · [Dansk](Troubleshooting-da) · **Bahasa Melayu**

# Menyelesaikan masalah

| Gejala | Punca dan penyelesaian |
| --- | --- |
| Kod keluar 2 | `SNACK_AND_LIFT_EMAIL` atau `SNACK_AND_LIFT_PASSWORD` tidak ditetapkan. |
| Log masuk gagal 7 kali, kemudian keluar 1 | E-mel atau kata laluan salah, atau akaun tiada dalam `chrome_profile` ini (laman menyimpan akaun dalam pelayar). Daftar semula dengan `--keep-open`. |
| Kod keluar 3 dan MISMATCH | Halaman My Bookings tidak menyenaraikan apa yang ditempah bot. Jalankan semula; semak sama ada kelas penuh. |
| Amaran "attempt 2 of 7" | Kadar kegagalan laman dihidupkan; ini retry sedang berfungsi (langkah 9). |
| Chrome memberi amaran tentang kata laluan | Chrome menandakan kata laluan lemah seperti `12346`; pilih yang lain. |
| Tiada tetingkap dalam Docker | Bekas ini tanpa kepala (headless) secara sengaja; gunakan `--screenshot-dir`. |
