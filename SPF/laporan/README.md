# Repositori Laporan Proyek Akhir Kuliah
**Mata Kuliah**: Arsitektur Jaringan Modern

Folder ini berisi **skeleton (kerangka kerja) laporan proyek akhir** yang terstruktur, lengkap, dan terperinci untuk memenuhi rubrik penilaian mata kuliah Arsitektur Jaringan Modern. Kerangka ini telah didesain ulang dengan **penamaan sekuensial (01 s.d. 06)** agar Anda dapat menulis dan menganalisis setiap bagian secara runtut dan efisien sebelum digabungkan menjadi dokumen akhir yang utuh.

---

## 📂 Struktur Segmentasi Laporan (Sekuensial)

Daftar di bawah ini merupakan dokumen kerangka kerja terpisah yang memetakan bab-bab pada outline tugas akhir Anda secara berurutan. Silakan klik tautan berkas untuk membukanya secara langsung:

1. **[01-judul-dan-identitas.md](file:///c:/Users/anang/OneDrive/Documents/GitHub/learn_sdn/SPF/laporan/01-judul-dan-identitas.md)**  
   *Mencakup: Outline Bagian 1 (Judul Proyek) & Bagian 2 (Identitas Penulis, NIM, Dosen Pembimbing, Link GitHub, dan Link YouTube).*
2. **[02-latar-belakang.md](file:///c:/Users/anang/OneDrive/Documents/GitHub/learn_sdn/SPF/laporan/02-latar-belakang.md)**  
   *Mencakup: Outline Bagian 3 (Latar Belakang - Permasalahan yang Diangkat dan Tujuan Kuantitatif Proyek).*  
   *🎯 Fokus Rubrik: Pemahaman Masalah dan Tujuan (Skor Maksimal: 5/5)*
3. **[03-deskripsi-solusi.md](file:///c:/Users/anang/OneDrive/Documents/GitHub/learn_sdn/SPF/laporan/03-deskripsi-solusi.md)**  
   *Mencakup: Outline Bagian 4 (Deskripsi Solusi - Gambaran Umum Solusi, Fitur Utama/Komponen, serta Alat & Teknologi).*
4. **[04-perancangan-sistem.md](file:///c:/Users/anang/OneDrive/Documents/GitHub/learn_sdn/SPF/laporan/04-perancangan-sistem.md)**  
   *Mencakup: Outline Bagian 5 (Perancangan Sistem - Arsitektur Jaringan SDN, Flowchart Paket OS-Ken Controller, Flowchart Siklus Testbed, dan Desain CLI).*  
   *🎯 Fokus Rubrik: Desain dan Arsitektur Solusi (Skor Maksimal: 5/5)*
5. **[05-implementasi.md](file:///c:/Users/anang/OneDrive/Documents/GitHub/learn_sdn/SPF/laporan/05-implementasi.md)**  
   *Mencakup: Outline Bagian 6 (Implementasi - Penjelasan Komponen Utama Codebase, Snippet Mekanisme Pengiriman Flow OpenFlow, dan Grafik Visualisasi Analisis Performa).*  
   *🎯 Fokus Rubrik: Implementasi dan Hasil (Skor Maksimal: 5/5)*
6. **[06-kesimpulan.md](file:///c:/Users/anang/OneDrive/Documents/GitHub/learn_sdn/SPF/laporan/06-kesimpulan.md)**  
   *Mencakup: Outline Bagian 7 (Kesimpulan Proyek Akhir - Ringkasan Hasil Capaian Komposit, Kendala Codebase/Mininet, dan Rekomendasi Fitur Lanjutan).*

---

## 📈 Panduan Penilaian & Cara Memperoleh Skor 5/5

Setiap bagian skeleton di dalam berkas-berkas di atas telah disisipkan kotak petunjuk khusus **"PANDUAN RUBRIK PENILAIAN"** dengan tips taktis untuk memastikan laporan Anda memenuhi standar tertinggi (Sangat Baik/5 Poin).

Secara garis besar, pastikan Anda memenuhi kriteria berikut:
* **Pemahaman Masalah & Tujuan**: Deskripsikan urgensi membandingkan A*, Bellman-Ford, dan Widest Path secara mendalam di bawah kondisi kegagalan, bukan sekadar teori umum jaringan.
* **Desain & Arsitektur Solusi**: Sertakan diagram arsitektur OS-Ken-Mininet dan alur logis flowchart pemrosesan paket (tersedia panduan sintaksis Mermaid di dalam file rancangan).
* **Implementasi & Hasil**: Masukkan cuplikan kode penting seperti penanganan paket OpenFlow dan penyajian grafik visualisasi throughput/loss yang rapi hasil ekspor Jupyter Notebook.
* **Presentasi (Video)**: Pastikan video presentasi berdurasi sesuai ketentuan, menjelaskan demo kode secara runtut, dan tautan YouTube dicantumkan dengan benar di dokumen identitas.
* **Dokumentasi & Pengumpulan**: Format dokumen terstruktur rapi. Sebelum pengumpulan, satukan seluruh berkas Markdown tersegmentasi ini menjadi satu file utama (misalnya `Laporan_Akhir_AJM.md`).

---

## 🛠️ Cara Menggabungkan Laporan (Penyatuan Akhir)

Setelah Anda selesai mengisi seluruh bagian tersegmentasi, Anda dapat menyatukannya secara instan menggunakan CLI command di terminal Anda (opsional, setelah semua file rampung diisi):

```bash
# Untuk pengguna Windows PowerShell:
Get-Content 01-judul-dan-identitas.md, 02-latar-belakang.md, 03-deskripsi-solusi.md, 04-perancangan-sistem.md, 05-implementasi.md, 06-kesimpulan.md | Out-File -FilePath Laporan_Proyek_Akhir_Lengkap.md -Encoding utf8
```
