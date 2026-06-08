# 4.8 Kesimpulan dan Saran

## 4.8.1 Kesimpulan

Berdasarkan hasil rancangan, pengujian, dan analisis data kuantitatif terhadap 3.900 baris data eksperimen di bawah 7 skenario kegagalan pada topologi Ring-5 dan Jellyfish, proyek akhir ini menyimpulkan hal-hal berikut:

1.  **Keberhasilan Implementasi Pengendali Modular**: Arsitektur pengendali SDN SPF berbasis OS-Ken berhasil diimplementasikan secara modular menggunakan pola *template method*, di mana kelas induk `base_controller.py` menangani seluruh mekanisme OpenFlow 1.3 (deteksi topologi LLDP, pembelajaran MAC, instalasi *flow rule*, dan rerouting otomatis), sementara ketiga subclass algoritmik (A\*, Bellman-Ford, Widest Path) hanya mengimplementasikan fungsi `compute_path()`. Modularitas ini memungkinkan penggantian algoritme routing secara instan tanpa mengubah kode penanganan protokol OpenFlow.

2.  **Terlaksananya Testbed Otomatis dengan Data yang Valid**: Skrip otomatisasi pengujian `benchmark_core.py` berhasil mengeksekusi 7 skenario kegagalan secara mandiri pada dua topologi dan tiga algoritme, mengumpulkan total 3.900 baris data metrik QoS yang valid dan siap dianalisis. Dari total tersebut, 3.511 baris (90.0%) tercatat sebagai pengujian sukses dan 389 baris (10.0%) sebagai error yang semuanya berasal dari skenario *switch_down* dan *link_down_during_traffic* dengan penyebab yang telah teridentifikasi.

3.  **Peringkat Komposit dan Rekomendasi Algoritme**: Berdasarkan evaluasi kuantitatif, Bellman-Ford menempati peringkat komposit pertama di kedua topologi (skor 0.8000) terutama karena keuntungan tidak disengaja dari anomali *bypass throttling*. Jika anomali tersebut dikeluarkan dari pertimbangan, A\* menjadi pilihan algoritmik yang paling seimbang: A\* mencatatkan runtime komputasi tercepat pada topologi kompleks Jellyfish (0.0749 ms, lebih cepat 20.5% dari Bellman-Ford) dengan hop count optimal yang identik, menjadikannya pilihan terbaik untuk jaringan SDN produksi yang mengutamakan kecepatan konvergensi. Widest Path menempati posisi terbawah karena ketergantungan kritis pada data kapasitas tautan statis yang tidak mencerminkan kondisi jaringan dinamis.

---

## 4.8.2 Keterbatasan

Proyek akhir ini memiliki beberapa keterbatasan teknis yang perlu diperhatikan dalam menafsirkan hasilnya:

1.  **Ketiadaan Monitoring Bandwidth Dinamis**: Ketiga pengendali mengandalkan file konfigurasi statis `link_weights.json` untuk mengetahui kapasitas tautan, sehingga tidak dapat mendeteksi perubahan kapasitas aktual di switch secara real-time. Keterbatasan ini secara langsung menyebabkan anomali *bypass throttling* yang mendistorsi peringkat komposit akhir.

2.  **Kondisi Lalu Lintas Homogen**: Pengujian hanya melibatkan lalu lintas data TCP iperf3 *single-flow* antara satu pasangan host pada satu waktu, tanpa *background traffic*. Kondisi ini tidak merepresentasikan beban jaringan nyata dengan banyak aliran data yang bersaing secara bersamaan, sehingga hasil throughput kemungkinan lebih optimis dari kondisi produksi.

3.  **Skala Topologi Terbatas**: Evaluasi hanya mencakup topologi berukuran kecil (5 switch Ring-5 dan 10 switch Jellyfish). Keunggulan runtime A\* berkat mekanisme *pruning* heuristik kemungkinan akan jauh lebih signifikan pada topologi berukuran lebih besar (50-100 switch), namun hal ini belum diverifikasi dalam proyek ini.

---

## 4.8.3 Saran

Berdasarkan keterbatasan yang diidentifikasi, berikut adalah dua rekomendasi utama untuk pengembangan proyek serupa di masa depan:

1.  **Implementasi Monitoring Bandwidth Dinamis via OpenFlow**: Menambahkan modul pemantauan statistik port menggunakan pesan OpenFlow `OFPPortStatsRequest` yang dikirim secara berkala (misalnya setiap 2-5 detik) ke setiap switch. Data statistik yang diterima (byte terkirim, paket drop, error) dapat digunakan untuk menghitung utilisasi bandwidth aktual dan memperbarui matriks biaya rute secara dinamis di controller. Perubahan ini akan mengeliminasi mismatch antara representasi biaya statis dan kondisi jaringan fisik yang dinamis, khususnya menghapus anomali bypass throttling yang memengaruhi validitas peringkat komposit.

2.  **Pengembangan Perutean Multipath dengan Fast Failover**: Mengembangkan modul controller agar dapat menghitung dan menyimpan beberapa jalur terpisah secara fisik (*node-disjoint paths*) menggunakan algoritme Suurballe atau Yen's K-Shortest sebelum terjadi kegagalan. Dengan menyimpan jalur cadangan (*backup path*) di memori controller, switch dapat langsung mengaktifkan jalur alternatif saat mendeteksi kegagalan tautan melalui OpenFlow *Port-Status*, tanpa harus menunggu siklus deteksi LLDP dan rekalkulasi jalur penuh. Pendekatan *fast failover* ini diperkirakan dapat mengurangi retransmisi TCP pada skenario *link flap* dari rata-rata 17.283 menjadi mendekati nol.
