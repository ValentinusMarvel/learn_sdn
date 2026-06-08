# 4.4 Landasan Teori

> [!TIP]
> **PANDUAN PENULISAN LANDASAN TEORI (Skor Maksimal: 5/5):**
> *   **Panjang**: Total berkisar antara **2–3 halaman** (sekitar 1.000–1.500 kata).
> *   **Gaya Penulisan**: Jelaskan konsep dasar secara ilmiah. Hindari penyalinan (*copy-paste*) definisi mentah dari internet tanpa parafrase. Gunakan referensi rujukan pustaka di akhir paragraf (misalnya `[1]`, `[2]`).
> *   **Struktur Wajib**: Memuat ulasan teoretis algoritme (4.4.1), karakteristik topologi (4.4.2), dan metrik evaluasi QoS jaringan (4.4.3).

---

## 4.4.1 Algoritme yang Diuji

> [!IMPORTANT]
> **PETUNJUK PENULISAN ALGORITME:**
> *   Ulas cara kerja singkat dari keempat algoritme yang digunakan dalam kode proyek:
>     1.  **Breadth-First Search (BFS)**: Digunakan untuk membangun *spanning tree* guna menangani *broadcast storms* di switch SDN.
>     2.  **A\***: Pencarian heuristik berbasis fungsi evaluasi $f(n) = g(n) + h(n)$.
>     3.  **Bellman-Ford**: Relaksasi jarak secara iteratif.
>     4.  **Widest Path**: Modifikasi pencarian rute berbasis *bottleneck capacity* maksimal.
> *   Sertakan **kompleksitas waktu** (Big-O notation) untuk setiap algoritme pada graf dengan $V$ node dan $E$ edge.
> *   Sebutkan karakteristik utama masing-masing algoritme.

### [TEMPLAT DRAFT LANDASAN ALGORITME]
Komputasi rute dinamis pada graf topologi jaringan memanfaatkan beberapa algoritme pencarian jalur terpendek (*Shortest Path First* / SPF) yang disesuaikan dengan kebutuhan optimasi:

1.  **Breadth-First Search (BFS)**:
    *   *Cara Kerja*: BFS melakukan penelusuran graf tingkat demi tingkat (*layer-by-layer*) mulai dari node akar. BFS mengeksplorasi semua node tetangga pada kedalaman saat ini sebelum berpindah ke node pada tingkat berikutnya. Pada proyek ini, BFS digunakan untuk menghitung *broadcast spanning tree* pada controller OS-Ken untuk mencegah *looping* paket ARP/broadcast di data plane.
    *   *Kompleksitas Waktu*: $O(V + E)$, di mana $V$ adalah jumlah switch dan $E$ adalah jumlah link fisik.
    *   *Karakteristik Utama*: Menemukan jalur dengan jumlah hop paling minimal pada graf tanpa bobot.

2.  **Algoritme A\***:
    *   *Cara Kerja*: A\* merupakan algoritme pencarian terarah (*informed search*) yang memperkirakan biaya total rute terkecil melalui node $n$ menggunakan fungsi evaluasi $f(n) = g(n) + h(n)$. Variabel $g(n)$ adalah biaya aktual dari node sumber ke node $n$, sedangkan $h(n)$ adalah estimasi biaya heuristik dari node $n$ ke node tujuan. Dalam proyek ini, fungsi heuristik $h(n)$ dihitung menggunakan jarak hop minimum dari tujuan ke node $n$ menggunakan metode *reverse-BFS*.
    *   *Kompleksitas Waktu*: $O(E \log V)$ pada kasus rata-rata menggunakan *priority queue*.
    *   *Karakteristik Utama*: Efisien dan cepat karena mampu memangkas (*pruning*) eksplorasi node graf yang tidak mengarah ke tujuan.

3.  **Algoritme Bellman-Ford**:
    *   *Cara Kerja*: Menemukan jalur terpendek dari satu node sumber ke semua node lainnya dengan cara melakukan relaksasi bobot link secara iteratif sebanyak $V-1$ kali. Pada setiap iterasi, algoritme memperbarui estimasi jarak terpendek jika ditemukan jalur baru yang lebih murah.
    *   *Kompleksitas Waktu*: $O(V \times E)$.
    *   *Karakteristik Utama*: Mampu menangani link dengan bobot negatif dan dapat mendeteksi keberadaan siklus berbobot negatif (*negative cycle*).

4.  **Algoritme Widest Path (Bottleneck Routing)**:
    *   *Cara Kerja*: Modifikasi dari algoritme Dijkstra yang bertujuan untuk mencari jalur yang memaksimalkan *minimum bandwidth* (kapasitas terendah) di sepanjang rute. Algoritme ini menggunakan antrean prioritas (*max-heap*) untuk memilih node tetangga dengan bottleneck bandwidth terbesar.
    *   *Kompleksitas Waktu*: $O(E \log V)$.
    *   *Karakteristik Utama*: Memprioritaskan jalur dengan kapasitas lalu lintas terbesar (*widest*), bukan rute terpendek (*shortest*).

---

## 4.4.2 Topologi Jaringan

> [!IMPORTANT]
> **PETUNJUK PENULISAN TOPOLOGI:**
> *   Jelaskan jenis topologi Ring-5 dan Jellyfish yang digunakan dalam eksperimen.
> *   Ulas karakteristik masing-masing topologi secara arsitektural ( Ring-5 memiliki pola melingkar dengan tingkat redundansi rendah, sedangkan Jellyfish merupakan topologi acak regular berbasis $d$-regular graph dengan seed tertentu yang memberikan redundansi sangat tinggi).
> *   Berikan alasan akademis pemilihan kedua topologi tersebut (untuk menguji performa algoritme di bawah karakteristik redundansi link yang bertolak belakang).

### [TEMPLAT DRAFT LANDASAN TOPOLOGI]
Struktur fisik dari data plane SDN memiliki pengaruh besar terhadap performa perutean dan resiliensi jalur terhadap kegagalan link. Proyek ini membandingkan dua karakteristik topologi yang bertolak belakang:

1.  **Topologi Ring-5 (Melingkar Teratur)**:
    *   *Karakteristik*: Terdiri dari 5 switch yang saling terhubung membentuk lingkaran tertutup (s1-s2-s3-s4-s5-s1). Setiap switch terhubung langsung dengan 2 host akses. Topologi ini memiliki derajat node (*node degree*) yang rendah dan konstan sebesar 2 untuk koneksi inter-switch.
    *   *Alasan Pemilihan*: Merepresentasikan arsitektur jaringan teratur dengan tingkat redundansi jalur yang sangat minim. Jika satu link antar-switch putus, hanya tersisa tepat satu jalur alternatif fisik untuk menghubungkan node-node tersebut. Hal ini sangat ideal untuk menguji batas ketahanan algoritme SPF saat terjadi *single link failure* atau pembatasan kapasitas pada jalur utama.

2.  **Topologi Jellyfish (Acak Regular)**:
    *   *Karakteristik*: Topologi pusat data berbasis graf acak $d$-regular (dalam hal ini, switch dihubungkan secara acak namun teratur dengan derajat node inter-switch yang seragam). Topologi Jellyfish pada proyek ini dibangun menggunakan 10 switch dengan generator seed acak 42 untuk memastikan replikasi.
    *   *Alasan Pemilihan*: Merepresentasikan struktur jaringan pusat data modern berskala besar (*data center network*) yang dinamis dengan tingkat redundansi jalur yang sangat tinggi. Jellyfish menyediakan banyak jalur alternatif (*multi-path*) antar-node dengan panjang hop yang bervariasi, memungkinkan evaluasi skalabilitas runtime algoritme SPF serta fleksibilitas pengalihan rute dinamis saat terjadi kegagalan tautan majemuk atau kegagalan switch total.

---

## 4.4.3 Metrik Evaluasi

> [!IMPORTANT]
> **PETUNJUK PENULISAN METRIK EVALUASI:**
> *   Definisikan secara teoritis metrik-metrik yang diukur:
>     1.  **Throughput (Mbps)**: Hubungkan dengan kapasitas transfer data TCP iperf3.
>     2.  **Runtime Komputasi Jalur (ms)**: Hubungkan dengan overhead pemrosesan rute di controller.
>     3.  **Packet Loss (%)**: Hubungkan dengan durasi *downtime* konvergensi saat kegagalan.
>     4.  **TCP Retransmissions**: Hubungkan dengan stabilitas transportasi data.
>     5.  **Hop Count**: Hubungkan dengan efisiensi konsumsi resource switch.
>     6.  **Recovery Throughput Delta (%)**: Hubungkan dengan daya pulih jaringan.
> *   Jelaskan relevansi setiap metrik terhadap jaminan kualitas layanan (*Quality of Service* / QoS) jaringan.

### [TEMPLAT DRAFT METRIK EVALUASI]
Untuk menilai efisiensi dan ketahanan algoritme perutean secara objektif, metrik evaluasi didefinisikan sebagai berikut:

1.  **Throughput (Mbps)**:
    *   *Definisi*: Laju transfer data aktual yang berhasil dikirimkan melalui saluran komunikasi dalam periode waktu tertentu. Diukur menggunakan aliran data iperf3 TCP selama 5 detik.
    *   *Relevansi*: Menunjukkan kapasitas transmisi data bersih yang dirasakan pengguna. Throughput tinggi menandakan rute yang dipilih memiliki kualitas link yang baik dan minim packet loss.

2.  **Runtime Komputasi Jalur (ms)**:
    *   *Definisi*: Waktu yang diperlukan oleh SDN controller (OS-Ken) untuk memproses fungsi komputasi algoritme SPF dari saat menerima request Packet-In hingga menghasilkan jalur rute.
    *   *Relevansi*: Menilai efisiensi komputasi algoritme. Runtime rendah sangat penting untuk meminimalkan *routing delay* awal dan mempercepat konvergensi pemulihan.

3.  **Packet Loss (%)**:
    *   *Definisi*: Persentase paket data yang hilang selama transmisi akibat link down sementara sebelum controller memasang flow baru. Diukur melalui perintah `pingall`.
    *   *Relevansi*: Menunjukkan keandalan jaringan. Packet loss tinggi menandakan kegagalan deteksi link atau keterlambatan konvergensi rute.

4.  **TCP Retransmissions**:
    *   *Definisi*: Jumlah paket TCP yang harus dikirim ulang oleh host pengirim karena paket sebelumnya tidak menerima ACK dari penerima dalam batas waktu RTO.
    *   *Relevansi*: Menilai stabilitas transport layer. Retransmisi tinggi mengindikasikan adanya kongesti link atau fluktuasi tautan dinamis selama pengiriman lalu lintas data aktif.

5.  **Hop Count**:
    *   *Definisi*: Jumlah hop/lompatan switch yang dilewati oleh aturan aliran rute terpilih dari switch asal ke switch tujuan.
    *   *Relevansi*: Menunjukkan efisiensi penggunaan sumber daya data plane. Hop count yang lebih pendek mengurangi konsumsi memori tabel TCAM di switch dan mengurangi latensi perambatan.

6.  **Recovery Throughput Delta (%)**:
    *   *Definisi*: Selisih persentase antara throughput rata-rata pada fase gangguan (fase *pre-failure* atau *during-failure*) relatif terhadap nilai baseline tanpa gangguan.
    *   *Relevansi*: Menilai tingkat pemulihan jaringan dinamis. Delta mendekati 0% menunjukkan resiliensi yang tinggi dari pengendali terhadap skenario kegagalan dinamis.
