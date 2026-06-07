# 4. Deskripsi Solusi

Bagian ini memaparkan solusi yang diusulkan untuk menjawab permasalahan perutean dinamis pada jaringan SDN serta merinci alat dan teknologi yang diintegrasikan dalam proyek akhir ini.

---

## 4.1 Gambaran Umum Solusi yang Diusulkan

Solusi yang diusulkan adalah arsitektur **SDN Shortest Path First (SPF) modular** yang dirancang dengan prinsip pemisahan tanggung jawab (*separation of concerns*). Sistem pengendali terpusat ini memisahkan tiga komponen inti:

1.  **Penemuan Topologi (*Topology Discovery*)**: deteksi otomatis switch, link, dan host melalui protokol LLDP.
2.  **Pemetaan Grafik Jaringan (*Graph Representation*)**: representasi topologi sebagai graf berbobot menggunakan *adjacency list* dan *port map* di memori controller.
3.  **Kalkulasi Rute Dinamis (*Path Computation*)**: implementasi algoritma perutean yang dapat diganti secara modular melalui mekanisme *subclass inheritance*.

Melalui arsitektur ini, pengendali OS-Ken mendeteksi perubahan topologi secara instan lewat pesan OpenFlow (`EventLinkAdd`, `EventLinkDelete`, `EventSwitchLeave`), memperbarui representasi grafik jaringan di memori, dan secara proaktif memicu algoritma perutean dinamis terpilih untuk menghitung ulang jalur dan memasang aturan aliran (*flow entries*) baru ke seluruh switch di sepanjang jalur, tanpa menunggu *Packet-In* baru. Pemisahan kode program ini memungkinkan penggantian algoritma perutean (A*, Bellman-Ford, atau Widest Path) secara instan tanpa perlu mengubah satu baris pun kode pada kelas dasar pengendali switch.

---

## 4.2 Fitur Utama atau Komponen Penting

Sistem perutean dinamis ini ditopang oleh empat komponen utama:

### 1. Topology Discovery Engine (OS-Ken Topology Module)
Menggunakan protokol LLDP (*Link Layer Discovery Protocol*) yang dikelola oleh modul topologi bawaan OS-Ken untuk mendeteksi keberadaan switch, link antar-switch, dan host secara dinamis. Setiap perubahan topologi (link naik/turun, switch masuk/keluar) akan memicu event handler `get_topology_data()` yang memperbarui seluruh struktur data internal: daftar switch, *adjacency list*, *port map*, dan *access ports*.

### 2. Shortest Path Forwarding Core (OS-Ken Controllers)
*   **`base_controller.py`**: Kelas induk (`SPFBaseController`) yang menyediakan seluruh logika dasar:
    *   Penanganan pesan OpenFlow: *Packet-In*, *Switch Features*, *Port Status*
    *   Pembelajaran host otomatis (MAC → (dpid, port))
    *   Instalasi flow rule bidirectional (*delete-then-add* untuk idempotency)
    *   Pembangunan *broadcast spanning tree* berbasis BFS untuk kontrol flooding
    *   Mekanisme rerouting proaktif saat topologi berubah
    *   Graceful shutdown dengan pembersihan seluruh flow entry
*   **Subclass Pengendali Algoritmik**: Tiga controller turunan yang masing-masing hanya mengimplementasikan satu fungsi: `compute_path()`:
    *   `astar_osken_controller.py`: memanggil `algorithms/astar.py` dengan heuristik *reverse-BFS hop-count*
    *   `bellman_ford_osken_controller.py`: memanggil `algorithms/bellman_ford.py` dengan bobot dari `link_weights.json`
    *   `widest_path_osken_controller.py`: memanggil `algorithms/widest_path.py` dengan kapasitas *bottleneck bandwidth*

### 3. Pure Python Pathfinding Algorithms
Modul algoritma murni yang terisolasi di dalam subfolder `SPF/algorithms/` untuk menjamin portabilitas dan testabilitas komputasi graf:
*   **`astar.py`**: Implementasi pencarian A* dengan heuristik *admissible* berbasis jarak hop reverse-BFS dari tujuan. Kompleksitas waktu: O(E log V) dalam kasus rata-rata.
*   **`bellman_ford.py`**: Implementasi Bellman-Ford dengan deteksi *negative cycle* dan dukungan bobot link arbitrer dari file JSON. Kompleksitas waktu: O(V × E).
*   **`widest_path.py`**: Implementasi modifikasi Dijkstra yang memaksimalkan *minimum bandwidth* pada jalur terpilih menggunakan *max-heap priority queue*. Kompleksitas waktu: O(E log V).

### 4. Automated Resilience Testbed (`run_live_scenarios.py`)
Skrip otomatisasi berbasis Mininet yang melakukan:
*   Inisialisasi topologi (Ring-5 atau Jellyfish) dan startup pengendali OS-Ken
*   Tunggu konvergensi topologi dan ARP learning (pingall)
*   Eksekusi skenario kegagalan secara terjadwal (pre-traffic atau during-traffic)
*   Pengukuran performa menggunakan `iperf3` (TCP, 5 detik per transfer)
*   Penangkapan lalu lintas jaringan menggunakan `tcpdump` secara paralel
*   Pencatatan hasil ke file JSONL yang kemudian dikonversi ke CSV

Parameter eksekusi akhir: **`max_pairs=20`** (20 pasangan host acak per skenario) dan **`repetitions=5`** (5 kali pengulangan per pasangan), menghasilkan total **3.900 baris data** yang dianalisis.

---

## 4.3 Alat dan Teknologi yang Digunakan

| Teknologi | Versi/Spesifikasi | Peran dalam Proyek |
| :--- | :--- | :--- |
| **Mininet** | 2.3+ | Emulasi infrastruktur jaringan (switch Open vSwitch, link, host) di lingkungan Linux. |
| **OS-Ken Controller** | Python 3 | Framework pengendali OpenFlow (fork aktif Ryu) yang menangani logika *control plane*. |
| **OpenFlow** | v1.3 | Protokol komunikasi *southbound API* standar antara controller dan switch. |
| **Python** | 3.x | Bahasa pemrograman utama untuk controller, algoritma, dan skrip testbed. |
| **iperf3** | 3.x | *Traffic generator* TCP untuk mengukur throughput, retransmisi, dan stabilitas koneksi. |
| **tcpdump** | 4.x | Penangkap paket jaringan (*packet capture*) untuk analisis lalu lintas tingkat rendah. |
| **Jupyter Notebook** | 7.x | Lingkungan interaktif untuk pipeline analisis data, statistik, dan visualisasi. |
| **Pandas** | 2.x | Library manipulasi dan agregasi data tabular untuk pemrosesan CSV hasil eksperimen. |
| **Seaborn/Matplotlib** | 0.13+/3.x | Library visualisasi grafis untuk pembuatan plot performa (bar, box, scatter, faceted). |
| **Docker** | Linux Utility | Kontainerisasi lingkungan pengujian untuk isolasi dan reproduktibilitas eksperimen. |
| **Google Colab** | Cloud Service | Platform cloud untuk eksekusi notebook analisis final dengan resource GPU/CPU. |
