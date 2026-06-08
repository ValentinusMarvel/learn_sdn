# 4.7 Hasil dan Analisis

> [!TIP]
> **PANDUAN PENULISAN HASIL DAN ANALISIS (Skor Maksimal: 5/5):**
> *   **Panjang**: Berkisar antara **3–4 halaman** (sekitar 1.200–1.800 kata).
> *   **Integrasi Gambar**: Gunakan path relatif (`../../img/analysis/`) agar gambar visualisasi grafis ter-render dengan benar. Pastikan setiap gambar memiliki nomor gambar, judul, dan keterangan analisis di bawahnya.
> *   **Akurasi Data**: Gunakan data kuantitatif eksak dari keluaran Jupyter Notebook final untuk topologi Ring-5 dan Jellyfish (meliputi throughput, runtime, hop count, success rate, dan recovery delta).

---

## 4.7.1 Presentasi Data

> [!IMPORTANT]
> **PETUNJUK PRESENTASI DATA:**
> *   Sajikan tabel rangkuman rata-rata metrik (seperti throughput, runtime, dan hop count) untuk A*, Bellman-Ford, dan Widest Path pada kedua topologi.
> *   Tampilkan visualisasi grafis utama yang diekspor oleh notebook:
>     1.  *Throughput rata-rata per skenario* (throughput_by_topology.png)
>     2.  *Distribusi runtime komputasi rute* (runtime_distribution.png)
>     3.  *Ketahanan terhadap kegagalan* (failure_recovery_analysis.png)
>     4.  *TCP Retransmissions* (retransmits_analysis.png)
>     5.  *Rata-rata hop count* (hop_count_comparison.png)

### [TEMPLAT DRAFT PRESENTASI DATA]

Berikut adalah visualisasi rata-rata throughput TCP yang diperoleh dari hasil emulasi iperf3 pada kedua topologi di bawah seluruh skenario gangguan:

![Rata-Rata Throughput per Skenario](../../img/analysis/throughput_by_topology.png)
*Gambar 4.1: Perbandingan Throughput Rata-Rata (Mbps) per Topologi dan Skenario Gangguan*

Distribusi waktu komputasi jalur (*runtime*) dalam skala logaritma disajikan pada Gambar 4.2:

![Distribusi Runtime Komputasi Jalur](../../img/analysis/runtime_distribution.png)
*Gambar 4.2: Distribusi Runtime Komputasi Jalur (ms) per Algoritme dan Topologi*

Untuk mengevaluasi dampak transient loss saat terjadi pemutusan link di tengah-tengah transmisi, Gambar 4.3 menampilkan rata-rata throughput pada fase baseline, pre-failure, dan during-failure:

![Dampak Kegagalan terhadap Throughput](../../img/analysis/failure_recovery_analysis.png)
*Gambar 4.3: Analisis Ketahanan Throughput Delta pada Fase Transien Kegagalan*

Selain itu, stabilitas lapisan transportasi dinilai melalui jumlah retransmisi TCP (Gambar 4.4) dan efisiensi rute dinilai melalui hop count rata-rata (Gambar 4.5):

![TCP Retransmissions](../../img/analysis/retransmits_analysis.png)
*Gambar 4.4: Total Retransmisi TCP per Algoritme dan Skenario Gangguan*

![Hop Count Comparison](../../img/analysis/hop_count_comparison.png)
*Gambar 4.5: Rata-Rata Hop Count per Algoritme dan Topologi*

Rangkuman metrik komparatif keseluruhan disajikan dalam tabel pivot di bawah ini:

| Topologi | Algoritme | Mean Throughput (Mbps) | Mean Runtime (ms) | Success Rate | Hop Count (Rata-rata) |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **Jellyfish** | A\* | 93.35 | 0.0749 | 89.29% | 1.75 |
| | Bellman-Ford | 93.79 | 0.0942 | 89.43% | 1.75 |
| | Widest Path | 91.49 | 0.0846 | 89.29% | 2.25 |
| **Ring-5** | A\* | 88.04 | 0.0526 | 90.83% | 1.45 |
| | Bellman-Ford | 95.03 | 0.0517 | 90.83% | 1.45 |
| | Widest Path | 86.39 | 0.0909 | 90.83% | 1.65 |

---

## 4.7.2 Analisis Perbandingan

> [!IMPORTANT]
> **PETUNJUK ANALISIS PERBANDINGAN:**
> *   Bahas perbedaan hasil performa antar-algoritme dan hubungkan dengan teori serta kompleksitas waktunya.
> *   **Perbandingan Throughput**: Jelaskan performa throughput pada skenario baseline (semua algo stabil di ~95 Mbps mendekati kapasitas link 100 Mbps).
> *   **Perbandingan Runtime**: Bahas mengapa A* secara konsisten paling cepat pada topologi kompleks Jellyfish (0.0749 ms vs Bellman-Ford 0.0942 ms) berkat pruning heuristik, sedangkan di Ring-5 yang sangat kecil Bellman-Ford bersaing ketat (0.0517 ms vs A* 0.0526 ms) karena overhead kalkulasi heuristik A* melampaui relaksasi sederhana Ring-5.
> *   **Perbandingan Hop Count**: Jelaskan mengapa Widest Path mencatatkan hop count lebih tinggi (2.25 pada Jellyfish, 1.65 pada Ring-5) dibanding A*/Bellman-Ford (1.75 dan 1.45) karena Widest Path mengoptimalkan kapasitas bottleneck bukan meminimalkan jarak lompatan.

### [TEMPLAT DRAFT ANALISIS KOMPARATIF]
Analisis komparatif dari data eksperimen mengungkapkan korelasi yang kuat antara teori algoritmik dan performa jaringan aktual:

1.  **Evaluasi Throughput Jaringan**:
    Pada kondisi baseline tanpa gangguan, seluruh algoritme menunjukkan kinerja throughput TCP yang optimal, yaitu berkisar antara **94.90–95.51 Mbps** di kedua topologi. Hal ini membuktikan bahwa bidang kontrol OpenFlow 1.3 dapat melayani instalasi flow aturan aliran dengan baik tanpa mendegradasi kecepatan link fisik emulasi 100 Mbps.
2.  **Efisiensi Waktu Komputasi (Runtime)**:
    Sesuai dengan teori kompleksitas waktu, algoritme A\* menunjukkan keunggulan runtime yang jelas pada topologi Jellyfish dengan rata-rata **0.0749 ms** dibandingkan Bellman-Ford (**0.0942 ms**). Perilaku ini terjadi karena A\* menggunakan heuristik estimasi jarak *reverse-BFS* untuk memandu arah pencarian dan memotong eksplorasi node graf yang tidak relevan. Menariknya, pada topologi Ring-5 yang sangat kecil (hanya 5 switch), Bellman-Ford mencatatkan runtime rata-rata yang sedikit lebih cepat (**0.0517 ms**) daripada A\* (**0.0526 ms**). Hal ini dapat dijelaskan karena overhead komputasi fungsi heuristik awal A\* di Python lebih besar daripada biaya komputasi relaksasi rute linear sederhana Bellman-Ford pada graf berukuran kecil.
3.  **Efisiensi Jalur (Hop Count)**:
    A\* dan Bellman-Ford secara konsisten menghasilkan rata-rata hop count yang identik (1.75 pada Jellyfish dan 1.45 pada Ring-5) karena keduanya berorientasi meminimalkan jarak rute secara mutlak. Sebaliknya, Widest Path mencatatkan hop count yang lebih tinggi (2.25 pada Jellyfish dan 1.65 pada Ring-5). Hal ini selaras dengan karakteristik Widest Path yang memodifikasi relaksasi untuk memaksimalkan kapasitas tautan terkecil (*bottleneck bandwidth*), sehingga sering kali memilih jalur memutar yang lebih panjang asalkan memiliki kapasitas link minimal yang lebih besar.

---

## 4.7.3 Pembahasan Temuan

> [!IMPORTANT]
> **PETUNJUK PEMBAHASAN TEMUAN & ANOMALI:**
> *   Bahas temuan anomali menarik yang tidak terduga dari eksperimen:
>     1.  **Anomali Throttling Ring-5**: Bellman-Ford tetap stabil di 95.03 Mbps sedangkan A* dan Widest Path drop ke 56.70 Mbps dan 86.39 Mbps. Jelaskan bias *bypass throttling* akibat representasi bandwidth statis sebagai cost pada Bellman-Ford.
>     2.  **Keterbatasan Switch Down**: Success rate jatuh ke 45% (error rate 55%) pada skenario switch_down di kedua topologi. Jelaskan isolasi host fisik karena hilangnya node switch akses.
>     3.  **TCP Retransmissions pada Link Flap**: Skenario link_flap memicu retransmisi TCP tertinggi karena osilasi rute dinamis (A* mencatatkan hingga 17.283 retransmisi di Jellyfish).

### [TEMPLAT DRAFT PEMBAHASAN ANOMALI]
Hasil eksperimen mengungkap beberapa anomali penting yang perlu dikritisi secara akademis:

1.  **Bias Bypass Throttling Bellman-Ford di Ring-5**:
    *   *Temuan*: Pada skenario Bandwidth Throttle di Ring-5, Bellman-Ford mencatatkan throughput konstan **95.03 Mbps**, sementara A\* turun tajam ke **56.70 Mbps** dan Widest Path turun ke **86.39 Mbps** (rata-rata keseluruhan **86.39 Mbps** untuk Widest Path).
    *   *Analisis*: Pengendali Bellman-Ford membaca kapasitas bandwidth dari `link_weights.json` dan secara tidak sengaja memperlakukannya sebagai *biaya jalur* (cost). Akibatnya, link dengan bandwidth 1000 Mbps dianggap memiliki cost 1000 (sangat mahal), sehingga Bellman-Ford secara alami menghindari link `s1-s2` tersebut. Link `s1-s2` inilah yang justru di-throttle oleh Mininet menjadi 10 Mbps. Karena Bellman-Ford sudah menghindari link tersebut sejak awal, kinerjanya tidak terpengaruh oleh throttling. Sebaliknya, A\* dan Widest Path yang memilih rute terpendek dan rute terlebar statis melewati link `s1-s2` mengalami degradasi throughput yang parah karena link tersebut dibatasi kapasitasnya secara dinamis tanpa diketahui oleh controller. Hal ini menunjukkan bahwa pemetaan bobot link (cost vs kapasitas) sangat krusial dalam desain perutean SDN.
2.  **Isolasi Node pada Kegagalan Switch Down**:
    *   *Temuan*: Skenario `switch_down` menghasilkan tingkat kesuksesan (*success rate*) yang rendah sebesar **45%** (dan tingkat error **55%**) pada semua algoritme di kedua topologi.
    *   *Analisis*: Ketika switch s1 dimatikan, semua host yang terhubung langsung ke switch s1 (host h1 dan h2 pada Ring-5) kehilangan koneksi fisik ke jaringan secara total. Kegagalan iperf3 pada skenario ini bukan disebabkan oleh kesalahan algoritme perutean dalam mencari jalan, melainkan karena ketiadaan jalur fisik alternatif akibat host terisolasi dari infrastruktur.
3.  **Tingginya Retransmisi TCP pada Link Flap**:
    *   *Temuan*: Skenario fluktuasi tautan (`link_flap`) memicu peningkatan retransmisi TCP yang sangat signifikan, mencapai puncaknya pada algoritme A\* sebanyak **17.283 retransmisi** di topologi Jellyfish.
    *   *Analisis*: Siklus dinamis link mati dan hidup kembali memicu pembersihan (*flush*) flow rule secara berulang oleh pengendali. Selama jeda waktu konvergensi dan pemasangan rute baru, paket TCP yang sedang dikirim aktif mengalami kehilangan (*drop*), memaksa protokol transport untuk melakukan retransmisi secara masif guna menjaga keutuhan data.
