# Panduan Penggunaan dan Penggabungan Laporan V2

Direktori ini berisi kerangka (skeleton) laporan proyek akhir yang disusun secara tersegmentasi menjadi 8 berkas Markdown terpisah. Setiap berkas mewakili bab atau bagian dari struktur wajib laporan proyek akhir SDN:

1.  `01-halaman-judul-dan-abstrak.md` (Halaman Judul dan Abstrak)
2.  `02-pendahuluan.md` (Bab I Pendahuluan: Latar Belakang, Tujuan, Ruang Lingkup, Sistematika)
3.  `03-landasan-teori.md` (Bab II Landasan Teori: Algoritme, Topologi, Metrik Evaluasi)
4.  `04-metodologi.md` (Bab III Metodologi: Perancangan, Parameter Link, Prosedur Replikasi)
5.  `05-implementasi.md` (Bab IV Implementasi: Struktur Repositori, Mekanisme OpenFlow, Kendala)
6.  `06-hasil-dan-analisis.md` (Bab V Hasil dan Analisis: Grafik Relatif, Analisis Komparatif, Pembahasan Anomali)
7.  `07-kesimpulan-dan-saran.md` (Bab VI Kesimpulan dan Saran: Kesimpulan Empiris, Keterbatasan, Saran)
8.  `08-daftar-pustaka-dan-lampiran.md` (Daftar Pustaka IEEE dan Lampiran A, B, C)

Setiap berkas dilengkapi dengan kotak informasi dan petunjuk penulisan akademik untuk membantu Anda melengkapi isi laporan secara profesional.

---

## Petunjuk Penggabungan Berkas Laporan

Untuk menyatukan seluruh berkas Markdown tersegmentasi di atas menjadi satu dokumen laporan akhir utuh (`Laporan_Proyek_Akhir_SPF_Multipath.md`), Anda dapat menggunakan perintah CLI di Windows PowerShell.

### Langkah-langkah Penggabungan:

1.  Buka terminal **PowerShell** di komputer Anda.
2.  Arahkan direktori kerja terminal ke folder `LaporanV2` ini:
    ```powershell
    cd SPF/laporan/LaporanV2
    ```
3.  Jalankan perintah penggabungan di bawah ini:
    ```powershell
    Get-Content 01-halaman-judul-dan-abstrak.md, 02-pendahuluan.md, 03-landasan-teori.md, 04-metodologi.md, 05-implementasi.md, 06-hasil-dan-analisis.md, 07-kesimpulan-dan-saran.md, 08-daftar-pustaka-dan-lampiran.md | Out-File -Encoding utf8 Laporan_Proyek_Akhir_SPF_Multipath.md
    ```

Perintah di atas akan membaca semua berkas secara berurutan dan menuliskan hasilnya ke dalam satu berkas laporan kompilasi dengan pengkodean karakter UTF-8 agar semua teks, lambang matematika, dan format tabel tersimpan dengan sempurna.
