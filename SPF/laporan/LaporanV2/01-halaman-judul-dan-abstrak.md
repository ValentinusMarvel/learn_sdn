# 4.1 Halaman Judul

## LAPORAN PROYEK AKHIR KULIAH
### MATA KULIAH: ARSITEKTUR JARINGAN MODERN

---

### JUDUL PROYEK:
**Analisis Komparatif Performa dan Resiliensi Algoritma Routing *Single-Source Shortest Path* (A\*, Bellman-Ford, dan Widest Path) pada Jaringan *Software-Defined Networking* (SDN) Berbasis OS-Ken dan Mininet**

*   **Topik yang Dipilih**: Topik 1 (Analisis Performa Algoritma Perutean SPF Tunggal)
*   **Nama Mata Kuliah**: Arsitektur Jaringan Modern
*   **Semester Akademik**: Semester Genap / 2025-2026
*   **Dosen Pengampu**: [Nama Dosen Pengampu]
*   **Program Studi**: Teknik Informatika / Teknik Komputer

### DAFTAR ANGGOTA KELOMPOK:
| No | Nama | NIM |
|:-:|:---|:---:|
| 1 | [Nama Anggota 1] | [NIM Anggota 1] |
| 2 | [Nama Anggota 2] | [NIM Anggota 2] |
| 3 | [Nama Anggota 3] | [NIM Anggota 3] |
| 4 | [Nama Anggota 4] | [NIM Anggota 4] |

---

# 4.2 Abstrak

Penelitian ini bertujuan untuk melakukan analisis komparatif terhadap performa dan resiliensi tiga algoritme perutean *Single-Source Shortest Path* (SPF), yaitu A\*, Bellman-Ford, dan Widest Path, pada jaringan *Software-Defined Networking* (SDN). Pengujian dilakukan menggunakan emulator Mininet dengan pengendali berbasis OS-Ken melalui protokol OpenFlow 1.3 pada dua arsitektur jaringan yang berbeda: topologi teratur melingkar (Ring-5) dan topologi acak regular (Jellyfish). Eksperimen dijalankan di bawah tujuh skenario kegagalan dinamis yang mencakup kondisi *baseline* tanpa gangguan, pemutusan link sebelum dan selama transmisi data, fluktuasi tautan (*link flap*), kegagalan switch total (*switch down*), pembatasan bandwidth (*bandwidth throttle*), dan pemutusan link acak khusus Jellyfish. Data dikumpulkan secara otomatis melalui testbed terotomatisasi dengan parameter 20 pasangan host acak dan 5 kali pengulangan untuk setiap skenario, menghasilkan total 3.900 baris data pengujian yang valid. Hasil evaluasi menunjukkan dua temuan utama. Pertama, algoritme A\* secara konsisten mencatatkan runtime komputasi jalur tercepat pada topologi kompleks Jellyfish, yaitu rata-rata 0.0749 ms, dibandingkan Bellman-Ford (0.0942 ms) dan Widest Path (0.0846 ms); keunggulan ini berasal dari mekanisme pemangkasan (*pruning*) berbasis estimasi heuristik *reverse-BFS* yang membatasi eksplorasi node graf tidak relevan. Kedua, algoritme Bellman-Ford menempati peringkat komposit teratas di kedua topologi dengan skor komposit 0.8000 karena mengalami anomali *bypass throttling* yang menguntungkan: controller Bellman-Ford membaca matriks bandwidth statis dari file konfigurasi `link_weights.json` sebagai *biaya jalur* (bukan kapasitas), sehingga secara tidak sengaja menghindari link yang sedang dibatasi kapasitasnya dan berhasil mempertahankan throughput 95.03 Mbps pada Ring-5. Sebaliknya, Widest Path mencatatkan penurunan throughput paling drastis hingga 86.39 Mbps pada Ring-5 akibat ketidakmampuan controller beradaptasi terhadap pembatasan bandwidth dinamis yang tidak tercatat di konfigurasi statis. Temuan ini menegaskan pentingnya representasi bobot link yang dinamis pada pengendali SDN untuk menjamin efisiensi dan keakuratan perutean di berbagai kondisi kegagalan jaringan.

**Kata Kunci**: *Software-Defined Networking*, OpenFlow, A\*, Bellman-Ford, Widest Path, Mininet, OS-Ken.
