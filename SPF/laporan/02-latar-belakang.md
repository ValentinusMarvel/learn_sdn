# 3. Latar Belakang

---

## 3.1 Permasalahan yang Diangkat

Pada jaringan konvensional, keputusan perutean dilakukan secara terdistribusi di masing-masing perangkat keras menggunakan protokol statis atau berbasis standar industri seperti OSPF (*Open Shortest Path First*) dan RIP (*Routing Information Protocol*). Pendekatan ini memiliki sejumlah keterbatasan fundamental:

1.  **Keterbatasan Visibilitas Global**: Setiap router hanya memiliki pengetahuan lokal tentang topologi jaringan di sekitarnya. Hal ini menyulitkan konfigurasi kebijakan lalu lintas (*traffic engineering*) yang fleksibel dan optimal secara keseluruhan jaringan.
2.  **Kekakuan Konfigurasi**: Perubahan kebijakan perutean pada jaringan tradisional memerlukan konfigurasi manual per perangkat. Dalam lingkungan pusat data modern yang dinamis, proses ini menjadi sangat lambat dan rentan terhadap kesalahan manusia (*human error*).
3.  **Respons Kegagalan yang Lambat**: Protokol perutean terdistribusi memerlukan waktu konvergensi yang signifikan (detik hingga menit) untuk menyesuaikan tabel routing saat terjadi kegagalan link atau switch, sehingga menyebabkan *downtime* dan kehilangan paket data yang tidak dapat diterima.

**Software-Defined Networking (SDN)** menawarkan solusi fundamental atas permasalahan tersebut melalui pemisahan bidang kontrol (*control plane*) dari bidang data (*data plane*). Dengan arsitektur SDN, sebuah pengendali terpusat (*controller*) memiliki visibilitas global atas seluruh topologi jaringan dan dapat memasang aturan aliran (*flow rules*) secara dinamis ke setiap switch menggunakan protokol standar OpenFlow. Hal ini memungkinkan pengambilan keputusan perutean yang cerdas, responsif, dan dapat diprogram secara langsung melalui perangkat lunak.

Namun, meskipun SDN memberikan fleksibilitas kontrol yang tinggi, **pemilihan algoritma perutean yang optimal** tetap menjadi tantangan terbuka. Terdapat berbagai algoritma untuk komputasi jalur terpendek (*Shortest Path First* — SPF), seperti:

*   **A\*** — algoritma pencarian heuristik yang memangkas ruang pencarian menggunakan estimasi jarak (*admissible heuristic*), sehingga berpotensi lebih cepat dibanding pencarian lengkap pada graf berukuran besar.
*   **Bellman-Ford** — algoritma berbasis relaksasi iteratif yang mendukung bobot link negatif. Algoritma ini menerapkan prinsip *dynamic programming* untuk menemukan jalur terpendek secara global.
*   **Widest Path** — algoritma modifikasi Dijkstra yang memaksimalkan *bottleneck bandwidth* pada jalur terpilih, sehingga cocok untuk skenario *Quality of Service* (QoS) yang memprioritaskan kapasitas throughput.

Performa komparatif dan resiliensi dari ketiga algoritma ini jarang dievaluasi secara langsung dalam satu *testbed* yang sama, terlebih di bawah skenario kegagalan link, fluktuasi (*link flap*), atau pembatasan kapasitas (*bandwidth throttling*). Selain itu, performa algoritma juga bervariasi tergantung pada kompleksitas dan struktur topologi jaringan. Topologi teratur melingkar (**Ring-5**) yang memiliki jalur redundansi terbatas (hanya 2 jalur antar-node) akan menunjukkan karakteristik yang sangat berbeda dengan topologi acak regular (**Jellyfish**) yang menyajikan tingkat redundansi jalur yang lebih tinggi.

Permasalahan inilah yang melandasi proyek akhir ini: **bagaimana performa dan resiliensi dari tiga algoritma perutean SPF (A\*, Bellman-Ford, dan Widest Path) jika dibandingkan secara kuantitatif pada jaringan SDN dengan dua topologi berbeda di bawah berbagai skenario kegagalan?**

---

## 3.2 Tujuan dari Proyek

Proyek akhir ini memiliki empat tujuan spesifik yang terukur:

1.  **Mengimplementasikan Pengendali SDN Modular**: Membangun aplikasi pengendali OS-Ken (sebagai fork modern dari Ryu Controller) yang mendukung komputasi jalur dinamis secara terpisah untuk algoritma A*, Bellman-Ford, dan Widest Path menggunakan protokol OpenFlow 1.3. Arsitektur didesain secara modular dengan `base_controller.py` sebagai kelas induk dan tiga subclass algoritmik yang masing-masing hanya perlu mengimplementasikan fungsi `compute_path()`.

2.  **Membangun Testbed Pengujian Otomatis**: Menyusun skrip simulasi Mininet terotomatisasi (`run_live_scenarios.py`) yang mampu menguji resiliensi ketiga algoritma di bawah **7 skenario kegagalan**:
    *   *Baseline No Failure* — kondisi normal tanpa gangguan sebagai acuan performa dasar.
    *   *Link Down Before Traffic* — pemutusan link statis sebelum lalu lintas dimulai.
    *   *Link Down During Traffic* — pemutusan link dinamis di tengah transfer data aktif.
    *   *Link Flap* — kombinasi link mati dan hidup kembali secara berkala untuk menguji stabilitas konvergensi.
    *   *Switch Down* — kegagalan total sebuah node/switch fisik.
    *   *Bandwidth Throttle* — pembatasan dinamis kapasitas link dari 1000 Mbps ke 10 Mbps.
    *   *Random Link Down (Jellyfish)* — kegagalan link acak khusus topologi Jellyfish untuk menguji adaptasi pada topologi dengan redundansi tinggi.

3.  **Melakukan Evaluasi Kuantitatif Secara Kritis**: Menganalisis metrik-metrik performa utama melalui pemrosesan data menggunakan Jupyter Notebook dengan parameter pengujian `max_pairs=20` dan `repetitions=5` (total **3.900 baris data** — 2.100 baris Jellyfish + 1.800 baris Ring-5):
    *   **Throughput (Mbps)** — kapasitas lalu lintas TCP yang dicapai oleh aliran data iperf3.
    *   **Runtime Komputasi Jalur (ms)** — waktu yang dibutuhkan controller untuk menghitung rute baru.
    *   **Packet Loss (%)** — persentase paket yang hilang akibat kegagalan jalur pingall.
    *   **Retransmisi TCP** — jumlah retransmisi paket TCP sebagai indikator kegagalan jalur sementara.
    *   **Hop Count** — jumlah lompatan switch pada rute terpilih sebagai indikator efisiensi jalur.
    *   **Failure Recovery Delta (%)** — mengukur persentase penurunan throughput relatif terhadap baseline saat terjadi gangguan.

4.  **Menyusun Peringkat Algoritma Berdasarkan Skor Komposit**: Menentukan algoritma terbaik yang paling optimal untuk masing-masing tipe topologi (Ring-5 dan Jellyfish) berdasarkan skor komposit ternormalisasi (0.0 hingga 1.0) yang menggabungkan seluruh metrik performa, guna memberikan rekomendasi desain perutean dinamis berbasis data empiris.
