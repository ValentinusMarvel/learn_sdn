# 4.3 Pendahuluan

## 4.3.1 Latar Belakang

Perkembangan teknologi jaringan komputer menuntut tingkat efisiensi, skalabilitas, dan keandalan yang semakin tinggi. Pada arsitektur jaringan tradisional, keputusan perutean dilakukan secara terdistribusi di setiap router menggunakan protokol statis atau dinamis konvensional seperti OSPF (*Open Shortest Path First*) dan RIP (*Routing Information Protocol*). Pendekatan terdistribusi ini membatasi visibilitas jaringan secara global, memperlambat proses konvergensi saat terjadi kegagalan tautan (*link failure*), dan mempersulit rekayasa lalu lintas (*traffic engineering*) yang membutuhkan pengendalian rute secara terpusat [1].

*Software-Defined Networking* (SDN) hadir sebagai paradigma baru dengan memisahkan bidang kontrol (*control plane*) dan bidang data (*data plane*) secara tegas. Melalui pengendali terpusat (*SDN controller*), administrator memiliki visibilitas global atas seluruh topologi jaringan dan dapat menginstruksikan switch bidang data untuk memasang aturan aliran (*flow rules*) secara dinamis melalui protokol standar OpenFlow [1]. Fleksibilitas ini membuka peluang untuk mengimplementasikan berbagai algoritme perutean *Shortest Path First* (SPF) secara terprogram langsung dari pengendali, sesuatu yang tidak mungkin dilakukan pada jaringan tradisional tanpa mengganti firmware perangkat keras.

Namun, efektivitas komputasi jalur terpendek sangat dipengaruhi oleh dua faktor: karakteristik algoritme routing yang digunakan dan bentuk fisik topologi jaringan tempat algoritme tersebut dijalankan. Terdapat perbedaan mendasar dalam cara ketiga algoritme utama mencari rute: algoritme A\* memanfaatkan estimasi heuristik jarak untuk memangkas pencarian secara terarah [5]; Bellman-Ford melakukan relaksasi iteratif yang mampu menangani cost link heterogen [6]; sedangkan Widest Path berfokus pada maksimalisasi kapasitas minimum di sepanjang jalur (*bottleneck bandwidth*) [7]. Performa dan resiliensi ketiga algoritme ini perlu diuji secara empiris pada topologi yang berbeda. Topologi Ring-5 mewakili arsitektur teratur dengan redundansi jalur terbatas, sementara topologi Jellyfish mewakili arsitektur jaringan pusat data modern (*data center network*) yang memiliki redundansi tinggi dan jalur alternatif yang melimpah [2].

Komparasi kuantitatif ini penting untuk memberikan panduan empiris bagi insinyur jaringan dalam memilih algoritme perutean yang paling sesuai dengan karakteristik topologi dan kebutuhan *Quality of Service* (QoS) di lingkungan SDN produksi.

---

## 4.3.2 Tujuan Proyek

Tujuan utama yang ingin dicapai dari proyek akhir ini adalah:

1.  **Mengimplementasikan Pengendali SDN SPF Modular**: Mengembangkan aplikasi pengendali berbasis OS-Ken yang mampu menghitung jalur secara dinamis menggunakan tiga algoritme perutean (A\*, Bellman-Ford, dan Widest Path) dengan arsitektur satu kelas induk (`base_controller.py`) dan tiga subclass algoritmik yang dapat dipertukarkan.
2.  **Membangun Testbed Pengujian Otomatis**: Menyusun skrip simulasi Mininet terotomatisasi yang dapat menguji ketahanan (*resilience*) jaringan di bawah 7 skenario kegagalan, mencakup pemutusan link, fluktuasi tautan, pembatasan bandwidth, dan kegagalan switch total, dengan parameter `max_pairs=20` dan `repetitions=5`.
3.  **Melakukan Evaluasi Kuantitatif dan Peringkat Komposit**: Menganalisis metrik-metrik performa utama (throughput, runtime, packet loss, TCP retransmits, hop count, dan recovery delta) berdasarkan 3.900 baris data eksperimen empiris untuk memberikan peringkat komposit performa algoritme pada masing-masing topologi.

---

## 4.3.3 Ruang Lingkup

Eksperimen dalam proyek akhir ini dibatasi oleh ruang lingkup dan batasan sebagai berikut:

1.  **Infrastruktur Emulasi**: Menggunakan emulator Mininet v2.3+ untuk mereplikasi *data plane* dengan switch berbasis Open vSwitch (OVS) dan protokol komunikasi OpenFlow 1.3 [2].
2.  **Kerangka Pengendali**: Bidang kontrol dikelola menggunakan kerangka kerja pengendali OS-Ken (Python 3), yaitu fork aktif dan terawat dari controller Ryu yang tidak lagi dikembangkan [3].
3.  **Topologi Jaringan**: Evaluasi dibatasi pada dua jenis topologi, yaitu Ring-5 (5 switch melingkar, 10 host, 2 host per switch) dan Jellyfish (10 switch acak regular dengan seed 42, 10 host).
4.  **Algoritme Routing**: Algoritme yang dievaluasi mencakup A\*, Bellman-Ford, dan Widest Path sebagai algoritme perutean utama, serta BFS untuk pembangunan *broadcast spanning tree*.
5.  **Metrik Evaluasi**: Data yang dianalisis mencakup throughput TCP (iperf3 [4]), runtime pencarian jalur (milidetik), packet loss (pingall), retransmisi TCP, hop count rute terpilih, dan recovery throughput delta.
6.  **Batasan Proyek**: Pembaruan kapasitas link aktual oleh controller bersifat statis dan dibaca dari file konfigurasi `link_weights.json` secara *offline*, tanpa mekanisme permintaan statistik port (`OFPPortStatsRequest`) secara berkala. Evaluasi juga dibatasi pada lalu lintas data iperf3 TCP tunggal antar satu pasangan host aktif pada satu waktu (*single-flow*), tanpa *background traffic*.

---

## 4.3.4 Sistematika Laporan

Laporan proyek akhir ini disusun dengan sistematika sebagai berikut:

*   **Bab 4.1 dan 4.2 (Halaman Judul dan Abstrak)**: Memuat identitas proyek, daftar anggota kelompok, dosen pengampu, serta ringkasan eksekutif penelitian yang mencakup topik, metode, dan dua temuan utama.
*   **Bab 4.3 (Pendahuluan)**: Menjelaskan latar belakang permasalahan perutean dinamis pada SDN, tiga tujuan proyek yang terukur, ruang lingkup pengujian beserta batasannya, serta sistematika laporan ini.
*   **Bab 4.4 (Landasan Teori)**: Memaparkan dasar ilmiah mengenai mekanisme OpenFlow, teori dasar dan kompleksitas algoritme A\*, Bellman-Ford, dan Widest Path, karakteristik topologi Ring-5 dan Jellyfish, serta definisi metrik QoS yang digunakan.
*   **Bab 4.5 (Metodologi)**: Merinci alur perancangan eksperimen dengan 7 skenario kegagalan, konfigurasi parameter link topologi, cuplikan kode inisialisasi topologi aktual, serta prosedur terperinci pengumpulan data yang memungkinkan replikasi penelitian.
*   **Bab 4.6 (Implementasi)**: Memaparkan struktur modular repositori `learn_sdn`, tabel pemetaan berkas implementasi, cuplikan kode kritis mekanisme *Packet-In* dan *Flow-Mod*, serta diagram arsitektur sistem, dan kendala teknis yang dihadapi beserta solusinya.
*   **Bab 4.7 (Hasil dan Analisis)**: Menyajikan delapan grafik hasil ekspor Jupyter Notebook dengan interpretasi analitik per gambar, tabel pivot ringkasan metrik per skenario, analisis perbandingan algoritme, dan pembahasan tiga anomali utama yang ditemukan.
*   **Bab 4.8 (Kesimpulan dan Saran)**: Merangkum pencapaian tiga tujuan proyek berdasarkan bukti kuantitatif, mengidentifikasi keterbatasan sistem, dan memberikan rekomendasi pengembangan modul QoS dinamis serta perutean multipath.
*   **Bab 4.9 dan 4.10 (Daftar Pustaka dan Lampiran)**: Menyajikan delapan daftar literatur referensi dalam format IEEE dan lampiran yang memuat enam tabel data ringkasan performa, deskripsi repositori kode, serta matriks kontribusi anggota kelompok.
