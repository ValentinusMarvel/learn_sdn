# Repositori Laporan Proyek Akhir Kuliah
**Mata Kuliah**: Arsitektur Jaringan Modern

Folder ini berisi **skeleton (kerangka kerja) laporan proyek akhir** yang terstruktur, lengkap, dan terperinci untuk memenuhi rubrik penilaian mata kuliah Arsitektur Jaringan Modern. Kerangka ini telah disegmentasikan menjadi beberapa dokumen terpisah agar Anda dapat menulis dan menganalisis setiap bagian secara efisien sebelum digabungkan menjadi dokumen akhir yang utuh.

---

## 📂 Struktur Segmentasi Laporan

Daftar di bawah ini merupakan dokumen kerangka kerja terpisah yang memetakan bab-bab pada outline tugas akhir Anda. Silakan klik tautan berkas untuk membukanya secara langsung:

1. **[00-judul-dan-identitas.md](file:///c:/Users/anang/OneDrive/Documents/GitHub/learn_sdn/SPF/laporan/00-judul-dan-identitas.md)**  
   *Berisi: Judul Proyek, Identitas Penulis/NIM, Dosen Pembimbing, tautan GitHub Repository, dan tautan YouTube Presentasi.*
2. **[03-latar-belakang.md](file:///c:/Users/anang/OneDrive/Documents/GitHub/learn_sdn/SPF/laporan/03-latar-belakang.md)**  
   *Berisi: Latar Belakang Masalah Jaringan SDN/Routing dinamis, Permasalahan Komparasi SPF, dan Tujuan Kuantitatif Proyek.*  
   *🎯 Fokus Rubrik: Pemahaman Masalah dan Tujuan (Skor Maksimal: 5/5)*
3. **[04-deskripsi-solusi.md](file:///c:/Users/anang/OneDrive/Documents/GitHub/learn_sdn/SPF/laporan/04-deskripsi-solusi.md)**  
   *Berisi: Gambaran Umum Solusi Ryu Controller berbasis SPF, Komponen Fitur Utama, serta Spesifikasi Alat & Teknologi (Mininet, Ryu, Python).*
4. **[05-perancangan-sistem.md](file:///c:/Users/anang/OneDrive/Documents/GitHub/learn_sdn/SPF/laporan/05-perancangan-sistem.md)**  
   *Berisi: Diagram Arsitektur Jaringan (Southbound OpenFlow 1.3), Flowchart Logika Rerouting Controller, dan Flowchart Siklus Testbed Otomatisasi.*  
   *🎯 Fokus Rubrik: Desain dan Arsitektur Solusi (Skor Maksimal: 5/5)*
5. **[06-implementasi.md](file:///c:/Users/anang/OneDrive/Documents/GitHub/learn_sdn/SPF/laporan/06-implementasi.md)**  
   *Berisi: Penjelasan Implementasi Berkas Kode (Topology, Controller, & Algorithms), Snippet Mekanisme Pengiriman Flow OpenFlow, dan Demo Hasil Visualisasi Grafik Analisis.*  
   *🎯 Fokus Rubrik: Implementasi dan Hasil (Skor Maksimal: 5/5)*
6. **[07-kesimpulan.md](file:///c:/Users/anang/OneDrive/Documents/GitHub/learn_sdn/SPF/laporan/07-kesimpulan.md)**  
   *Berisi: Ringkasan Hasil Capaian Performa Komposit, Kendala Teknis Codebase/Mininet, dan Rekomendasi Pengembangan Fitur Lanjutan (ECMP/Multipath).*

---

## 📈 Panduan Penilaian & Cara Memperoleh Skor 5/5

Setiap bagian skeleton di dalam berkas-berkas di atas telah disisipkan kotak petunjuk khusus **"PANDUAN RUBRIK PENILAIAN"** dengan tips taktis untuk memastikan laporan Anda memenuhi standar tertinggi (Sangat Baik/5 Poin).

Secara garis besar, pastikan Anda memenuhi kriteria berikut:
* **Pemahaman Masalah & Tujuan**: Deskripsikan urgensi membandingkan A*, Bellman-Ford, dan Widest Path secara mendalam di bawah kondisi kegagalan, bukan sekadar teori umum jaringan.
* **Desain & Arsitektur Solusi**: Sertakan diagram arsitektur Ryu-Mininet dan alur logis flowchart pemrosesan paket (tersedia panduan sintaksis Mermaid di dalam file rancangan).
* **Implementasi & Hasil**: Masukkan cuplikan kode penting seperti penanganan paket OpenFlow dan penyajian grafik visualisasi throughput/loss yang rapi hasil ekspor Jupyter Notebook.
* **Presentasi (Video)**: Pastikan video presentasi berdurasi sesuai ketentuan, menjelaskan demo kode secara runtut, dan tautan YouTube dicantumkan dengan benar di dokumen identitas.
* **Dokumentasi & Pengumpulan**: Format dokumen terstruktur rapi. Sebelum pengumpulan, satukan seluruh berkas Markdown tersegmentasi ini menjadi satu file utama (misalnya `Laporan_Akhir_AJM.md`).

---

## 🛠️ Cara Menggabungkan Laporan (Penyatuan Akhir)

Setelah Anda mengisi seluruh bagian tersegmentasi, Anda dapat menyatukannya secara instan menggunakan CLI command di terminal Anda (opsional, setelah semua file rampung diisi):

```bash
# Untuk pengguna Windows PowerShell:
Get-Content 00-judul-dan-identitas.md, 03-latar-belakang.md, 04-deskripsi-solusi.md, 05-perancangan-sistem.md, 06-implementasi.md, 07-kesimpulan.md | Out-File -FilePath Laporan_Proyek_Akhir_Lengkap.md -Encoding utf8
```
