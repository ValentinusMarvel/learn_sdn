# 4. Deskripsi Solusi

Bagian ini memaparkan solusi yang diusulkan untuk menjawab permasalahan perutean dinamis pada jaringan SDN serta merinci alat dan teknologi yang diintegrasikan dalam proyek akhir ini.

---

## 4.1 Gambaran Umum Solusi yang Diusulkan
Solusi yang diusulkan adalah arsitektur **SDN Shortest Path First (SPF) modular**. Kami membangun sistem pengendali terpusat yang memisahkan antara penemuan topologi (*topology discovery*), pemetaan grafik jaringan (*graph representation*), dan algoritma kalkulasi rute dinamis.

Melalui arsitektur ini, pengendali Ryu dapat mendeteksi perubahan topologi secara instan lewat pesan OpenFlow, memperbarui representasi grafik jaringan di memori, dan memicu algoritma perutean dinamis terpilih untuk memasang aliran (*flow entries*) baru ke switch secara otomatis. Pemisahan kode program ini memungkinkan penggantian algoritma perutean (A*, Bellman-Ford, atau Widest Path) secara instan tanpa perlu mengubah kode dasar pengendali switch.

---

## 4.2 Fitur Utama atau Komponen Penting
Sistem perutean dinamis ini ditopang oleh empat komponen utama:
1.  **Topology Discovery Engine (Ryu Topology Module)**:
    Menggunakan protokol LLDP (*Link Layer Discovery Protocol*) untuk mendeteksi keberadaan switch, link antar-switch, dan host secara dinamis di bawah naungan OpenFlow 1.3.
2.  **Shortest Path Forwarding Core (Ryu Controllers)**:
    *   [base_controller.py](file:///c:/Users/anang/OneDrive/Documents/GitHub/learn_sdn/SPF/base_controller.py): Menyediakan logika dasar penanganan pesan OpenFlow (*packet-in*, *port-status*, *features-reply*), pemetaan topologi, pemeliharaan tabel ARP statis, serta fungsi pembungkusan aturan aliran (*flow installer*).
    *   Subclass Pengendali Algoritmik: [astar_osken_controller.py](file:///c:/Users/anang/OneDrive/Documents/GitHub/learn_sdn/SPF/astar_osken_controller.py), [bellman_ford_osken_controller.py](file:///c:/Users/anang/OneDrive/Documents/GitHub/learn_sdn/SPF/bellman_ford_osken_controller.py), dan [widest_path_osken_controller.py](file:///c:/Users/anang/OneDrive/Documents/GitHub/learn_sdn/SPF/widest_path_osken_controller.py) yang memicu pustaka algoritma masing-masing saat kalkulasi jalur diperlukan.
3.  **Pure Python Pathfinding Algorithms**:
    Modul algoritma murni yang terisolasi di dalam subfolder `SPF/algorithms/` ([astar.py](file:///c:/Users/anang/OneDrive/Documents/GitHub/learn_sdn/SPF/algorithms/astar.py), [bellman_ford.py](file:///c:/Users/anang/OneDrive/Documents/GitHub/learn_sdn/SPF/algorithms/bellman_ford.py), [widest_path.py](file:///c:/Users/anang/OneDrive/Documents/GitHub/learn_sdn/SPF/algorithms/widest_path.py)) untuk menjamin portabilitas komputasi graf.
4.  **Automated Resilience Testbed (run_live_scenarios.py)**:
    Skrip otomatisasi berbasis Mininet ([run_live_scenarios.py](file:///c:/Users/anang/OneDrive/Documents/GitHub/learn_sdn/SPF/testing-code/run_live_scenarios.py)) yang bertugas memicu kegagalan link/switch secara dinamis pada detik tertentu saat transfer data TCP iperf3 sedang berjalan, menangkap lalu lintas jaringan menggunakan `tcpdump` secara otomatis, dan mengumpulkan metrik performa ke dalam file JSONL/CSV.

---

## 4.3 Alat dan Teknologi yang Digunakan
*   **Mininet Network Emulator**: Digunakan untuk emulasi infrastruktur jaringan (switch, link, host) di lingkungan Linux lokal.
*   **Ryu Controller Framework (OS-Ken)**: *Framework* pengendali OpenFlow berbasis Python yang menangani logika *control plane*.
*   **OpenFlow Protokol 1.3**: Protokol komunikasi *southbound API* standar untuk pertukaran instruksi antara bidang kontrol (Ryu) dan bidang data (Mininet Open vSwitch).
*   **Python 3**: Bahasa pemrograman utama yang digunakan untuk membangun controller, modul algoritma, dan skrip testbed.
*   **iperf3 & tcpdump**: Alat bantu pengukuran performa (*traffic generator* lalu lintas TCP) dan penangkap paket data jaringan (*packet capture*).
*   **Jupyter Notebook & Pandas/Seaborn**: Digunakan untuk pemrosesan data, statistik deskriptif, pemodelan skor komposit peringkat, dan visualisasi grafis hasil eksperimen.
