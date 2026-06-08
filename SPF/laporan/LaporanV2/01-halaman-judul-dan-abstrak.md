# 4.1 Halaman Judul

## LAPORAN PROYEK AKHIR KULIAH
### MATA KULIAH: ARSITEKTUR JARINGAN MODERN

---

### JUDUL PROYEK:
**Analisis Komparatif Performa dan Resiliensi Algoritma Routing Single-Source Shortest Path (A\*, Bellman-Ford, dan Widest Path) pada Jaringan Software-Defined Networking (SDN) Berbasis OS-Ken dan Mininet**

*   **Topik yang Dipilih**: Topik 1 (Analisis Performa Algoritma Perutean SPF Tunggal)
*   **Semester Akademik**: Semester Genap / 2025-2026
*   **Dosen Pengampu**: [Nama Dosen Pengampu]

### DAFTAR ANGGOTA KELOMPOK:
1.  [Nama Anggota 1] - [NIM Anggota 1]
2.  [Nama Anggota 2] - [NIM Anggota 2]
3.  [Nama Anggota 3] - [NIM Anggota 3]
*(Catatan: Silakan sesuaikan daftar anggota kelompok Anda)*

---

# 4.2 Abstrak

> [!TIP]
> **PANDUAN PENULISAN ABSTRAK (Skor Maksimal: 5/5):**
> *   **Panjang**: Wajib ditulis dalam **satu paragraf** dengan panjang **200–300 kata**.
> *   **Bahasa**: Gunakan Bahasa Indonesia baku yang ringkas dan padat. Istilah asing ditulis miring (*italic*).
> *   **Komponen Wajib**:
>     1.  **Topik & Latar Belakang**: Sebutkan perutean dinamis berbasis Software-Defined Networking (SDN).
>     2.  **Topologi & Algoritme**: Sebutkan evaluasi komparatif algoritme A*, Bellman-Ford, dan Widest Path pada topologi Ring-5 dan Jellyfish.
>     3.  **Metode Eksperimen**: Sebutkan emulasi Mininet dengan pengendali OS-Ken, pengujian 7 skenario kegagalan link/switch, parameter `max_pairs=20` dan `repetitions=5` (total 3.900 baris data).
>     4.  **Dua Temuan Utama**:
>         *   *Temuan 1 (Runtime & Hop Count)*: A* memiliki runtime komputasi tercepat (rata-rata 0.0749 ms di Jellyfish) dengan hop count optimal yang sama dengan Bellman-Ford.
>         *   *Temuan 2 (Anomali Throttling & Resiliensi)*: Bellman-Ford menduduki peringkat komposit #1 karena anomali *bypass throttling* di Ring-5 (95.03 Mbps) akibat pemakaian matriks bandwidth statis sebagai cost, sedangkan Widest Path mengalami degradasi terburuk (86.39 Mbps) karena ketergantungan pada data link statis.
> *   **Kata Kunci**: Tuliskan 3–5 kata kunci di bawah paragraf abstrak.

### [TEMPLAT DRAFT ABSTRAK UNTUK DISESUAIKAN]
Penelitian ini bertujuan untuk melakukan analisis komparatif terhadap performa dan resiliensi tiga algoritme perutean *Single-Source Shortest Path* (SPF), yaitu A\*, Bellman-Ford, dan Widest Path, pada jaringan *Software-Defined Networking* (SDN). Pengujian dilakukan menggunakan emulator Mininet dengan pengendali berbasis OS-Ken (fork modern dari Ryu) melalui protokol OpenFlow 1.3. Eksperimen dijalankan pada dua arsitektur jaringan yang berbeda, yaitu topologi teratur melingkar (Ring-5) dan topologi acak regular (Jellyfish). Pengukuran dilakukan di bawah tujuh skenario kegagalan dinamis, termasuk kegagalan link dinamis, fluktuasi tautan (*link flap*), kegagalan switch, dan pembatasan bandwidth (*bandwidth throttling*). Data dikumpulkan secara otomatis melalui testbed dengan parameter 20 pasangan host acak dan 5 kali pengulangan untuk setiap skenario (total 3.900 baris data pengujian). Hasil evaluasi menunjukkan dua temuan utama. Pertama, algoritme A\* secara konsisten mencatatkan runtime komputasi jalur tercepat pada topologi kompleks dengan rata-rata 0.0749 ms pada Jellyfish, serta menghasilkan hop count efisien yang setara dengan Bellman-Ford. Kedua, algoritme Bellman-Ford menempati peringkat komposit teratas di kedua topologi (skor komposit 0.8000) karena mengalami anomali *bypass throttling* yang menguntungkan akibat penggunaan matriks bandwidth statis dari file konfigurasi sebagai biaya link, sementara Widest Path mencatatkan penurunan throughput paling drastis hingga mencapai 86.39 Mbps pada Ring-5 akibat ketidakmampuan beradaptasi dengan pembatasan bandwidth dinamis. Temuan ini menegaskan pentingnya representasi bobot link dinamis pada pengendali SDN untuk menjamin efisiensi perutean.

**Kata Kunci**: Software-Defined Networking, OpenFlow, A\*, Bellman-Ford, Widest Path.
