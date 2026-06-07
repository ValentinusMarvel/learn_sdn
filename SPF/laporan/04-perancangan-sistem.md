# 5. Perancangan Sistem

Bab ini memaparkan arsitektur teknis sistem, diagram alir proses utama, dan desain antarmuka CLI yang digunakan untuk menjalankan pengujian. Seluruh diagram dibuat menggunakan **Mermaid syntax** yang ter-render otomatis di Markdown.

---

## 5.1 Arsitektur Jaringan Solusi (OS-Ken & Mininet)

Sistem ini menggunakan arsitektur SDN klasik dengan pemisahan tegas antara *control plane* (OS-Ken Controller) dan *data plane* (Mininet Open vSwitch). Komunikasi antara kedua bidang dilakukan melalui protokol OpenFlow 1.3 (*southbound API*).

Berikut adalah diagram arsitektur integrasi sistem:

```mermaid
graph TD
    subgraph Control Plane ["Control Plane (OS-Ken Controllers)"]
        ryu_base["base_controller.py<br/>SPFBaseController"] <--> algo_switch{Algoritma?}
        algo_switch -->|A*| c_astar["astar_osken_controller.py<br/>compute_path()"]
        algo_switch -->|Bellman-Ford| c_bf["bellman_ford_osken_controller.py<br/>compute_path()"]
        algo_switch -->|Widest Path| c_wp["widest_path_osken_controller.py<br/>compute_path()"]
    end

    subgraph Southbound ["Southbound API (OpenFlow 1.3)"]
        ctrl_msg["Packet-In / Flow-Mod / Port-Status / LLDP"]
    end

    subgraph Data Plane ["Data Plane (Mininet OVS)"]
        s1((s1)) <--> s2((s2))
        s2 <--> s3((s3))
        s3 <--> s4((s4))
        s4 <--> s5((s5))
        s5 <--> s1((s1))

        h1[h1] --- s1
        h3[h3] --- s2
        h10[h10] --- s5
    end

    ryu_base <--> ctrl_msg
    ctrl_msg <--> s1
    ctrl_msg <--> s2
    ctrl_msg <--> s5
```

**Penjelasan arsitektur:**
*   **Control Plane**: `SPFBaseController` merupakan kelas induk yang menangani seluruh interaksi OpenFlow (Packet-In, Flow-Mod, LLDP processing). Tiga subclass algoritmik masing-masing hanya perlu mengimplementasikan `compute_path()`, yaitu fungsi yang menerima switch sumber, switch tujuan, dan port akses, lalu mengembalikan daftar tuple `(dpid, in_port, out_port)`.
*   **Southbound API**: Pesan OpenFlow 1.3 yang mengalir antara controller dan switch meliputi: *Packet-In* (paket tanpa flow rule dikirim ke controller), *Flow-Mod* (controller memasang/menghapus flow rule), *Port-Status* (notifikasi perubahan status port), dan *LLDP* (deteksi topologi).
*   **Data Plane**: Contoh di atas menunjukkan topologi Ring-5 dengan 5 switch (s1–s5) yang terhubung melingkar. Setiap switch memiliki 2 host yang terhubung melalui *access port*. Topologi Jellyfish memiliki 10 switch dengan koneksi acak regular (seed 42).

---

## 5.2 Diagram Alir / Alur Proses (Flowchart)

### A. Alur Pemrosesan *Packet-In* & Rerouting Dinamis

Diagram berikut menjelaskan logika pengendali saat menerima paket baru yang belum memiliki aturan aliran (*flow rules*) di switch:

```mermaid
flowchart TD
    A([Mulai: Packet-In Terdeteksi di Switch]) --> B[Kirim pesan Packet-In ke OS-Ken Controller]
    B --> C{Apakah Paket LLDP?}
    C -->|Ya| D1([Abaikan, Ditangani Modul Topologi])
    C -->|Tidak| D2{Apakah Src pada Access Port?}
    D2 -->|Ya| E[Pelajari Lokasi Host Src: MAC → dpid, port]
    D2 -->|Tidak| E
    E --> F{Apakah MAC Dst Terdaftar di mymacs?}
    F -->|Tidak| G[Lakukan Controlled Flood via Spanning Tree] --> H([Selesai])
    F -->|Ya| I[Cari DPID Switch Src & Dst Host]
    I --> J[Panggil Fungsi compute_path]
    J --> K{Pilih Algoritma Routing Aktif}
    K -->|A*| L1[Hitung rute dengan heuristic reverse-BFS]
    K -->|Bellman-Ford| L2[Hitung rute dengan link weights dari JSON]
    K -->|Widest Path| L3[Hitung rute dengan bottleneck bandwidth maksimal]
    L1 --> M[Dapatkan path: daftar tuple dpid, in_port, out_port]
    L2 --> M
    L3 --> M
    M --> N{Path Ditemukan?}
    N -->|Tidak| O[Pasang Drop Flow Sementara 5 detik] --> H
    N -->|Ya| P[install_path: Pasang Flow-Mod Bidirectional]
    P --> Q[Kirim Packet-Out untuk melepas paket tertahan]
    Q --> H
```

**Penjelasan alur:**
1. Setiap paket tanpa flow rule memicu *Packet-In* ke controller.
2. Paket LLDP langsung diabaikan (ditangani modul topologi terpisah).
3. Lokasi host sumber dipelajari hanya dari *access port* (bukan inter-switch port).
4. Jika MAC tujuan diketahui, controller memanggil `compute_path()` sesuai algoritma aktif.
5. Jika tidak ada jalur (misalnya switch tujuan terputus), *drop flow* sementara dipasang selama 5 detik untuk mencegah *Packet-In storm*.
6. Flow dipasang secara **bidirectional** (baik arah maju maupun balik) pada setiap switch di sepanjang jalur.

---

### B. Alur Eksekusi Otomatisasi Testbed Gangguan (*Resilience Run*)

Diagram berikut menjelaskan alur kerja skrip pengujian `run_live_scenarios.py` saat menjalankan satu skenario kegagalan:

```mermaid
flowchart TD
    Start([Mulai Skenario Pengujian]) --> Init[Jalankan OS-Ken Controller & Inisialisasi Topologi Mininet]
    Init --> Discovery[Tunggu Topologi Dikenali & ARP Konvergen via pingall]
    Discovery --> Pre{Apakah Ada Pre-Action?}
    Pre -->|Ya: link_down_before / switch_down / throttle| Act1[Terapkan Kegagalan/Pembatasan Link Sebelum Traffic]
    Act1 --> Traffic
    Pre -->|Tidak: link_down_during / link_flap| Traffic[Mulai Transfer Data iperf3 TCP 5 detik & Nyalakan tcpdump]
    Traffic --> Time{Detik ke-1 Dicapai?}
    Time -->|Ya| Act2[Terapkan Kegagalan Link/Switch Secara Dinamis]
    Act2 --> Wait
    Time -->|Tidak: baseline| Wait[Tunggu iperf3 Selesai 5 Detik]
    Wait --> Stop[Matikan tcpdump & Hentikan Controller/Mininet]
    Stop --> Parse[Parse JSON iperf3 → Ekstrak Throughput, Retransmits, Runtime]
    Parse --> Save[Simpan Hasil ke JSONL/CSV]
    Save --> End([Selesai: Lanjut ke Skenario Berikutnya])
```

**Penjelasan alur:**
1. Setiap iterasi skenario memulai pengendali OS-Ken dan topologi Mininet dari nol (*clean state*).
2. Setelah topologi konvergen (diverifikasi melalui pingall), skenario kegagalan diterapkan sesuai jenisnya:
   *   **Pre-action** (link_down_before, switch_down, bandwidth_throttle): kegagalan diterapkan *sebelum* traffic dimulai.
   *   **During-action** (link_down_during, link_flap): kegagalan diterapkan 1 detik *setelah* traffic dimulai.
3. Transfer data TCP iperf3 berjalan selama 5 detik per pasangan host.
4. Hasil dikumpulkan dalam format JSONL, kemudian dikonversi ke CSV untuk analisis Jupyter Notebook.

---

### C. Alur Rerouting Otomatis Pasca-Kegagalan Topologi

Diagram berikut menjelaskan mekanisme internal controller saat topologi berubah akibat kegagalan link/switch:

```mermaid
flowchart TD
    A([Event: Link/Switch Berubah]) --> B[LLDP Mendeteksi Perubahan Topologi]
    B --> C[get_topology_data: Perbarui Switch List, Adjacency, Port Map]
    C --> D{Topologi Signature Berubah?}
    D -->|Tidak| E([Abaikan, Tidak Ada Perubahan])
    D -->|Ya| F[Hapus Host pada Switch yang Hilang]
    F --> G[Flush Semua Flow Entry yang Dipasang]
    G --> H[Bangun Ulang Broadcast Spanning Tree via BFS]
    H --> I[Panggil _on_topology_changed Hook untuk Subclass]
    I --> J[Reinstall Seluruh Rute untuk Semua Pasangan Host yang Diketahui]
    J --> K([Selesai: Controller Siap Melayani Traffic Baru])
```

**Penjelasan mekanisme:**
1. Perubahan topologi dideteksi melalui event LLDP dan divalidasi menggunakan *topology signature* (hash dari daftar switch dan link) untuk menghindari pemrosesan duplikat.
2. Seluruh flow entry lama di-flush untuk mencegah *stale routing*.
3. Spanning tree dibangun ulang untuk memastikan controlled flooding tetap berfungsi.
4. Seluruh rute yang diketahui dihitung ulang secara proaktif menggunakan algoritma aktif, **tanpa menunggu Packet-In baru**.

---

## 5.3 Desain Antarmuka (CLI & Konfigurasi)

Sistem pengujian dijalankan melalui CLI (Command Line Interface) berbasis terminal Linux. Berikut adalah skema perintah utama:

```bash
python3 SPF/testing-code/run_live_scenarios.py \
  --topologies [ring5 | jellyfish] \
  --algorithms [astar | bellman_ford | widest_path] \
  --scenarios [baseline_no_failure | link_down_before_traffic | \
               link_down_during_traffic | link_flap | switch_down | \
               bandwidth_throttle | random_link_down_jellyfish] \
  --max-pairs 20 \
  --repetitions 5 \
  --pcap-dir [Direktori Output PCAP] \
  --output [Berkas Hasil JSONL]
```

**Parameter penting:**
| Parameter | Nilai Eksperimen | Penjelasan |
| :--- | :---: | :--- |
| `--max-pairs` | 20 | Jumlah pasangan host acak yang diuji per skenario |
| `--repetitions` | 5 | Jumlah pengulangan per pasangan host |
| `--topologies` | ring5, jellyfish | Dua topologi yang dibandingkan |
| `--algorithms` | astar, bellman_ford, widest_path | Tiga algoritma yang dievaluasi |
| `--scenarios` | 7 jenis | Baseline + 6 skenario kegagalan |

Konfigurasi bobot kapasitas link statis dibaca oleh controller dari berkas `link_weights.json`. File ini mendefinisikan bandwidth (dalam Mbps) untuk setiap link antar-switch, yang digunakan oleh Bellman-Ford sebagai cost dan oleh Widest Path sebagai kapasitas.
