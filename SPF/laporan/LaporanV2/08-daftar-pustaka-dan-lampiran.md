# DAFTAR PUSTAKA

Sitasi di dalam teks laporan menggunakan penomoran dengan tanda kurung siku (contoh: [1], [5]). Format penulisan mengikuti panduan IEEE:

[1] N. McKeown *et al.*, "OpenFlow: enabling innovation in campus networks," *ACM SIGCOMM Computer Communication Review*, vol. 38, no. 2, pp. 69-74, 2008.

[2] B. Lantz, B. Heller, and N. McKeown, "A network in a laptop: rapid prototyping for software-defined networks," in *Proceedings of the 9th ACM SIGCOMM Workshop on Hot Topics in Networks (HotNets-IX)*, pp. 1-6, Nov. 2010.

[3] OS-Ken Project, "OS-Ken: An Open-Source Controller Platform for Software-Defined Networking," [Online]. Available: https://github.com/osrg/os-ken, [Diakses: 8-Jun-2026].

[4] ESnet, "iperf3: A TCP, UDP, and SCTP network bandwidth measurement tool," [Online]. Available: https://github.com/esnet/iperf, [Diakses: 8-Jun-2026].

[5] P. E. Hart, N. J. Nilsson, and B. Raphael, "A Formal Basis for the Heuristic Determination of Minimum Cost Paths," *IEEE Transactions on Systems Science and Cybernetics*, vol. 4, no. 2, pp. 100-107, July 1968.

[6] R. Bellman, "On a routing problem," *Quarterly of Applied Mathematics*, vol. 16, no. 1, pp. 87-90, 1958.

[7] L. R. Ford and D. R. Fulkerson, *Flows in Networks*. Princeton, NJ: Princeton Univ. Press, 1962.

[8] ValentinusMarvel, "learn_sdn: Repositori kode proyek Analisis Komparatif Performa dan Resiliensi Algoritma SPF pada SDN," GitHub, [Online]. Available: https://github.com/ValentinusMarvel/learn_sdn, [Diakses: 8-Jun-2026].

---

# LAMPIRAN

## Lampiran A: Tabel Data Ringkasan Performa (Summary Statistics)

Seluruh data di bawah ini diekstraksi langsung dari keluaran (*cell outputs*) Jupyter Notebook `plot_results_executed_final.ipynb` yang dieksekusi dengan parameter `max_pairs=20` dan `repetitions=5` (total 3.900 baris data):

### Tabel A.1: Rata-Rata Throughput (Mbps) per Topologi dan Skenario

| Topologi | Skenario Gangguan | A\* | Bellman-Ford | Widest Path |
| :--- | :--- | :---: | :---: | :---: |
| **Jellyfish** | Bandwidth Throttle | 95.24 | 95.24 | 82.37 |
| | Baseline No Failure | 95.14 | 95.22 | 95.28 |
| | Link Down Before Traffic | 95.24 | 95.22 | 95.18 |
| | Link Down During Traffic | 92.09 | 92.41 | 91.99 |
| | Link Flap | 86.06 | 88.71 | 87.20 |
| | Random Link Down Jellyfish | 95.24 | 95.11 | 95.27 |
| | Switch Down | 95.24 | 95.04 | 95.37 |
| **Ring-5** | Bandwidth Throttle | 56.70 | 94.95 | 48.11 |
| | Baseline No Failure | 95.27 | 94.90 | 95.26 |
| | Link Down Before Traffic | 95.22 | 95.20 | 95.23 |
| | Link Down During Traffic | 94.94 | 95.13 | 95.15 |
| | Link Flap | 94.90 | 94.93 | 94.22 |
| | Switch Down | 95.08 | 95.11 | 95.16 |

### Tabel A.2: Rata-Rata Runtime Komputasi Jalur (ms) per Topologi dan Skenario

| Topologi | Skenario Gangguan | A\* | Bellman-Ford | Widest Path |
| :--- | :--- | :---: | :---: | :---: |
| **Jellyfish** | Bandwidth Throttle | 0.0714 | 0.0945 | 0.0793 |
| | Baseline No Failure | 0.0726 | 0.0931 | 0.0825 |
| | Link Down Before Traffic | 0.0701 | 0.0921 | 0.0829 |
| | Link Down During Traffic | 0.0893 | 0.1079 | 0.1084 |
| | Link Flap | 0.0678 | 0.0876 | 0.0776 |
| | Random Link Down Jellyfish | 0.0738 | 0.0923 | 0.0795 |
| | Switch Down | 0.0910 | 0.0952 | 0.0899 |
| **Ring-5** | Bandwidth Throttle | 0.0556 | 0.0512 | 0.0519 |
| | Baseline No Failure | 0.0542 | 0.0685 | 0.0520 |
| | Link Down Before Traffic | 0.0533 | 0.0474 | 0.0515 |
| | Link Down During Traffic | 0.0508 | 0.0493 | 0.2700 |
| | Link Flap | 0.0480 | 0.0436 | 0.0448 |
| | Switch Down | 0.0549 | 0.0486 | 0.0563 |

### Tabel A.3: Rata-Rata Hop Count per Topologi dan Skenario

| Topologi | Skenario Gangguan | A\* | Bellman-Ford | Widest Path |
| :--- | :--- | :---: | :---: | :---: |
| **Jellyfish** | Bandwidth Throttle | 1.75 | 1.75 | 2.25 |
| | Baseline No Failure | 1.75 | 1.75 | 2.25 |
| | Link Down Before Traffic | 1.75 | 1.75 | 2.25 |
| | Link Down During Traffic | 1.76 | 1.73 | 2.25 |
| | Link Flap | 1.75 | 1.75 | 2.25 |
| | Random Link Down Jellyfish | 1.75 | 1.75 | 2.25 |
| | Switch Down | 1.89 | 1.89 | 2.11 |
| **Ring-5** | Bandwidth Throttle | 1.45 | 1.45 | 1.65 |
| | Baseline No Failure | 1.45 | 1.45 | 1.65 |
| | Link Down Before Traffic | 1.45 | 1.45 | 1.65 |
| | Link Down During Traffic | 1.45 | 1.45 | 1.65 |
| | Link Flap | 1.45 | 1.45 | 1.65 |
| | Switch Down | 1.56 | 1.56 | 1.78 |

### Tabel A.4: Success Rate per Skenario

| Topologi | Skenario Gangguan | A\* | Bellman-Ford | Widest Path |
| :--- | :--- | :---: | :---: | :---: |
| **Jellyfish** | Bandwidth Throttle | 100/100 (100%) | 100/100 (100%) | 100/100 (100%) |
| | Baseline No Failure | 100/100 (100%) | 100/100 (100%) | 100/100 (100%) |
| | Link Down Before Traffic | 100/100 (100%) | 100/100 (100%) | 100/100 (100%) |
| | Link Down During Traffic | 80/100 (80%) | 81/100 (81%) | 80/100 (80%) |
| | Link Flap | 100/100 (100%) | 100/100 (100%) | 100/100 (100%) |
| | Random Link Down Jellyfish | 100/100 (100%) | 100/100 (100%) | 100/100 (100%) |
| | Switch Down | 45/100 (45%) | 45/100 (45%) | 45/100 (45%) |
| **Ring-5** | Bandwidth Throttle | 100/100 (100%) | 100/100 (100%) | 100/100 (100%) |
| | Baseline No Failure | 100/100 (100%) | 100/100 (100%) | 100/100 (100%) |
| | Link Down Before Traffic | 100/100 (100%) | 100/100 (100%) | 100/100 (100%) |
| | Link Down During Traffic | 100/100 (100%) | 100/100 (100%) | 100/100 (100%) |
| | Link Flap | 100/100 (100%) | 100/100 (100%) | 100/100 (100%) |
| | Switch Down | 45/100 (45%) | 45/100 (45%) | 45/100 (45%) |

### Tabel A.5: Dampak Kegagalan (Delta Throughput vs Baseline, dalam %)

| Topologi | Fase Kegagalan | A\* | Bellman-Ford | Widest Path |
| :--- | :--- | :---: | :---: | :---: |
| **Jellyfish** | During-Failure | -6.73% | -5.10% | -6.24% |
| | Pre-Failure | +0.10% | -0.05% | -3.94% |
| **Ring-5** | During-Failure | -0.37% | +0.14% | -0.61% |
| | Pre-Failure | -16.59% | +0.19% | -20.23% |

### Tabel A.6: Peringkat Komposit Akhir

| Topologi | Peringkat | Algoritme | Mean Throughput (Mbps) | Mean Runtime (ms) | Std Throughput | Success Rate | Skor Komposit |
| :--- | :---: | :--- | :---: | :---: | :---: | :---: | :---: |
| **Jellyfish** | 1 | Bellman-Ford | 93.7897 | 0.0942 | 3.4133 | 89.43% | **0.8000** |
| | 2 | A\* | 93.3519 | 0.0749 | 4.3856 | 89.29% | 0.7046 |
| | 3 | Widest Path | 91.4899 | 0.0846 | 13.4988 | 89.29% | 0.0991 |
| **Ring-5** | 1 | Bellman-Ford | 95.0287 | 0.0517 | 0.5864 | 90.83% | **0.8000** |
| | 2 | A\* | 88.0394 | 0.0526 | 23.5992 | 90.83% | 0.2897 |
| | 3 | Widest Path | 86.3860 | 0.0909 | 25.8231 | 90.83% | 0.0000 |

---

## Lampiran B: Deskripsi Repositori Kode

Repositori proyek akhir tersedia di: [github.com/ValentinusMarvel/learn_sdn](https://github.com/ValentinusMarvel/learn_sdn) [8].

Struktur direktori utama yang relevan:

```text
learn_sdn/
└── SPF/
    ├── base_controller.py                       # Kelas pengendali induk OS-Ken
    ├── astar_osken_controller.py                # Subclass pengendali A*
    ├── bellman_ford_osken_controller.py         # Subclass pengendali Bellman-Ford
    ├── widest_path_osken_controller.py          # Subclass pengendali Widest Path
    ├── link_weights.json                        # Konfigurasi bobot tautan statis
    ├── topo-ring5_lab.py                        # Definisi topologi Ring-5 (Mininet)
    ├── jellyfish_topo.py                        # Definisi topologi Jellyfish (Mininet)
    ├── benchmark_core.py                        # Pustaka inti orkestrasi eksperimen (Mininet & OS-Ken)
    ├── benchmark_jsonl_to_csv.py                # Konverter log JSONL ke CSV
    ├── testing-code/
    │   └── run_live_scenarios.py                # Skrip utama pengeksekusi otomatisasi 7 skenario
    ├── algorithms/
    │   ├── astar.py                             # Implementasi A* murni
    │   ├── bellman_ford.py                      # Implementasi Bellman-Ford murni
    │   └── widest_path.py                       # Implementasi Widest Path murni
    ├── analysis/
    │   └── plot_results_executed_final.ipynb    # Jupyter Notebook analisis data final
    ├── csv/
    │   ├── ring5-scenarios.csv                  # Data eksperimen Ring-5 (1.800 baris)
    │   ├── jellyfish-scenarios.csv              # Data eksperimen Jellyfish (2.100 baris)
    │   └── analysis/                            # Output CSV, Markdown, dan LaTeX
    └── laporan/
        └── LaporanV2/                           # Berkas laporan tersegmentasi ini
```

**Perintah menjalankan pengendali:**

```bash
os-ken-manager SPF/bellman_ford_osken_controller.py
```

**Perintah eksekusi testbed otomatis:**

```bash
sudo python3 SPF/testing-code/run_live_scenarios.py --topologies ring5 --algorithms bellman_ford \
  --scenarios baseline_no_failure link_down_before_traffic link_down_during_traffic link_flap switch_down bandwidth_throttle \
  --max-pairs 20 --repetitions 5 --output SPF/csv/ring5-scenarios.jsonl
```

---

## Lampiran C: Pernyataan Kontribusi Individu Anggota Kelompok

Setiap anggota kelompok berkontribusi secara berkeadilan dalam perancangan, implementasi, pengujian, dan penyusunan laporan proyek akhir ini. Matriks kontribusi anggota kelompok dirinci pada tabel berikut:

| No | Nama Anggota | NIM | Peran Utama | Rincian Kontribusi | Tanda Tangan |
| :-: | :--- | :---: | :--- | :--- | :---: |
| 1 | [Nama Anggota 1] | [NIM 1] | *Project Leader* / Developer | Merancang arsitektur modular `base_controller.py`, mengimplementasikan subclass A\*, dan mengintegrasikan modul heuristik *reverse-BFS*. | \_\_\_\_\_\_\_\_\_\_\_ |
| 2 | [Nama Anggota 2] | [NIM 2] | Test Engineer / Data Analyst | Merancang dan mengeksekusi testbed 7 skenario kegagalan, melakukan validasi 3.900 data point, dan mengembangkan pipeline analisis Jupyter Notebook. | \_\_\_\_\_\_\_\_\_\_\_ |
| 3 | [Nama Anggota 3] | [NIM 3] | Developer / Technical Writer | Mengimplementasikan subclass Bellman-Ford, mengintegrasikan pembacaan `link_weights.json`, dan menyusun Bab Pendahuluan hingga Landasan Teori. | \_\_\_\_\_\_\_\_\_\_\_ |
| 4 | [Nama Anggota 4] | [NIM 4] | Developer / Technical Writer | Mengimplementasikan subclass Widest Path, menganalisis kendala monitoring dinamis, dan menyusun Bab Metodologi hingga Daftar Pustaka. | \_\_\_\_\_\_\_\_\_\_\_ |
