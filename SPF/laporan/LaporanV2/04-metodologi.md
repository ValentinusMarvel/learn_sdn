# 4.5 Metodologi

> [!TIP]
> **PANDUAN PENULISAN METODOLOGI (Skor Maksimal: 5/5):**
> *   **Panjang**: Total berkisar antara **2–3 halaman** (sekitar 800–1.200 kata).
> *   **Kejelasan Alur**: Uraikan alur rancangan pengujian secara runut dari topologi, penyiapan controller, hingga eksekusi testbed.
> *   **Replikabilitas**: Metodologi harus sangat terperinci sehingga kelompok lain dapat mereplikasi eksperimen dengan hasil yang identik.

---

## 4.5.1 Perancangan Eksperimen

> [!IMPORTANT]
> **PETUNJUK PENULISAN PERANCANGAN EKSPERIMEN:**
> *   Jelaskan kombinasi pengujian yang dilakukan: **2 topologi** (Ring-5, Jellyfish) $\times$ **3 algoritme** (A*, Bellman-Ford, Widest Path) $\times$ **7 skenario kegagalan**.
> *   Uraikan secara detail ketujuh skenario gangguan yang diuji:
>     1.  *Baseline No Failure* (tanpa gangguan).
>     2.  *Link Down Before Traffic* (mati sebelum traffic dimulai).
>     3.  *Link Down During Traffic* (mati pada detik ke-1 saat traffic).
>     4.  *Link Flap* (mati-hidup berkala).
>     5.  *Switch Down* (kegagalan switch total).
>     6.  *Bandwidth Throttle* (kapasitas drop dari 1000 Mbps ke 10 Mbps).
>     7.  *Random Link Down Jellyfish* (link acak mati, khusus Jellyfish).
> *   Sebutkan alat dan utilitas pengujian yang diintegrasikan dalam skrip `run_live_scenarios.py` (seperti `iperf3` untuk TCP, `pingall` untuk loss, `tcpdump` untuk PCAP capture).

### [TEMPLAT DRAFT PERANCANGAN EKSPERIMEN]
Eksperimen dirancang untuk mengevaluasi ketangguhan jaringan dinamis secara kuantitatif. Struktur pengujian memadukan 3 variabel bebas utama:
1.  **Algoritme SPF Dinamis**: A\*, Bellman-Ford, dan Widest Path.
2.  **Topologi Jaringan**: Ring-5 dan Jellyfish.
3.  **Skenario Kegagalan/Gangguan**:
    *   *Baseline No Failure*: Kondisi kontrol tanpa gangguan untuk mengukur performa puncak jaringan.
    *   *Link Down Before Traffic*: Memutuskan link utama (s1-s2) sebelum lalu lintas data dimulai. Menguji kemampuan konvergensi statis pengendali.
    *   *Link Down During Traffic*: Memutuskan link utama (s1-s2) pada detik ke-1 saat transmisi iperf3 berjalan aktif. Menguji *transient loss* dan rerouting dinamis real-time.
    *   *Link Flap*: Mematikan link s1-s2 pada detik ke-1 dan menghidupkannya kembali pada detik ke-3. Menguji konvergensi rute balik dan kestabilan transportasi data.
    *   *Switch Down*: Mematikan switch fisik s1 secara total sebelum traffic dimulai. Menguji *node failure recovery* dan dampaknya pada isolasi host.
    *   *Bandwidth Throttle*: Membatasi bandwidth link s1-s2 dari 1000 Mbps ke 10 Mbps pada detik ke-1. Menguji *link degradation adaptation*.
    *   *Random Link Down (Jellyfish)*: Memutuskan satu link inter-switch acak pada topologi Jellyfish sebelum pengujian. Menguji adaptabilitas rute pada topologi berderajat tinggi.

Alat pengujian yang diintegrasikan dalam testbed terotomatisasi ini meliputi:
*   `iperf3`: Menghasilkan lalu lintas data TCP arah maju dan balik selama 5 detik untuk mengukur throughput aktual dan retransmisi.
*   `pingall`: Mengevaluasi keterhubungan host dan mendeteksi packet loss sebelum skenario traffic dijalankan.
*   `tcpdump`: Menangkap paket mentah (.pcap) pada antarmuka switch untuk keperluan verifikasi pengalihan rute.

---

## 4.5.2 Topologi Jaringan & Parameter Link

> [!IMPORTANT]
> **PETUNJUK PENULISAN TOPOLOGI & LINK:**
> *   Jelaskan parameter tautan (link parameters) yang dipasang pada testbed emulasi Mininet.
> *   Sebutkan kapasitas bandwidth baseline (100 Mbps) dan nilai delay tautan dasar.
> *   Lampirkan cuplikan skrip inisialisasi topologi Mininet (misalnya bagian pembentukan switch dan penambahan link dengan parameter delay/bandwidth) dari `topo-ring5_lab.py` atau `jellyfish_topo.py`. Batasi cuplikan kode maksimal 30 baris.

### [TEMPLAT DRAFT DETAIL TOPOLOGI]
Tautan inter-switch dan tautan akses host dikonfigurasi dengan parameter spesifik pada Mininet untuk mereplikasi kondisi jaringan fisik:
*   **Bandwidth Link Baseline**: Diatur sebesar 100 Mbps untuk semua tautan fisik guna menyamakan kapasitas dasar.
*   **Delay Link**: Diatur sebesar 1 milidetik untuk tautan inter-switch untuk mensimulasikan latensi transmisi fisik minimal.
*   **Tipe Tautan**: Menggunakan tautan berbasis TCLink pada Mininet agar parameter bandwidth dan delay dapat diterapkan secara akurat.

Berikut adalah cuplikan kode inisialisasi pembentukan topologi Ring-5 dari berkas `SPF/topo-ring5_lab.py`:

```python
# CUPLIKAN INI HANYA TEMPLAT, SILAKAN DISESUAIKAN DENGAN KODE AKTUAL
class Ring5Topology(Topo):
    def build(self):
        # Tambahkan 5 Switch
        switches = []
        for i in range(1, 6):
            switches.append(self.addSwitch(f's{i}', dpid=f'{i:016x}'))
            
        # Hubungkan Switch membentuk Lingkaran (Ring-5)
        for i in range(5):
            self.addLink(switches[i], switches[(i+1)%5], 
                         cls=TCLink, bw=100, delay='1ms')
            
        # Tambahkan 2 Host per Switch (Total 10 Host)
        for i in range(5):
            h1 = self.addHost(f'h{2*i+1}', ip=f'10.0.0.{2*i+1}/24')
            h2 = self.addHost(f'h{2*i+2}', ip=f'10.0.0.{2*i+2}/24')
            self.addLink(h1, switches[i], cls=TCLink, bw=100)
            self.addLink(h2, switches[i], cls=TCLink, bw=100)
```

---

## 4.5.3 Prosedur Pengumpulan Data

> [!IMPORTANT]
> **PETUNJUK PENULISAN PROSEDUR PENGUMPULAN DATA:**
> *   Uraikan langkah-langkah eksperimen secara berurutan (*step-by-step*) dari awal hingga akhir agar pembaca dapat mereplikasi pengujian secara mandiri.
> *   Sertakan skema perintah CLI untuk menjalankan skrip testbed `run_live_scenarios.py`.
> *   Jelaskan bagaimana proses ekstraksi log output JSONL dikonversi menjadi CSV dan dibersihkan untuk siap dimuat oleh Jupyter Notebook.

### [TEMPLAT DRAFT PROSEDUR]
Prosedur eksekusi pengujian otomatis dan pengumpulan data dilakukan melalui tahapan-tahapan berikut:

1.  **Persiapan Lingkungan**: Menjalankan kontainer Docker yang telah diinstalasi Mininet dan OS-Ken Controller.
2.  **Inisialisasi Testbed**: Menjalankan skrip `run_live_scenarios.py` untuk mengotomatisasi inisialisasi topologi, menjalankan pengendali dinamis, memicu event kegagalan, dan mencatat data performa. Perintah eksekusi pengujian:
    ```bash
    python3 SPF/testing-code/run_live_scenarios.py \
      --topologies ring5 jellyfish \
      --algorithms astar bellman_ford widest_path \
      --max-pairs 20 \
      --repetitions 5 \
      --output SPF/csv/benchmark-results.jsonl
    ```
3.  **Pengumpulan Log Mentah**: Hasil eksekusi setiap repetisi pasangan host dicatat dalam format JSON Lines (JSONL) untuk menjaga integritas data jika eksekusi terputus di tengah jalan.
4.  **Konversi dan Pembersihan Data**: Mengonversi berkas log JSONL mentah menjadi format tabel CSV terstruktur menggunakan modul Python:
    ```bash
    python3 SPF/benchmark_jsonl_to_csv.py \
      SPF/csv/benchmark-results.jsonl \
      SPF/csv/benchmark-results.csv
    ```
5.  **Validasi Data**: Membuka Jupyter Notebook untuk melakukan pengecekan data hilang (*missing values*) pada kolom utama dan memastikan total 3.900 baris data terekam lengkap tanpa duplikasi.
