# 3. Latar Belakang

> [!TIP]
> **PANDUAN RUBRIK PENILAIAN - KRITERIA 1 (Skor Maksimal: 5/5):**
> Untuk mendapatkan nilai maksimal, penjelasan latar belakang dan tujuan proyek akhir tidak boleh bersifat teoretis umum. Anda harus menjelaskan:
> 1. Urgensi peralihan dari arsitektur jaringan tradisional ke Software-Defined Networking (SDN) dari sudut pandang fleksibilitas kontrol perutean.
> 2. Permasalahan nyata mengapa perbandingan algoritma dinamis SPF (*Shortest Path First*) sangat krusial pada topologi yang heterogen dan rentan kegagalan (*link failure*).
> 3. Tujuan kuantitatif proyek secara spesifik (apa saja metrik performa dan resiliensi yang diukur).

---

## 3.1 Permasalahan yang Diangkat
*Tuliskan latar belakang masalah yang melandasi proyek ini. Anda dapat mengembangkan poin-poin berikut:*
*   **Keterbatasan Arsitektur Jaringan Tradisional**: Pada jaringan konvensional, keputusan perutean dilakukan secara terdistribusi di masing-masing perangkat keras menggunakan protokol statis atau berbasis standar industri seperti OSPF/RIP. Hal ini membatasi visibilitas global jaringan dan menyulitkan konfigurasi kebijakan lalu lintas (*traffic engineering*) yang fleksibel.
*   **Keunggulan Jaringan SDN**: Dengan pemisahan antara bidang kontrol (*control plane*) dan bidang data (*data plane*), Software-Defined Networking (SDN) memungkinkan kontrol terpusat yang dinamis atas seluruh infrastruktur jaringan menggunakan aplikasi pengendali (*controller*).
*   **Tantangan Algoritma SPF Kontemporer**: Terdapat berbagai algoritma untuk komputasi jalur terpendek (SPF), seperti Dijkstra (paling umum), **A\*** (berbasis heuristik), **Bellman-Ford** (berbasis relaksasi yang mendukung nilai biaya negatif), dan **Widest Path** (memaksimalkan bandwidth bottleneck untuk QoS). Namun, performa komparatif dan resiliensi dari algoritma-algoritma ini jarang dievaluasi secara langsung dalam satu *testbed* yang sama di bawah skenario kegagalan link, fluktuasi (*link flap*), atau pembatasan kapasitas (*bandwidth throttling*).
*   **Heterogenitas Topologi**: Performa algoritma bervariasi tergantung pada kompleksitas dan struktur topologi jaringan. Oleh karena itu, diperlukan perbandingan performa pada topologi teratur melingkar (**Ring-5**) yang memiliki jalur redundansi terbatas, dan topologi acak regular (**Jellyfish**) yang menyajikan tingkat redundansi jalur yang tinggi.

---

## 3.2 Tujuan dari Proyek
*Tuliskan tujuan spesifik proyek akhir Anda. Berikut draf tujuan yang selaras dengan codebase:*
1.  **Mengimplementasikan Pengendali SDN Modular**: Membangun aplikasi Ryu Controller yang mendukung komputasi jalur dinamis secara terpisah untuk algoritma A*, Bellman-Ford, dan Widest Path menggunakan OpenFlow 1.3.
2.  **Membangun Testbed Pengujian Otomatis**: Menyusun skrip simulasi Mininet terotomatisasi untuk menguji resiliensi algoritma di bawah 7 skenario kegagalan:
    *   *Baseline* (kondisi normal tanpa gangguan).
    *   *Link Down Before Traffic* (pemutusan link sebelum lalu lintas dimulai).
    *   *Link Down During Traffic* (pemutusan link secara dinamis di tengah transfer data).
    *   *Link Flap* (kombinasi link mati dan hidup kembali secara berkala).
    *   *Switch Down* (kegagalan fisik node/perangkat switch).
    *   *Bandwidth Throttle* (pembatasan dinamis kapasitas link).
    *   *Random Link Down* (kegagalan link acak khusus topologi Jellyfish).
3.  **Melakukan Evaluasi Kuantitatif Secara Kritis**: Menganalisis metrik-metrik performa utama melalui pemrosesan Jupyter Notebook:
    *   **Throughput (Mbps)**: Kapasitas lalu lintas yang dicapai aliran data.
    *   **Runtime Komputasi Jalur (ms)**: Waktu yang dibutuhkan controller untuk menemukan rute baru.
    *   **Packet Loss (%)**: Persentase paket yang hilang akibat gangguan jaringan.
    *   **Retransmisi TCP**: Jumlah retransmisi paket akibat kegagalan jalur.
    *   **Hop Count**: Jumlah lompatan switch pada rute terpilih.
    *   **Failure Recovery Delta (%)**: Mengukur seberapa cepat dan efisien sistem memulihkan throughput pasca-gangguan.
4.  **Menyusun Peringkat Algoritma Berdasarkan Skor Komposit**: Menentukan algoritma terbaik yang paling optimal untuk masing-masing tipe topologi (Ring-5 dan Jellyfish) guna memberikan rekomendasi desain perutean dinamis.
