# 4.7 Hasil dan Analisis

## 4.7.1 Presentasi Data

Seluruh visualisasi dan tabel data di bawah ini dihasilkan secara otomatis oleh Jupyter Notebook `plot_results_executed_final.ipynb` yang dieksekusi dengan parameter `max_pairs=20` dan `repetitions=5`.

### Ringkasan Metrik Rata-Rata Keseluruhan per Algoritme dan Topologi

Tabel berikut menyajikan ringkasan rata-rata metrik utama dari seluruh skenario pengujian yang berhasil (`status=success`):

| Topologi | Algoritme | Mean Throughput (Mbps) | Mean Runtime (ms) | Mean Hop Count | Success Rate | Skor Komposit |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **Jellyfish** | Bellman-Ford | 93.79 | 0.0942 | 1.75 | 89.43% | **0.8000** |
| | A\* | 93.35 | 0.0749 | 1.75 | 89.29% | 0.7046 |
| | Widest Path | 91.49 | 0.0846 | 2.25 | 89.29% | 0.0991 |
| **Ring-5** | Bellman-Ford | 95.03 | 0.0517 | 1.45 | 90.83% | **0.8000** |
| | A\* | 88.04 | 0.0526 | 1.45 | 90.83% | 0.2897 |
| | Widest Path | 86.39 | 0.0909 | 1.65 | 90.83% | 0.0000 |

*Catatan: Skor komposit dihitung menggunakan normalisasi Min-Max dengan bobot: Throughput (40%), Runtime (20%), Success Rate (20%), dan Stabilitas Throughput/Std (20%).*

---

### Gambar 4.1: Perbandingan Throughput Rata-Rata per Skenario dan Topologi

![Rata-Rata Throughput per Skenario](../../img/analysis/throughput_by_topology.png)

*Gambar 4.1: Perbandingan throughput rata-rata (Mbps) ketiga algoritme pada setiap skenario kegagalan untuk topologi Jellyfish (kiri) dan Ring-5 (kanan). Sumbu-x menunjukkan nama skenario dan sumbu-y menunjukkan throughput dalam Mbps.*

**Interpretasi:** Pada kondisi *baseline* (tanpa gangguan), ketiga algoritme menunjukkan performa throughput yang hampir identik di kedua topologi, berkisar antara 94.90 hingga 95.28 Mbps, mendekati batas kapasitas tautan 100 Mbps pada emulasi Mininet. Anomali paling mencolok terjadi pada skenario *Bandwidth Throttle* di Ring-5: A\* turun ke **56.70 Mbps** dan Widest Path turun drastis ke **48.11 Mbps**, sementara Bellman-Ford tetap stabil di **94.95 Mbps**. Pada topologi Jellyfish, dampak *bandwidth throttle* lebih kecil karena tersedia lebih banyak jalur alternatif, dengan Widest Path hanya turun ke **82.37 Mbps**.

---

### Gambar 4.2: Distribusi Runtime Komputasi Jalur

![Distribusi Runtime Komputasi Jalur](../../img/analysis/runtime_distribution.png)

*Gambar 4.2: Distribusi runtime komputasi jalur (ms) dalam skala logaritma menggunakan *box plot*. Setiap kotak mewakili interkuartil (IQR) distribusi runtime, dengan titik-titik menunjukkan pencilan (outlier).*

**Interpretasi:** A\* memiliki median runtime paling rendah dan distribusi paling sempit pada topologi Jellyfish (rata-rata 0.0749 ms), menunjukkan konsistensi tinggi dalam kecepatan komputasi. Bellman-Ford lebih kompetitif di Ring-5 (0.0517 ms vs A\* 0.0526 ms) karena jumlah switch yang kecil (hanya 5) membatasi jumlah iterasi relaksasi. Widest Path memiliki *outlier* runtime yang signifikan, terutama pada skenario *Link Down During Traffic* di Ring-5 (0.2700 ms), menandakan bahwa perubahan topologi saat transmisi aktif memperlambat re-komputasi jalur pada algoritme berbasis *max-heap* ini.

---

### Gambar 4.3: Analisis Ketahanan terhadap Kegagalan (*Failure Recovery*)

![Dampak Kegagalan terhadap Throughput](../../img/analysis/failure_recovery_analysis.png)

*Gambar 4.3: Rata-rata throughput pada tiga fase pengujian: *Baseline* (tanpa gangguan), *Pre-Failure* (sebelum kegagalan), dan *During-Failure* (saat kegagalan). Perbedaan tinggi bar menunjukkan besar delta throughput akibat kegagalan.*

**Interpretasi:** Perbandingan delta throughput antar-fase mengungkap perbedaan resiliensi yang signifikan antar-algoritme:

| Topologi | Algoritme | Delta *During-Failure* | Delta *Pre-Failure* |
| :--- | :--- | :---: | :---: |
| **Jellyfish** | A\* | -6.73% | +0.10% |
| | Bellman-Ford | -5.10% | -0.05% |
| | Widest Path | -6.24% | -3.94% |
| **Ring-5** | A\* | -0.37% | -16.59% |
| | Bellman-Ford | +0.14% | +0.19% |
| | Widest Path | -0.61% | -20.23% |

Bellman-Ford menunjukkan resiliensi terbaik di Ring-5, bahkan mencatatkan delta positif (+0.14%) pada fase *during* karena perilaku *bypass throttling*. A\* dan Widest Path mengalami penurunan besar pada fase *pre* di Ring-5 (masing-masing -16.59% dan -20.23%) akibat skenario *bandwidth throttle* yang membatasi link utama `s1-s2`.

---

### Gambar 4.4: Analisis Retransmisi TCP

![TCP Retransmissions](../../img/analysis/retransmits_analysis.png)

*Gambar 4.4: Total retransmisi TCP per algoritme dan skenario kegagalan pada masing-masing topologi. Skenario dengan nilai tinggi menunjukkan instabilitas koneksi yang lebih besar.*

**Interpretasi:** Skenario *Link Flap* menghasilkan retransmisi TCP tertinggi pada kedua topologi. Pada Jellyfish, A\* mencatatkan hingga **17.283 retransmisi** dan Widest Path mencapai **16.231 retransmisi**, jauh melebihi skenario lainnya. Penyebabnya adalah siklus *link mati dan hidup kembali* yang memicu pembersihan (*flush*) dan pemasangan ulang *flow rule* secara berulang, selama jeda konvergensi mana paket TCP yang aktif di-*drop* dan harus di-*retransmit*. Sebaliknya, skenario *Switch Down* hanya menghasilkan 0-4 retransmisi karena koneksi langsung terputus total tanpa sempat melakukan retransmisi, dan iperf3 segera melaporkan kegagalan.

---

### Gambar 4.5: Perbandingan Hop Count Rata-Rata

![Hop Count Comparison](../../img/analysis/hop_count_comparison.png)

*Gambar 4.5: Rata-rata hop count per algoritme dan topologi. Bar yang lebih tinggi menunjukkan jalur yang dipilih lebih panjang (lebih banyak switch yang dilewati).*

**Interpretasi:** A\* dan Bellman-Ford menghasilkan rata-rata hop count yang identik: **1.75 pada Jellyfish** dan **1.45 pada Ring-5**, karena keduanya berorientasi meminimalkan jarak rute. Widest Path secara konsisten mencatatkan hop count lebih tinggi: **2.25 pada Jellyfish** dan **1.65 pada Ring-5**. Perbedaan ini selaras dengan tujuan Widest Path yang mengoptimalkan *bottleneck bandwidth*, bukan meminimalkan jumlah hop, sehingga sering memilih jalur memutar yang lebih panjang asalkan memiliki kapasitas tautan minimum yang lebih besar.

---

## 4.7.2 Analisis Perbandingan

Analisis komparatif dari data eksperimen mengungkap korelasi yang kuat antara teori algoritmik dan performa jaringan aktual:

**1. Evaluasi Throughput Jaringan**

Pada kondisi *baseline* tanpa gangguan, ketiga algoritme menunjukkan throughput yang hampir identik (94.90-95.28 Mbps) karena semuanya menemukan jalur terpendek yang setara pada topologi tanpa hambatan. Perbedaan throughput yang signifikan baru muncul pada skenario *bandwidth throttle*, di mana kemampuan (atau ketidakmampuan) algoritme menghindari tautan yang terdegradasi menjadi faktor penentu utama. Bellman-Ford unggul secara kebetulan karena penggunaan bandwidth sebagai *cost*, sedangkan A\* dan Widest Path yang beroperasi berdasarkan data statis mengalami degradasi signifikan.

**2. Efisiensi Waktu Komputasi (Runtime)**

Sesuai dengan teori kompleksitas waktu, A\* menunjukkan keunggulan runtime yang jelas pada topologi kompleks Jellyfish (0.0749 ms vs Bellman-Ford 0.0942 ms, selisih 25.7%). Hal ini terjadi karena heuristik *reverse-BFS* A\* secara efektif memangkas eksplorasi node yang tidak relevan pada graf berukuran lebih besar (10 switch Jellyfish). Menariknya, pada topologi Ring-5 yang kecil (5 switch), Bellman-Ford sedikit lebih cepat (0.0517 ms vs A\* 0.0526 ms), karena overhead komputasi heuristik awal A\* di Python melebihi biaya relaksasi sederhana Bellman-Ford pada graf sangat kecil.

**3. Efisiensi Jalur (Hop Count)**

A\* dan Bellman-Ford secara konsisten menemukan rute terpendek dengan hop count identik (1.75 pada Jellyfish, 1.45 pada Ring-5). Widest Path yang mengoptimalkan kapasitas *bottleneck* secara inheren menghasilkan hop count lebih tinggi (2.25 dan 1.65), mengorbankan efisiensi jarak demi optimasi bandwidth. Hop count yang lebih tinggi pada Widest Path juga berarti lebih banyak *flow entries* yang harus dipasang di switch, sedikit meningkatkan konsumsi memori TCAM.

---

## 4.7.3 Pembahasan Temuan

Eksperimen mengungkap tiga temuan anomali yang secara akademis penting untuk dianalisis:

**Temuan 1: Anomali Bypass Throttling Bellman-Ford di Ring-5**

Pada skenario *Bandwidth Throttle* di Ring-5, Bellman-Ford mencatatkan throughput stabil sebesar **94.95 Mbps**, sementara A\* turun ke **56.70 Mbps** dan Widest Path turun ke **48.11 Mbps**. Akar penyebabnya adalah desain pengendali Bellman-Ford yang membaca nilai kapasitas bandwidth dari `link_weights.json` dan memperlakukannya sebagai *biaya jalur* (cost) secara langsung. Akibatnya, tautan `s1-s2` dengan bandwidth terdaftar 1000 Mbps memiliki cost 1000 (sangat mahal), sedangkan jalur alternatif `s1-s5-s4-s3-s2` memiliki total cost hanya 103. Bellman-Ford secara otomatis memilih jalur alternatif yang lebih murah ini, yang secara tidak sengaja menghindari tautan yang sedang dibatasi fisik oleh Mininet menjadi 10 Mbps. Perilaku ini menunjukkan bahwa **pemilihan representasi bobot link** (cost vs kapasitas) pada algoritme perutean memiliki dampak yang jauh melampaui sekadar pilihan teknis, dan dapat menghasilkan performa yang sangat berbeda dalam kondisi kegagalan tertentu.

**Temuan 2: Isolasi Node pada Kegagalan Switch Down**

Skenario `switch_down` menghasilkan *success rate* yang rendah sebesar **45% (45/100 pengujian)** untuk semua algoritme di kedua topologi, tanpa perbedaan antar-algoritme. Hal ini membuktikan bahwa kegagalan tersebut bukan disebabkan oleh kekurangan algoritme routing, melainkan oleh keterbatasan fisik topologi: ketika switch dimatikan, semua host yang terhubung langsung ke switch tersebut kehilangan koneksi fisik ke jaringan secara total. Tidak ada jalur fisik alternatif yang dapat menghubungkan host-host tersebut, sehingga iperf3 gagal sepenuhnya. Temuan ini menegaskan bahwa skenario *switch down* lebih menguji **ketahanan topologi** terhadap kegagalan node daripada kualitas algoritme routing itu sendiri.

**Temuan 3: Tingginya Retransmisi TCP pada Link Flap**

Skenario *link flap* memicu peningkatan retransmisi TCP yang sangat signifikan, mencapai **17.283 retransmisi** pada A\* di topologi Jellyfish. Pola ini terjadi karena siklus *link mati-hidup* memaksa pengendali melakukan dua siklus rerouting penuh dalam satu sesi iperf3 (5 detik): pertama saat link mati (detik ke-1), dan kedua saat link hidup kembali (detik ke-3). Selama setiap jeda konvergensi, paket TCP yang sudah dalam perjalanan di-*drop* oleh switch karena tidak ada flow rule yang valid, memaksa protokol TCP untuk melakukan retransmisi masif. Temuan ini menegaskan pentingnya meminimalkan waktu konvergensi pengendali, terutama untuk aplikasi yang sensitif terhadap keterlambatan seperti streaming video atau layanan real-time.
