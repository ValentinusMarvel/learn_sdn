# 7. Kesimpulan Proyek Akhir

Bab ini merangkum seluruh hasil evaluasi proyek akhir, menganalisis kendala-kendala teknis yang dihadapi selama implementasi, dan menawarkan rekomendasi pengembangan lanjutan untuk meningkatkan kualitas perutean dinamis pada jaringan SDN.

---

## 7.1 Ringkasan Hasil yang Dicapai
*Tuliskan ringkasan dari hasil analisis performa komposit Anda. Berikut draf ringkasan yang selaras dengan temuan pengujian:*
*   **Keunggulan Pemulihan Jalur Dinamis**: Seluruh algoritma (A*, Bellman-Ford, dan Widest Path) berhasil mendemonstrasikan resiliensi terhadap kegagalan link dinamis (`link_down_during_traffic` dan `link_flap`) dengan mengalihkan jalur lalu lintas data secara otomatis lewat kontrol terpusat Ryu.
*   **Pemenang Peringkat Performa Komposit**: Algoritma **Bellman-Ford** secara kuantitatif menempati peringkat **#1** di kedua topologi (Skor: 0.7641 pada Jellyfish dan 0.8000 pada Ring-5). Hal ini disebabkan oleh perilaku bypass throttling bandwidth yang tak sengaja akibat controller Bellman-Ford memperlakukan bandwidth statis link sebagai "biaya/cost" jalur, sehingga ia menghindari link bandwidth tinggi `s1-s2` (cost 1000) yang sedang dibatasi.
*   **Efisiensi Runtime A\***: Algoritma **A\*** terbukti memiliki runtime komputasi jalur terpendek yang sangat cepat (khususnya pada topologi Jellyfish dengan rata-rata komputasi **0.0566 ms** dibanding Widest Path sebesar **0.2600 ms**). Penggunaan heuristik estimasi jarak hop reverse-BFS secara efektif membatasi jumlah node graf yang diperiksa.
*   **Kelemahan Widest Path**: Widest Path menempati peringkat **terbawah** karena ketergantungannya pada data statis kapasitas link di `link_weights.json`. Ketika terjadi pembatasan bandwidth fisik secara dinamis di Mininet, controller Widest Path yang tidak mengetahui pembatasan tersebut tetap memilih jalur throttled karena mengira kapasitasnya masih 1000 Mbps.

---

## 7.2 Kendala yang Dihadapi
*Identifikasi beberapa tantangan teknis dalam proyek ini:*
1.  **Dinamika Keadaan Jaringan vs Cost Statis**: Controller Bellman-Ford dan Widest Path bersifat pasif dan hanya membaca konfigurasi kapasitas link dari file statis [link_weights.json](file:///c:/Users/anang/OneDrive/Documents/GitHub/learn_sdn/SPF/link_weights.json). Controller tidak memantau utilitas atau pembatasan bandwidth aktual secara dinamis pada control plane.
2.  **Masalah Skalabilitas OpenFlow Packet-In**: Penanganan rute pertama menggunakan mekanisme Packet-In memicu latensi komputasi awal di Ryu controller sebelum aturan flow dipasang di switch, yang dapat menjadi bottleneck apabila jumlah aliran data meningkat drastis.
3.  **Keterbatasan Simulasi di Mininet**: Beberapa skenario kegagalan switch (`switch_down`) memotong koneksi fisik host secara mutlak ke switch tujuan, sehingga menghasilkan error transmisi data yang tidak dapat dipulihkan oleh algoritma routing mana pun karena ketiadaan jalur alternatif fisik.

---

## 7.3 Pengembangan Lanjutan yang Dapat Dilakukan
*Sediakan saran pengembangan di masa mendatang untuk mendapatkan nilai tambah akademis:*
1.  **Implementasi Dynamic Link Monitoring (QoS Dinamis)**:
    Menambahkan fitur *link monitoring* di Ryu controller menggunakan modul OpenFlow `OFPPortStatsRequest`. Pengendali harus meminta statistik port secara berkala dari switch untuk menghitung utilisasi bandwidth aktual, latensi, dan packet loss secara real-time, lalu memperbarui matriks cost secara dinamis.
2.  **Integrasi ECMP (Equal-Cost Multipath)**:
    Mengembangkan controller agar mendukung distribusi lalu lintas data secara paralel pada jalur-jalur alternatif yang memiliki bobot/biaya yang sama guna menghindari overload pada satu link tertentu.
3.  **Penggunaan Algoritma Multipath (Suurballe & Yen's K-Shortest)**:
    Mengganti skema perutean single-path ke perutean multipath menggunakan algoritma Suurballe atau Yen untuk menghitung jalur cadangan (*backup path*) yang terpisah secara fisik (*node-disjoint*) sebelum terjadi kegagalan link, guna mempercepat waktu konvergensi (*fast failover*).
