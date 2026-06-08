# BAB II LANDASAN TEORI

## 2.1 Algoritme yang Diuji

Komputasi rute dinamis pada graf topologi jaringan memanfaatkan beberapa algoritme pencarian jalur terpendek yang disesuaikan dengan kebutuhan optimasi masing-masing. Proyek ini mengimplementasikan empat algoritme berikut:

**1. Breadth-First Search (BFS)**

BFS melakukan penelusuran graf tingkat demi tingkat (*layer-by-layer*) mulai dari node akar, mengeksplorasi semua node tetangga pada kedalaman saat ini sebelum berpindah ke kedalaman berikutnya. Dalam konteks proyek ini, BFS tidak digunakan sebagai algoritme perutean utama, melainkan untuk dua fungsi kritis: membangun *broadcast spanning tree* guna mencegah *looping* paket ARP di *data plane*, serta menghitung estimasi jarak hop minimum (*heuristic*) yang digunakan oleh algoritme A\*. Kompleksitas waktu BFS adalah $O(V + E)$, di mana $V$ adalah jumlah switch dan $E$ adalah jumlah tautan fisik.

**2. Algoritme A\***

A\* adalah algoritme pencarian terarah (*informed search*) yang memperkirakan total biaya rute terkecil melalui setiap node $n$ menggunakan fungsi evaluasi $f(n) = g(n) + h(n)$ [5]. Variabel $g(n)$ merepresentasikan biaya aktual dari node sumber ke node $n$, sedangkan $h(n)$ adalah estimasi heuristik biaya tersisa dari node $n$ ke tujuan. Dalam implementasi proyek ini, fungsi heuristik $h(n)$ dihitung menggunakan jarak hop minimum dari tujuan ke setiap node via *reverse-BFS*, yang memastikan heuristik bersifat *admissible* (tidak pernah melebih-lebihkan biaya sebenarnya). Kompleksitas waktu A\* pada kasus rata-rata adalah $O(E \log V)$ menggunakan *priority queue*. Karakteristik utama A\* adalah efisiensinya karena mampu memangkas (*pruning*) eksplorasi node yang tidak mengarah ke tujuan, menjadikannya sangat unggul pada topologi dengan banyak node seperti Jellyfish.

**3. Algoritme Bellman-Ford**

Bellman-Ford menemukan jalur terpendek dari satu node sumber ke semua node lainnya melalui relaksasi bobot tautan secara iteratif sebanyak $V-1$ kali [6]. Pada setiap iterasi, algoritme memperbarui estimasi jarak terpendek ke setiap node jika ditemukan jalur alternatif yang lebih murah. Kompleksitas waktu Bellman-Ford adalah $O(V \times E)$, yang secara teoritis lebih lambat dari A\* pada graf besar. Namun, Bellman-Ford memiliki kelebihan menangani bobot tautan negatif dan kemampuan mendeteksi siklus berbobot negatif (*negative cycle*). Dalam implementasi proyek, pengendali Bellman-Ford membaca bobot tautan dari file konfigurasi `link_weights.json` dan menggunakannya secara langsung sebagai *biaya jalur* (cost), yang menciptakan perilaku unik yang dibahas lebih lanjut pada bab analisis.

**4. Algoritme Widest Path (*Bottleneck Routing*)**

Widest Path adalah modifikasi dari algoritme Dijkstra yang tujuannya bukan meminimalkan jarak, melainkan mencari jalur yang memaksimalkan *minimum bandwidth* (kapasitas terendah) di sepanjang rute [7]. Algoritme ini menggunakan *max-heap* sebagai antrean prioritas untuk selalu memilih node tetangga dengan *bottleneck bandwidth* terbesar. Kompleksitas waktu Widest Path adalah $O(E \log V)$, setara dengan A\*. Karakteristik utamanya adalah memprioritaskan kapasitas lalu lintas (*widest*) bukan jarak lompatan (*shortest*), yang secara langsung berpengaruh pada hop count yang lebih tinggi dibanding A\* dan Bellman-Ford.

---

## 2.2 Topologi Jaringan

Struktur fisik *data plane* SDN memiliki pengaruh signifikan terhadap performa perutean dan tingkat resiliensi jalur terhadap kegagalan tautan. Proyek ini membandingkan dua karakteristik topologi yang bertolak belakang untuk mengevaluasi adaptabilitas algoritme pada kondisi jaringan yang berbeda:

**1. Topologi Ring-5 (Melingkar Teratur)**

Topologi Ring-5 terdiri dari 5 switch yang saling terhubung membentuk lingkaran tertutup dengan pola hubungan s1-s2-s3-s4-s5-s1. Setiap switch terhubung langsung dengan 2 host akses, sehingga total terdapat 10 host dalam jaringan. Semua tautan inter-switch dikonfigurasi dengan bandwidth 100 Mbps dan delay 2 ms, memberikan dasar performa yang seragam. Topologi ini memiliki *node degree* inter-switch yang rendah dan konstan (degree 2), yang berarti setiap switch hanya memiliki tepat 2 jalur inter-switch untuk mencapai switch tetangganya.

Topologi Ring-5 dipilih karena mewakili arsitektur jaringan teratur dengan tingkat redundansi jalur yang sangat minim. Apabila satu tautan inter-switch putus, hanya tersisa tepat satu jalur memutar yang panjang untuk menghubungkan kedua ujung. Karakteristik ini menjadikannya sangat ideal untuk menguji batas ketahanan algoritme SPF pada skenario *single link failure*, di mana kemampuan rerouting dengan *hop count* seefisien mungkin sangat diuji.

**2. Topologi Jellyfish (Acak Regular)**

Topologi Jellyfish adalah arsitektur jaringan pusat data (*data center network*) berbasis graf acak $d$-regular. Setiap switch dihubungkan secara acak namun dengan *node degree* inter-switch yang seragam, menghasilkan jaringan dengan distribusi jalur yang lebih merata dibanding topologi hierarkis. Topologi Jellyfish pada proyek ini dibangun menggunakan 10 switch dengan 10 host, menggunakan generator seed acak 42 untuk menjamin replikabilitas topologi [2].

Topologi Jellyfish dipilih karena mewakili struktur jaringan pusat data modern berskala besar yang memiliki tingkat redundansi jalur sangat tinggi. Banyaknya jalur alternatif *multi-path* antar-node dengan panjang hop yang bervariasi memungkinkan evaluasi menyeluruh dari skalabilitas runtime algoritme SPF, fleksibilitas pengalihan rute dinamis saat terjadi kegagalan tautan majemuk, serta kemampuan adaptasi pada kondisi gangguan link acak yang tidak dapat diprediksi.

---

## 2.3 Metrik Evaluasi

Untuk menilai efisiensi dan ketahanan algoritme perutean secara objektif dan terukur, enam metrik evaluasi didefinisikan sebagai berikut:

**1. Throughput (Mbps)**

Throughput adalah laju transfer data aktual yang berhasil dikirimkan melalui saluran komunikasi dalam periode waktu tertentu. Pada proyek ini, throughput diukur menggunakan aliran data iperf3 TCP selama 5 detik [4]. Throughput tinggi menunjukkan bahwa rute yang dipilih oleh algoritme memiliki kualitas tautan yang baik, sedikit kehilangan paket, dan tidak melewati titik kemacetan (*congestion point*). Throughput merupakan metrik utama penilaian kepuasan pengguna layanan jaringan.

**2. Runtime Komputasi Jalur (ms)**

Runtime adalah waktu yang diperlukan oleh pengendali OS-Ken untuk memproses fungsi komputasi algoritme SPF, mulai dari saat menerima permintaan *Packet-In* hingga menghasilkan daftar jalur rute yang lengkap. Runtime yang rendah sangat penting untuk meminimalkan *routing delay* awal saat koneksi pertama dibentuk dan untuk mempercepat konvergensi pemulihan saat terjadi kegagalan.

**3. Packet Loss (%)**

Packet loss adalah persentase paket data yang hilang selama transmisi, akibat tautan yang sedang *down* atau timeout konvergensi pengendali. Pada proyek ini, packet loss diukur melalui perintah `pingall` sebelum setiap sesi iperf3 dijalankan. Packet loss tinggi menandakan kegagalan deteksi tautan atau keterlambatan konvergensi rute pengendali.

**4. TCP Retransmissions**

TCP Retransmissions adalah jumlah paket TCP yang harus dikirim ulang oleh host pengirim karena paket sebelumnya tidak menerima konfirmasi (*ACK*) dari penerima dalam batas waktu *Retransmission Timeout* (RTO). Retransmisi tinggi mengindikasikan adanya instabilitas koneksi atau fluktuasi tautan yang terjadi selama transmisi data aktif, seperti pada skenario *link flap*.

**5. Hop Count**

Hop count adalah jumlah switch yang dilewati oleh aturan aliran rute dari switch sumber ke switch tujuan. Hop count yang lebih pendek berarti konsumsi memori tabel TCAM (*Ternary Content-Addressable Memory*) di switch lebih sedikit dan latensi perambatan (*propagation latency*) lebih rendah. Metrik ini menunjukkan efisiensi pemilihan jalur oleh algoritme: apakah algoritme menemukan rute terpendek (hop optimal) atau rute memutar.

**6. Recovery Throughput Delta (%)**

Recovery delta adalah selisih persentase antara throughput rata-rata pada fase *pre-failure* atau *during-failure* relatif terhadap nilai throughput *baseline* tanpa gangguan. Nilai delta mendekati 0% menunjukkan resiliensi tinggi dari pengendali terhadap skenario kegagalan, sedangkan nilai delta negatif yang besar menunjukkan penurunan performa signifikan yang disebabkan oleh lambatnya rerouting atau ketidakmampuan algoritme beradaptasi.
