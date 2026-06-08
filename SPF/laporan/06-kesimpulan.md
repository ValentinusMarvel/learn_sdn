# 7. Kesimpulan Proyek Akhir

Bab ini merangkum seluruh hasil evaluasi kuantitatif proyek akhir, mengidentifikasi kendala-kendala teknis yang dihadapi selama implementasi dan pengujian, serta menawarkan rekomendasi pengembangan lanjutan untuk meningkatkan kualitas perutean dinamis pada jaringan SDN.

---

## 7.1 Ringkasan Hasil yang Dicapai

Berdasarkan analisis terhadap **3.900 baris data** eksperimen (2.100 Jellyfish + 1.800 Ring-5) dengan `max_pairs=20` dan `repetitions=5` di bawah 7 skenario kegagalan, proyek ini berhasil membuktikan beberapa temuan utama:

### A. Resiliensi Perutean Dinamis SDN

Seluruh algoritma (A*, Bellman-Ford, dan Widest Path) berhasil mendemonstrasikan **resiliensi terhadap kegagalan link dinamis**. Pada skenario `link_down_during_traffic` dan `link_flap`, controller OS-Ken secara otomatis mendeteksi perubahan topologi melalui LLDP, menghitung ulang jalur menggunakan algoritma terpilih, dan memasang flow baru ke switch, yang mana seluruh proses ini terjadi dalam hitungan milidetik. Penurunan throughput pada skenario kegagalan dinamis berkisar antara **–0.37%** (Bellman-Ford, Ring-5 during) hingga **–6.73%** (A*, Jellyfish during) dari baseline, menunjukkan kemampuan pemulihan yang sangat baik.

### B. Pemenang Peringkat Performa Komposit

Algoritma **Bellman-Ford** menempati peringkat **#1** di kedua topologi dengan skor komposit:
*   **Jellyfish**: 0.8000 (throughput rata-rata 93.79 Mbps, runtime 0.0942 ms, success rate 89.43%)
*   **Ring-5**: 0.8000 (throughput rata-rata 95.03 Mbps, runtime 0.0517 ms, success rate 90.83%)

Namun, kemenangan ini perlu dikritisi secara akademis karena disebabkan oleh **perilaku bypass throttling yang tidak disengaja**: controller Bellman-Ford memperlakukan bandwidth statis dari `link_weights.json` sebagai *biaya jalur* (cost), sehingga ia menghindari link bandwidth tinggi `s1-s2` (cost 1000) yang justru sedang dibatasi oleh skenario bandwidth throttle. Perilaku ini menguntungkan Bellman-Ford secara tidak sengaja.

### C. Efisiensi Runtime Komputasi A*

Algoritma **A\*** terbukti memiliki **runtime komputasi jalur tercepat** secara konsisten pada topologi kompleks:
*   **Jellyfish**: rata-rata **0.0749 ms** (vs Bellman-Ford 0.0942 ms, Widest Path 0.0846 ms)
*   **Ring-5**: rata-rata **0.0526 ms** (vs Bellman-Ford 0.0517 ms, Widest Path 0.0909 ms)

Penggunaan heuristik estimasi jarak hop *reverse-BFS* secara efektif membatasi jumlah node graf yang diperiksa, menjadikan A* sebagai pilihan optimal untuk skenario di mana latensi komputasi jalur menjadi faktor kritis (misalnya pada topologi skala besar).

### D. Kelemahan Widest Path pada Skenario Bandwidth Throttle

Widest Path menempati peringkat **terbawah** di kedua topologi karena dua faktor utama:
1.  **Ketergantungan pada data statis kapasitas link**: Controller Widest Path membaca bandwidth dari `link_weights.json` dan memilih jalur dengan *bottleneck bandwidth* tertinggi. Ketika Mininet membatasi bandwidth fisik link `s1-s2` dari 1000 Mbps ke 10 Mbps, controller tidak mengetahui pembatasan tersebut dan tetap memilih jalur melalui link throttled karena mengira kapasitasnya masih 1000 Mbps.
2.  **Hop count lebih tinggi**: Rata-rata hop count Widest Path adalah **2.250** pada Jellyfish dan **1.650** pada Ring-5, lebih tinggi dibanding A*/Bellman-Ford (1.750 dan 1.450), karena algoritma ini mengoptimalkan bandwidth bukan jarak.

Akibatnya, throughput Widest Path turun drastis ke **48.12 Mbps** (–49.49%) pada Ring-5 bandwidth throttle, dan **82.37 Mbps** (–13.54%) pada Jellyfish bandwidth throttle.

### E. Statistik Data dan Error

| Metrik | Jellyfish | Ring-5 |
| :--- | :---: | :---: |
| Total baris data | 2.100 | 1.800 |
| Data sukses | 1.876 (89.3%) | 1.635 (90.8%) |
| Data error | 224 (10.7%) | 165 (9.2%) |
| Skenario diuji | 7 | 6 |
| Error rate tertinggi | switch_down: 55% | switch_down: 55% |

Seluruh error (389 baris) berasal dari skenario `link_down_during_traffic` dan `switch_down`. Penyebab error utama adalah "iperf3 JSON payload did not include bits_per_second", yang menunjukkan bahwa koneksi TCP gagal terbentuk karena jalur terputus total, bukan karena kegagalan algoritma routing.

---

## 7.2 Kendala yang Dihadapi

Selama implementasi dan pengujian proyek ini, beberapa kendala teknis signifikan ditemui:

1.  **Dinamika Keadaan Jaringan vs Cost Statis**: Controller Bellman-Ford dan Widest Path membaca konfigurasi kapasitas link dari file statis `link_weights.json` yang tidak diperbarui secara dinamis. Akibatnya, kedua controller ini tidak mengetahui perubahan kapasitas aktual saat terjadi bandwidth throttle di Mininet. Hal ini menyebabkan *mismatch* antara persepsi controller tentang kapasitas link dan kapasitas aktualnya.

2.  **Masalah Skalabilitas Packet-In**: Penanganan rute pertama menggunakan mekanisme *Packet-In* memicu latensi komputasi awal di controller OS-Ken sebelum flow dipasang di switch. Pada eksperimen dengan `max_pairs=20`, hal ini berarti **20 pasangan host × 2 arah = 40 kalkulasi jalur** harus dilakukan per skenario. Meskipun latensi per kalkulasi hanya ~0.05–0.27 ms, akumulasinya dapat menjadi bottleneck pada topologi yang jauh lebih besar.

3.  **Keterbatasan Simulasi Switch Down di Mininet**: Skenario `switch_down` memotong koneksi fisik host ke switch secara mutlak. Pada Ring-5 (5 switch, 2 host per switch), mematikan satu switch langsung menghilangkan **2 host** dari jaringan, menghasilkan success rate hanya **45%**, yang mana hal ini terjadi bukan karena kegagalan algoritma routing, melainkan karena ketiadaan jalur fisik alternatif menuju host yang terisolasi. Hal ini mengindikasikan bahwa skenario switch_down lebih menguji **topologi fisik** daripada **algoritma routing**.

4.  **Waktu Eksekusi Pengujian yang Panjang**: Dengan `max_pairs=20` dan `repetitions=5`, total eksekusi mencakup **3 algoritma × 2 topologi × 6–7 skenario × 20 pasangan × 5 repetisi = 3.900 tes individual**, masing-masing melibatkan inisialisasi Mininet, konvergensi topologi, transfer iperf3 5 detik, dan penangkapan pcap. Total waktu eksekusi memerlukan beberapa jam pada VM.

---

## 7.3 Pengembangan Lanjutan yang Dapat Dilakukan

Berdasarkan temuan dan keterbatasan proyek ini, berikut adalah beberapa rekomendasi pengembangan lanjutan yang dapat meningkatkan nilai akademis dan praktis sistem:

1.  **Implementasi Dynamic Link Monitoring (QoS Dinamis)**:
    Menambahkan fitur *link monitoring* di controller OS-Ken menggunakan modul OpenFlow `OFPPortStatsRequest`. Pengendali harus meminta statistik port secara berkala (misalnya setiap 1–5 detik) dari switch untuk menghitung utilisasi bandwidth aktual, latensi, dan packet loss secara *real-time*, lalu memperbarui matriks cost/kapasitas secara dinamis. Hal ini akan mengeliminasi masalah *static cost mismatch* yang ditemukan pada Bellman-Ford dan Widest Path.

2.  **Integrasi ECMP (Equal-Cost Multipath)**:
    Mengembangkan controller agar mendukung distribusi lalu lintas data secara paralel pada jalur-jalur alternatif yang memiliki bobot/biaya yang sama menggunakan OpenFlow SELECT Group. Hal ini berpotensi meningkatkan throughput agregat dan resiliensi terhadap kegagalan link tunggal, terutama pada topologi Jellyfish yang memiliki banyak jalur redundan.

3.  **Penggunaan Algoritma Multipath (Suurballe & Yen's K-Shortest)**:
    Mengganti skema perutean *single-path* ke perutean *multipath* menggunakan algoritma Suurballe atau Yen's K-Shortest untuk menghitung jalur cadangan (*backup path*) yang terpisah secara fisik (*node-disjoint*) sebelum terjadi kegagalan link. Pendekatan ini memungkinkan *fast failover* tanpa menunggu deteksi LLDP dan rekalkulasi jalur.

4.  **Evaluasi pada Topologi Skala Lebih Besar**:
    Menguji ketiga algoritma pada topologi dengan jumlah switch dan host yang lebih besar (misalnya 50–100 switch) untuk memvalidasi skalabilitas runtime komputasi jalur. Heuristik A* diharapkan menunjukkan keunggulan yang lebih signifikan pada topologi berukuran besar karena efek *pruning*-nya lebih terasa.

5.  **Instrumentasi dan Observabilitas**:
    Menambahkan *telemetry* dan *dashboarding* menggunakan Prometheus + Grafana untuk memonitor metrik controller secara real-time: jumlah Packet-In per detik, latensi kalkulasi jalur, jumlah flow entry aktif, dan status link. Hal ini akan memperkaya analisis dan memberikan visualisasi operasional yang lebih komprehensif.
