# 4.8 Kesimpulan dan Saran

> [!TIP]
> **PANDUAN PENULISAN KESIMPULAN DAN SARAN (Skor Maksimal: 5/5):**
> *   **Panjang**: Total wajib dibatasi maksimal **1 halaman** (sekitar 300–400 kata) agar padat dan fokus pada inti capaian.
> *   **Bukti data**: Di bagian kesimpulan, jangan hanya menulis kalimat normatif. Sebutkan secara singkat angka empiris dari hasil analisis sebagai bukti tercapainya tujuan.
> *   **Keselarasan**: Pastikan poin-poin kesimpulan menjawab secara langsung tujuan proyek yang ditulis di bab Pendahuluan (4.3.2).

---

## 4.8.1 Kesimpulan

> [!IMPORTANT]
> **PETUNJUK PENULISAN KESIMPULAN:**
> *   Ulas ketercapaian ketiga tujuan proyek:
>     1.  *Tercapainya tujuan 1*: Suksesnya pembuatan controller modular OS-Ken dengan kelas induk `base_controller.py` dan subclass algoritmik.
>     2.  *Tercapainya tujuan 2*: Terlaksananya testbed 7 skenario pada Mininet dengan 3.900 data point terkumpul.
>     3.  *Tercapainya tujuan 3*: Hasil komparasi kuantitatif dan peringkat komposit (menyebutkan peringkat #1 Bellman-Ford di Ring-5 dan Jellyfish, keunggulan runtime A* di Jellyfish, serta degradasi throughput Widest Path).

### [TEMPLAT DRAFT KESIMPULAN]
Berdasarkan hasil rancangan, pengujian, dan analisis data kuantitatif yang dilakukan, kesimpulan proyek akhir ini adalah:
1.  **Keberhasilan Implementasi Pengendali Modular**: Arsitektur pengendali SDN SPF berbasis OS-Ken telah sukses dibangun secara modular. Pemisahan kelas induk `base_controller.py` dan subclass algoritmik terbukti mempermudah penggantian algoritme routing (A\*, Bellman-Ford, atau Widest Path) secara instan tanpa perlu memodifikasi kode penanganan pesan OpenFlow dasar.
2.  **Terlaksananya Testbed Otomatisasi**: Skrip otomatisasi pengujian `run_live_scenarios.py` berhasil mengeksekusi 7 skenario gangguan pada topologi Ring-5 dan Jellyfish secara mandiri, mengumpulkan total 3.900 baris data metrik QoS (throughput, runtime, packet loss, retransmits, hop count, dan recovery delta) secara valid dan siap dianalisis.
3.  **Peringkat Komposit Algoritme**: Evaluasi kuantitatif menunjukkan bahwa Bellman-Ford menduduki peringkat #1 pada kedua topologi dengan skor komposit 0.8000 karena diuntungkan oleh anomali *bypass throttling* di Ring-5 (mempertahankan 95.03 Mbps) akibat pembacaan bobot statis sebagai cost. Sementara itu, A\* mencatatkan runtime tercepat pada topologi Jellyfish sebesar **0.0749 ms** dengan hop count optimal, sedangkan Widest Path menempati posisi terbawah karena keterbatasan data kapasitas link statis yang memicu degradasi throughput hingga **86.39 Mbps** pada Ring-5.

---

## 4.8.2 Keterbatasan

> [!IMPORTANT]
> **PETUNJUK PENULISAN KETERBATASAN:**
> *   Sebutkan secara jujur keterbatasan sistem yang dibangun, misalnya:
>     1.  Ketergantungan controller pada file konfigurasi link statis (`link_weights.json`) untuk mengetahui bandwidth link, sehingga tidak responsif terhadap degradasi link dinamis di data plane.
>     2.  Testbed dibatasi pada lalu lintas data TCP iperf3 tunggal (single-flow) antar-host tanpa adanya background traffic yang padat.

### [TEMPLAT DRAFT KETERBATASAN]
Proyek akhir ini memiliki beberapa batasan dan keterbatasan teknis:
1.  **Ketiadaan QoS Monitoring Real-Time**: Pengendali dinamis yang diimplementasikan masih sangat bergantung pada file konfigurasi eksternal statis `link_weights.json` untuk mengetahui bobot link, sehingga controller tidak dapat mendeteksi degradasi kapasitas bandwidth fisik aktual di switch secara real-time.
2.  **Kondisi Trafik Homogen**: Pengujian ketahanan hanya melibatkan lalu lintas data *single-flow* iperf3 antar satu pasangan host aktif pada satu waktu, sehingga belum mengevaluasi performa algoritme di bawah beban lalu lintas multi-user yang padat (*background network traffic*).

---

## 4.8.3 Saran

> [!IMPORTANT]
> **PETUNJUK PENULISAN SARAN:**
> *   Usulkan **1–2 ide pengembangan lanjutan** yang konkret untuk mengatasi keterbatasan di atas, misalnya:
>     1.  Mengintegrasikan dynamic link monitoring dengan mengirim request pesan statistik port `OFPPortStatsRequest` ke switch OpenFlow untuk menghitung utilisasi bandwidth real-time.
>     2.  Mengembangkan perutean multipath dinamis menggunakan algoritme Suurballe atau Yen's K-Shortest Path untuk mempersiapkan jalur cadangan (backup path) sebelum terjadi kegagalan tautan (*fast failover*).

### [TEMPLAT DRAFT SARAN]
Untuk pengembangan proyek serupa di masa depan, disarankan beberapa saran perbaikan sebagai berikut:
1.  **Implementasi Pengukuran Bandwidth Dinamis**: Menambahkan modul pemantauan port statistik menggunakan pesan standard OpenFlow `OFPPortStatsRequest` secara berkala (misalnya setiap 2 detik) untuk mengkalkulasi utilisasi bandwidth aktual di switch secara dinamis, sehingga matriks biaya rute diperbarui secara real-time.
2.  **Penerapan Rerouting Multipath (Fast Failover)**: Mengembangkan modul perutean agar dapat menghitung beberapa rute terpisah secara fisik (*node-disjoint paths*) menggunakan algoritme Suurballe, sehingga switch dapat langsung memindahkan paket ke jalur cadangan saat terjadi gangguan link tanpa harus memicu event Packet-In ke controller.
