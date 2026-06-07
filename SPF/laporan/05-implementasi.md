# 6. Implementasi

> [!TIP]
> **PANDUAN RUBRIK PENILAIAN - KRITERIA 3 (Skor Maksimal: 5/5):**
> Untuk mendapatkan skor maksimal pada bagian implementasi, Anda harus:
> 1. Menjelaskan secara runut struktur file kode program yang digunakan (pemetaan file di repositori).
> 2. Menampilkan cuplikan kode (*snippet*) penting dari pengendali Ryu (seperti mekanisme instalasi flow atau event handler packet-in).
> 3. Menyajikan demo hasil implementasi berupa grafik visualisasi performa dan resiliensi (throughput, runtime, packet loss, retransmits) hasil ekspor Jupyter Notebook Anda.

---

## 6.1 Pemetaan Berkas Implementasi
Berikut adalah tabel yang memetakan berkas implementasi di repositori [github.com/ValentinusMarvel/learn_sdn](https://github.com/ValentinusMarvel/learn_sdn):

| Komponen | Nama Berkas | Peran dan Fungsi |
| :--- | :--- | :--- |
| **Topologi Jaringan** | [topo-ring5_lab.py](file:///c:/Users/anang/OneDrive/Documents/GitHub/learn_sdn/SPF/topo-ring5_lab.py) | Membangun topologi emulasi Ring-5 (5 switch, 10 host). |
| | [jellyfish_topo.py](file:///c:/Users/anang/OneDrive/Documents/GitHub/learn_sdn/SPF/jellyfish_topo.py) | Membangun topologi acak regular Jellyfish (10 switch, 10 host). |
| **Pengendali Ryu (Control)** | [base_controller.py](file:///c:/Users/anang/OneDrive/Documents/GitHub/learn_sdn/SPF/base_controller.py) | Menyediakan fungsi dasar SPF, ARP static, dan OFP Flow Mod. |
| | [astar_osken_controller.py](file:///c:/Users/anang/OneDrive/Documents/GitHub/learn_sdn/SPF/astar_osken_controller.py) | Controller Ryu khusus untuk menjalankan perutean A*. |
| | [bellman_ford_osken_controller.py](file:///c:/Users/anang/OneDrive/Documents/GitHub/learn_sdn/SPF/bellman_ford_osken_controller.py) | Controller Ryu khusus untuk perutean Bellman-Ford (memakai weights). |
| | [widest_path_osken_controller.py](file:///c:/Users/anang/OneDrive/Documents/GitHub/learn_sdn/SPF/widest_path_osken_controller.py) | Controller Ryu khusus perutean QoS Widest Path. |
| **Algoritma Core (Math)** | [astar.py](file:///c:/Users/anang/OneDrive/Documents/GitHub/learn_sdn/SPF/algorithms/astar.py) | Implementasi pencarian A* murni dengan heuristik reverse-BFS. |
| | [bellman_ford.py](file:///c:/Users/anang/OneDrive/Documents/GitHub/learn_sdn/SPF/algorithms/bellman_ford.py) | Implementasi Bellman-Ford murni dengan deteksi negative cycle. |
| | [widest_path.py](file:///c:/Users/anang/OneDrive/Documents/GitHub/learn_sdn/SPF/algorithms/widest_path.py) | Implementasi pencarian jalur dengan bottleneck bandwidth maksimal. |
| **Simulasi & Testbed** | [run_live_scenarios.py](file:///c:/Users/anang/OneDrive/Documents/GitHub/learn_sdn/SPF/testing-code/run_live_scenarios.py) | Skrip Python otomatisasi eksekusi 7 skenario kegagalan. |
| **Analisis & Plot** | [plot_results.ipynb](file:///c:/Users/anang/OneDrive/Documents/GitHub/learn_sdn/SPF/analysis/plot_results.ipynb) | Jupyter Notebook pengolahan data hasil uji coba dan visualisasi. |

---

## 6.2 Cuplikan Kode / Mekanisme Penting

### A. Mekanisme Penanganan Packet-In OpenFlow 1.3
*Jelaskan bagaimana Ryu menangkap pesan Packet-In dari switch saat paket ARP atau IPv4 pertama kali masuk ke kontrol kontrol. Tampilkan cuplikan kode `@set_ev_cls` dari [base_controller.py](file:///c:/Users/anang/OneDrive/Documents/GitHub/learn_sdn/SPF/base_controller.py):*

```python
# Masukkan potongan kode penanganan packet-in di sini
# Contoh:
# @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
# def _packet_in_handler(self, ev):
#     ...
```

### B. Mekanisme Instalasi Flow Rule (*Flow Mod*)
*Jelaskan bagaimana Ryu mengirimkan perintah `OFPFlowMod` untuk memasang aturan port pada switch di sepanjang jalur hasil kalkulasi:*

```python
# Masukkan potongan kode add_flow di sini dari base_controller.py
# def add_flow(self, datapath, priority, match, actions, buffer_id=None, idle_timeout=0):
#     ...
```

---

## 6.3 Hasil Pengujian & Demo Visualisasi
*Sajikan visualisasi performa hasil ekspor Jupyter Notebook Anda. Anda dapat menyisipkan file gambar yang tersimpan di `SPF/img/analysis/` (gunakan absolute paths untuk memastikan gambar ter-render di PDF/laporan akhir).*

### A. Perbandingan Throughput Rata-Rata per Skenario
*Tampilkan gambar dari `SPF/img/analysis/throughput_by_topology.png` untuk menunjukkan bagaimana masing-masing algoritma merespons pembatasan bandwidth atau kegagalan link:*

![Throughput Comparison](/workspaces/learn_sdn/SPF/img/analysis/throughput_by_topology.png)

*Interpretasikan grafik di atas:*
*   Jelaskan mengapa A* dan Widest Path mengalami penurunan throughput yang tajam hingga ~52 Mbps pada skenario Bandwidth Throttle di Ring-5, sedangkan Bellman-Ford tidak terpengaruh (~95 Mbps).
*   Sebutkan hubungan ini dengan penggunaan kapasitas bandwidth dari `link_weights.json` secara keliru sebagai biaya (*cost*) pada Bellman-Ford.

---

### B. Distribusi Waktu Komputasi Jalur (Runtime)
*Tampilkan gambar `SPF/img/analysis/runtime_distribution.png` untuk membandingkan kecepatan pemrosesan keputusan perutean antar-algoritma:*

![Runtime Distribution](/workspaces/learn_sdn/SPF/img/analysis/runtime_distribution.png)

*Interpretasikan grafik di atas:*
*   Bandingkan efisiensi runtime A* (yang menggunakan heuristic pruning) dengan Bellman-Ford (exhaustive relaxation) dan Widest Path (modified Dijkstra).
*   Jelaskan mengapa runtime Widest Path secara umum lebih lambat dibanding A*.

---

### C. Analisis Resiliensi: Dampak Kegagalan (Failure Recovery Delta)
*Tampilkan gambar `SPF/img/analysis/failure_recovery_analysis.png` untuk melihat dampak langsung saat link terputus di tengah-tengah transmisi:*

![Failure Recovery](/workspaces/learn_sdn/SPF/img/analysis/failure_recovery_analysis.png)

*Interpretasikan grafik di atas:*
*   Jelaskan dampak pemutusan link dinamis pada detik ke-1 dalam skenario `link_down_during_traffic` dan `link_flap`.
*   Tunjukkan tingkat retransmisi TCP (dari file `retransmits_analysis.png`) untuk menunjukkan tingkat keparahan paket yang hilang sebelum rute berhasil dialihkan oleh controller.

---

## 6.4 Hasil Peringkat Komposit Akhir
Berikut adalah tabel peringkat akhir performa algoritma komposit per topologi hasil olahan Jupyter Notebook (skor 0.0 s.d 1.0):

### A. Topologi Jellyfish
| Peringkat | Algoritma | Mean Throughput (Mbps) | Mean Runtime (ms) | Success Rate | Composite Score |
| :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | **Bellman-Ford** | 95.15 | 0.0931 | 92.86% | **0.7641** |
| 2 | **A\*** | 95.08 | 0.0566 | 92.86% | **0.4439** |
| 3 | **Widest Path** | 95.06 | 0.2600 | 92.86% | **0.0000** |

### B. Topologi Ring-5
| Peringkat | Algoritma | Mean Throughput (Mbps) | Mean Runtime (ms) | Success Rate | Composite Score |
| :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | **Bellman-Ford** | 94.59 | 0.0418 | 91.67% | **0.8000** |
| 2 | **A\*** | 87.43 | 0.0427 | 91.67% | **0.1985** |
| 3 | **Widest Path** | 87.46 | 0.1595 | 91.67% | **0.0016** |
