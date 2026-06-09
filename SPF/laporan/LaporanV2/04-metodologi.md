# BAB III METODOLOGI

## 3.1 Perancangan Eksperimen

Eksperimen dirancang untuk mengevaluasi performa dan ketahanan jaringan SDN secara kuantitatif dengan mengkombinasikan tiga variabel bebas utama: algoritme SPF, topologi jaringan, dan skenario kegagalan. Kombinasi lengkap pengujian adalah: **2 topologi** (Ring-5 dan Jellyfish) x **3 algoritme** (A\*, Bellman-Ford, dan Widest Path) x **7 skenario kegagalan** x **20 pasangan host** x **5 repetisi**, menghasilkan total **3.900 baris data pengujian empiris**.

Ketujuh skenario kegagalan yang dirancang adalah sebagai berikut:

| No | Nama Skenario | Deskripsi | Tujuan Pengujian |
|:-:|:---|:---|:---|
| 1 | *Baseline No Failure* | Kondisi kontrol tanpa gangguan apa pun. | Mengukur performa puncak sebagai acuan (*baseline*). |
| 2 | *Link Down Before Traffic* | Memutuskan tautan s1-s2 sebelum lalu lintas data dimulai. | Menguji konvergensi statis pengendali dan kemampuan pre-routing. |
| 3 | *Link Down During Traffic* | Memutuskan tautan s1-s2 pada detik ke-1 saat transmisi iperf3 aktif. | Menguji *transient loss* dan kemampuan rerouting dinamis secara real-time. |
| 4 | *Link Flap* | Mematikan tautan s1-s2 pada detik ke-1 dan menghidupkannya kembali pada detik ke-3. | Menguji konvergensi rute bolak-balik dan stabilitas transportasi data. |
| 5 | *Switch Down* | Mematikan switch s1 secara total sebelum lalu lintas dimulai. | Menguji dampak kegagalan node terhadap isolasi host. |
| 6 | *Bandwidth Throttle* | Membatasi bandwidth tautan s1-s2 dari 100 Mbps menjadi 10 Mbps pada detik ke-1. | Menguji kemampuan algoritme mendeteksi dan menghindari tautan dengan kapasitas terdegradasi. |
| 7 | *Random Link Down Jellyfish* | Memutuskan satu tautan inter-switch acak pada topologi Jellyfish sebelum pengujian. | Menguji adaptabilitas algoritme pada topologi berderajat tinggi dengan kegagalan tidak terduga. |

Alat pengujian yang diintegrasikan dalam testbed terotomatisasi meliputi:

*   **iperf3** [4]: Menghasilkan lalu lintas data TCP selama 5 detik per pasangan host, mengukur throughput aktual (Mbps) dan jumlah retransmisi TCP.
*   **pingall**: Mengevaluasi keterhubungan antar-host dan mendeteksi persentase packet loss sebelum sesi iperf3 dijalankan.
*   **tcpdump**: Menangkap paket mentah dalam format `.pcap` pada antarmuka switch untuk verifikasi pengalihan rute dan analisis paket lebih mendalam.

---

## 3.2 Topologi Jaringan dan Parameter Tautan

Kedua topologi dibangun menggunakan Mininet [2] dengan parameter tautan yang dikonfigurasi secara konsisten untuk menyamakan kondisi *baseline* antar topologi.

**Parameter Tautan Inter-Switch:**

| Parameter | Nilai |
|:---|:---:|
| Bandwidth *baseline* | 100 Mbps |
| Delay | 2 ms |
| Tipe Tautan | TCLink (HFSC *enabled*) |
| Protokol Switch | OpenFlow 1.3 |

Topologi Ring-5 diimplementasikan dalam file `SPF/topo-ring5_lab.py`. Berikut adalah cuplikan kode inisialisasi topologi Ring-5 yang aktual, menampilkan pembentukan switch, host, dan penambahan tautan inter-switch dengan parameter bandwidth dan delay:

```python
# Berkas: SPF/topo-ring5_lab.py (Kelas Ring5Topo, 40 baris kritis)
class Ring5Topo(Topo):
    """5-switch ring topology with 10 hosts (2 per switch)."""

    def addSwitch(self, name, **opts):
        kwargs = {"protocols": "OpenFlow13"}
        kwargs.update(opts)
        return super(Ring5Topo, self).addSwitch(name, **kwargs)

    def __init__(self):
        Topo.__init__(self)
        # Tambahkan 10 Host (2 per Switch)
        h1  = self.addHost("h1",  ip="10.0.0.1/24")
        h2  = self.addHost("h2",  ip="10.0.0.2/24")
        h3  = self.addHost("h3",  ip="10.0.0.3/24")
        h4  = self.addHost("h4",  ip="10.0.0.4/24")
        h5  = self.addHost("h5",  ip="10.0.0.5/24")
        # ... (h6 s.d. h10 serupa, dipersingkat)
        # Tambahkan 5 Switch (OpenFlow 1.3)
        s1 = self.addSwitch("s1")
        s2 = self.addSwitch("s2")
        s3 = self.addSwitch("s3")
        s4 = self.addSwitch("s4")
        s5 = self.addSwitch("s5")
        # Koneksi Host ke Switch (port akses)
        self.addLink(s1, h1, port1=1, port2=1)
        self.addLink(s1, h2, port1=2, port2=1)
        self.addLink(s2, h3, port1=1, port2=1)
        # ... (s3, s4, s5 serupa)
        # Tautan Inter-Switch Membentuk Lingkaran (Ring)
        # Semua tautan: 100 Mbps, 2ms delay, HFSC enabled
        self.addLink(s1, s2, port1=3, port2=3, bw=100, delay="2ms", use_hfsc=True)
        self.addLink(s2, s3, port1=4, port2=3, bw=100, delay="2ms", use_hfsc=True)
        self.addLink(s3, s4, port1=4, port2=3, bw=100, delay="2ms", use_hfsc=True)
        self.addLink(s4, s5, port1=4, port2=3, bw=100, delay="2ms", use_hfsc=True)
        self.addLink(s5, s1, port1=4, port2=4, bw=100, delay="2ms", use_hfsc=True)
```

Diagram topologi Ring-5 yang dihasilkan dari kode di atas adalah sebagai berikut:

```
        h1   h3   h5   h7   h9
        |    |    |    |    |
       s1---s2---s3---s4---s5
        |    |    |    |    |
        h2   h4   h6   h8   h10
        \_______________________/
              (ring: s5-s1)
```

---

## 3.3 Prosedur Pengumpulan Data

Prosedur eksekusi pengujian otomatis dan pengumpulan data dilakukan melalui tahapan yang berurutan dan dapat direplikasi oleh pihak lain:

**Langkah 1: Persiapan Lingkungan**

Jalankan kontainer Docker yang telah diinstalasi Mininet, OS-Ken, dan semua dependensi Python yang diperlukan. Repositori `learn_sdn` harus sudah di-*clone* di dalam kontainer.

**Langkah 2: Eksekusi Testbed Otomatis**

Jalankan skrip `benchmark_core.py` untuk mengotomatisasi inisialisasi topologi, aktivasi pengendali, pemicuan skenario kegagalan, dan pencatatan data performa. Skrip ini menangani semua langkah secara mandiri:

```bash
# Contoh eksekusi untuk topologi Ring-5 dengan Bellman-Ford
sudo python3 SPF/testing-code/run_live_scenarios.py \
  --topologies ring5 \
  --algorithms bellman_ford \
  --scenarios baseline_no_failure link_down_before_traffic link_down_during_traffic link_flap switch_down bandwidth_throttle \
  --max-pairs 20 \
  --repetitions 5 \
  --output SPF/csv/ring5-scenarios.jsonl
```

Proses ini diulang untuk setiap kombinasi `{topo: ring5, jellyfish}` dan `{controller: astar, bellman_ford, widest_path}`.

**Langkah 3: Pengumpulan Log Mentah**

Hasil eksekusi setiap repetisi pasangan host dicatat dalam format JSON Lines (JSONL) ke file `ring5-scenarios.jsonl` dan `jellyfish-scenarios.jsonl`. Format JSONL dipilih karena tahan terhadap interupsi; jika eksekusi terhenti di tengah jalan, data yang sudah terkumpul tetap valid dan tidak rusak.

**Langkah 4: Konversi ke Format CSV**

File log JSONL dikonversi menjadi tabel CSV terstruktur menggunakan modul konversi khusus:

```bash
python3 SPF/benchmark_jsonl_to_csv.py \
  SPF/csv/ring5-scenarios.jsonl \
  SPF/csv/ring5-scenarios.csv
```

**Langkah 5: Validasi dan Analisis Data**

Jupyter Notebook `analysis/plot_results_executed_final.ipynb` digunakan untuk melakukan pengecekan data hilang (*missing values*), memisahkan baris status `error` dari data sukses, memastikan total 3.900 baris data terekam lengkap, dan mengeksekusi seluruh pipeline analisis statistik serta visualisasi grafis.
