# 4.3 Pendahuluan

> [!TIP]
> **PANDUAN UMUM PENDAHULUAN (Skor Maksimal: 5/5):**
> *   **Panjang**: Total panjang bab Pendahuluan berkisar **1–2 halaman** (sekitar 500–800 kata).
> *   **Gaya Bahasa**: Gunakan Bahasa Indonesia akademis, objektif, dan formal.
> *   **Struktur sub-bab**: Wajib memuat sub-bab Latar Belakang (4.3.1), Tujuan Proyek (4.3.2), Ruang Lingkup (4.3.3), dan Sistematika Laporan (4.3.4) tanpa ada yang terlewat.

---

## 4.3.1 Latar Belakang

> [!IMPORTANT]
> **PETUNJUK PENULISAN LATAR BELAKANG:**
> *   Jelaskan **mengapa perutean Shortest Path First (SPF) dinamis penting** dalam jaringan komputer, terutama dalam mengatasi rigiditas (kekakuan) jaringan tradisional.
> *   Perkenalkan konsep **Software-Defined Networking (SDN)** sebagai solusi pemisahan *control plane* dan *data plane* yang memungkinkan pemrograman rute secara terpusat.
> *   Jelaskan **mengapa topik komparasi performa dan resiliensi A\*, Bellman-Ford, dan Widest Path relevan** untuk dipelajari pada topologi yang berbeda (melingkar Ring-5 vs acak regular Jellyfish).
> *   Gunakan metode deduktif (dari umum ke khusus): Jaringan Komputer $\rightarrow$ Masalah Routing Tradisional $\rightarrow$ Solusi SDN $\rightarrow$ Kebutuhan Komparasi Algoritme SPF Dinamis $\rightarrow$ Pernyataan Masalah Proyek.

### [TEMPLAT DRAFT LATAR BELAKANG]
Perkembangan teknologi jaringan komputer menuntut tingkat efisiensi, skalabilitas, dan keandalan yang semakin tinggi. Pada arsitektur jaringan tradisional, keputusan perutean dilakukan secara terdistribusi di setiap router menggunakan protokol statis atau dinamis konvensional seperti OSPF dan RIP. Pendekatan terdistribusi ini membatasi visibilitas jaringan secara global, memperlambat proses konvergensi saat terjadi kegagalan tautan (*link failure*), dan mempersulit rekayasa lalu lintas (*traffic engineering*).

Software-Defined Networking (SDN) hadir sebagai paradigma baru dengan memisahkan bidang kontrol (*control plane*) dan bidang data (*data plane*). Melalui perantara pengendali terpusat (*SDN controller*), administrator memiliki visibilitas global atas seluruh topologi jaringan dan dapat menginstruksikan switch bidang data untuk memasang aturan aliran (*flow rules*) secara dinamis melalui protokol standar seperti OpenFlow. Fleksibilitas ini memungkinkan implementasi berbagai algoritme perutean *Shortest Path First* (SPF) secara dinamis langsung dari pengendali.

Namun, efektivitas komputasi jalur terpendek sangat dipengaruhi oleh karakteristik algoritme routing yang digunakan serta bentuk fisik topologi jaringan. Terdapat perbedaan signifikan dalam cara pencarian rute: algoritme A\* memanfaatkan estimasi heuristik jarak untuk memangkas pencarian, Bellman-Ford melakukan relaksasi iteratif untuk menangani cost link dinamis, sedangkan Widest Path berfokus pada minimalisasi hambatan bandwidth (*bottleneck*). Performa dan resiliensi dari ketiga algoritme ini perlu diuji pada topologi teratur Ring-5 yang memiliki redundansi jalur terbatas dan topologi acak regular Jellyfish yang memiliki redundansi tinggi, di bawah berbagai gangguan fisik seperti pemutusan link, fluktuasi tautan, pembatasan bandwidth, dan kegagalan switch. Komparasi kuantitatif ini penting untuk menentukan algoritme terbaik yang dapat mempertahankan kinerja jaringan SDN di berbagai kondisi gangguan.

---

## 4.3.2 Tujuan Proyek

> [!IMPORTANT]
> **PETUNJUK PENULISAN TUJUAN PROYEK:**
> *   Nyatakan secara spesifik apa yang ingin dicapai melalui proyek ini.
> *   **Maksimal 3 tujuan** yang harus bersifat **terukur** (*measurable*).
> *   Gunakan kata kerja aktif operasional (seperti *mengimplementasikan*, *membangun*, *menganalisis*, *membandingkan*).

### [TEMPLAT TUJUAN PROYEK]
Tujuan utama yang ingin dicapai dari proyek akhir ini adalah:
1.  **Mengimplementasikan Pengendali SDN SPF Modular**: Mengembangkan aplikasi pengendali berbasis OS-Ken yang mampu menghitung jalur secara dinamis dan independen menggunakan tiga algoritme perutean (A\*, Bellman-Ford, dan Widest Path) dengan memanfaatkan satu berkas kelas dasar pengendali (`base_controller.py`).
2.  **Membangun Testbed Pengujian Otomatis**: Menyusun skrip simulasi Mininet terotomatisasi yang dapat menguji ketahanan (*resilience*) jaringan di bawah 7 skenario kegagalan link, fluktuasi tautan, pembatasan bandwidth, dan kegagalan switch.
3.  **Melakukan Evaluasi Kuantitatif dan Peringkat Komposit**: Menganalisis metrik-metrik performa utama (throughput, runtime, packet loss, TCP retransmits, hop count, dan recovery delta) berdasarkan 3.900 baris data eksperimen empiris untuk memberikan peringkat komposit performa algoritme pada masing-masing topologi.

---

## 4.3.3 Ruang Lingkup

> [!IMPORTANT]
> **PETUNJUK PENULISAN RUANG LINGKUP & BATASAN:**
> *   Uraikan ruang lingkup teknologi yang digunakan (emulator Mininet, controller OS-Ken, OpenFlow 1.3).
> *   Sebutkan secara spesifik topologi jaringan yang digunakan (Ring-5 dengan 5 switch dan 10 host, Jellyfish dengan 10 switch dan 10 host).
> *   Sebutkan metrik-metrik yang diukur (Throughput, Runtime Komputasi Jalur, Packet Loss, TCP Retransmissions, Hop Count).
> *   Sebutkan batasan/limitasi proyek (misalnya: bobot link statis dibaca dari file JSON, tidak adanya monitoring dinamis utilitas port stats secara real-time, evaluasi dibatasi pada lalu lintas data iperf3 TCP tunggal).

### [TEMPLAT RUANG LINGKUP & BATASAN]
Eksperimen dalam proyek akhir ini dibatasi oleh ruang lingkup dan batasan sebagai berikut:
1.  **Infrastruktur Emulasi**: Menggunakan emulator Mininet v2.3+ untuk mereplikasi data plane dengan switch berbasis Open vSwitch (OVS) dan protokol komunikasi OpenFlow 1.3.
2.  **Kerangka Pengendali**: Bidang kontrol dikelola menggunakan kerangka kerja pengendali OS-Ken (Python 3).
3.  **Topologi Jaringan**: Evaluasi dibatasi pada dua jenis topologi, yaitu Ring-5 (5 switch melingkar, 10 host) dan Jellyfish (10 switch acak regular, 10 host).
4.  **Algoritme Routing**: Algoritme yang dievaluasi mencakup pencarian rute terpendek A\*, Bellman-Ford, dan Widest Path, serta BFS untuk *flooding spanning tree*.
5.  **Metrik Evaluasi**: Data yang dianalisis mencakup *throughput* TCP (iperf3), runtime pencarian jalur (milidetik), *packet loss* (pingall), *retransmisi* TCP, *hop count* rute terpilih, dan *recovery throughput delta*.
6.  **Batasan Proyek**: Pembaruan kapasitas link aktual oleh controller bersifat statis dan dibaca dari file konfigurasi `link_weights.json` secara offline, tanpa adanya mekanisme permintaan statistik port (`OFPPortStatsRequest`) secara berkala dan dinamis dari switch OpenFlow.

---

## 4.3.4 Sistematika Laporan

> [!IMPORTANT]
> **PETUNJUK PENULISAN SISTEMATIKA LAPORAN:**
> *   Uraikan secara ringkas dan runtut alur pembahasan di setiap bab berikutnya (Bab Landasan Teori, Metodologi, Implementasi, Hasil dan Analisis, serta Kesimpulan).

### [TEMPLAT SISTEMATIKA LAPORAN]
Sistematika penulisan laporan proyek akhir ini dibagi menjadi beberapa bab utama sebagai berikut:
*   **Bab 4.1 & 4.2 Halaman Judul dan Abstrak**: Memuat identitas proyek, penulis, dosen pengampu, serta ringkasan eksekutif penelitian.
*   **Bab 4.3 Pendahuluan**: Menjelaskan latar belakang permasalahan perutean dinamis, tujuan proyek yang terukur, ruang lingkup pengujian, serta batasan sistem yang dibangun.
*   **Bab 4.4 Landasan Teori**: Memaparkan landasan ilmiah mengenai Software-Defined Networking, mekanisme OpenFlow, teori dasar dan kompleksitas algoritme A\*, Bellman-Ford, dan Widest Path, serta pemetaan topologi Ring-5 dan Jellyfish.
*   **Bab 4.5 Metodologi**: Merinci alur perancangan eksperimen, konfigurasi parameter link topologi, serta prosedur terperinci pengumpulan data untuk menjamin replikasi penelitian.
*   **Bab 4.6 Implementasi**: Memaparkan integrasi controller OS-Ken dengan repositori learn_sdn, cuplikan kode modifikasi penanganan Packet-In dan rerouting dinamis, serta kendala teknis yang dihadapi.
*   **Bab 4.7 Hasil dan Analisis**: Menyajikan grafik hasil ekspor data-driven dari Jupyter Notebook serta melakukan analisis perbandingan performa, resiliensi, dan pembahasan anomali routing.
*   **Bab 4.8 Kesimpulan dan Saran**: Merangkum pencapaian tujuan proyek berdasarkan bukti kuantitatif, keterbatasan sistem, serta rekomendasi pengembangan modul QoS dinamis di masa depan.
*   **Bab 4.9 & 4.10 Daftar Pustaka dan Lampiran**: Menyajikan daftar literatur referensi IEEE dan lampiran data summary statistics lengkap serta kontribusi anggota kelompok.
