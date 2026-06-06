# Analysis Notebook Pipeline — CSV from Scenario Runs

**Purpose**: Dokumen ini menjelaskan pipeline analisis yang akan diimplementasikan di Python notebook untuk membaca CSV hasil `run_live_scenarios`, mengagregasi metrik, dan membuat visualisasi perbandingan yang siap dipakai di laporan.

**Scope**: CSV hasil scenario-mode dan file pendamping yang berasal dari `SPF/testing-code/run_live_scenarios.py`, `SPF/benchmark_jsonl_to_csv.py`, dan `SPF/testing-code/pcap_to_csv.py`.

**Status**: Planning document

---

## 1. Goal Statement

Notebook harus menjadi lapisan analisis yang reprodusibel di atas hasil CSV, bukan tempat untuk menjalankan eksperimen. Artinya, notebook fokus pada:

- membaca CSV hasil run,
- menyatukan metadata run dan record-level,
- menghitung ringkasan statistik,
- membandingkan topology, algorithm, dan scenario,
- menghasilkan plot dan tabel ringkas untuk laporan.

### Target Outcome
- Satu notebook yang bisa dijalankan ulang dari CSV mentah.
- Visualisasi yang konsisten untuk throughput, hop count, runtime, packet loss, dan recovery-related metrics.
- Output tabel agregasi yang bisa diekspor ke CSV baru atau dipakai langsung di laporan.
- Pemisahan jelas antara data mentah, data bersih, dan hasil agregasi.

---

## 2. Input Data Contract

Notebook ini mengonsumsi CSV yang sudah dihasilkan oleh pipeline scenario-mode. Sumber utama yang perlu dibaca adalah:

- `SPF/csv/pcap-csv/<topology>/<algorithm>/<scenario>/<host>.csv` untuk bukti packet-level dari PCAP.
- CSV hasil konversi scenario summary bila tersedia dari JSONL output `run_live_scenarios`.
- Run log Markdown bila ingin menyertakan metadata eksekusi, seperti command line, git commit, dan controller log path.

### Data Yang Perlu Dipertahankan
Notebook tidak boleh kehilangan pemisahan berikut:

- **Record-level data**: source/destination host, hop count, runtime, throughput, scenario, packet loss, dan path-related fields.
- **Run-level metadata**: command line, git branch, git commit, output dir, pcap dir, controller log path, seed, dan timestamp run.

### Minimal Schema Yang Diharapkan
Kolom yang idealnya tersedia atau bisa diturunkan dari CSV:

- `benchmark_mode`
- `run_id`
- `topology`
- `algorithm`
- `scenario_name`
- `scenario_phase`
- `source_host`
- `destination_host`
- `source_switch`
- `destination_switch`
- `hop_count`
- `path_cost`
- `runtime_ms`
- `throughput_mbps`
- `pingall_loss_pct`
- `tcpdump_pcap_paths`
- `tcpdump_csv_paths`
- `status`
- `error`
- `note`

Jika satu atau dua kolom tidak tersedia di CSV yang dipakai, notebook harus menandai itu sebagai gap data, bukan mengisi asumsi diam-diam.

---

## 3. Notebook Pipeline

### Cell 1: Imports and Config
Tujuan cell ini adalah menyiapkan library dan path dasar.

Contoh isi:
- `pandas` untuk load dan agregasi data.
- `matplotlib` atau `seaborn` untuk plot.
- `pathlib.Path` untuk navigasi folder.
- Konfigurasi folder input CSV dan folder output gambar/tabel.

Output yang diharapkan:
- semua path input tervalidasi,
- notebook tahu topology dan scenario mana yang akan dianalisis,
- style plot sudah diset konsisten.

### Cell 2: Discover Inputs
Cell ini mendeteksi file CSV yang tersedia.

Langkah:
- scan `SPF/csv/pcap-csv/` recursively,
- kelompokkan file berdasarkan topology, algorithm, scenario, dan host,
- jika ada CSV summary lain, baca juga dengan pola nama file yang konsisten.

Output yang diharapkan:
- daftar file yang akan dianalisis,
- tabel inventory singkat berisi jumlah file per topology/algorithm/scenario.

### Cell 3: Load and Validate
Cell ini membaca CSV ke `DataFrame`.

Langkah:
- baca semua CSV yang relevan,
- standardisasi nama kolom ke snake_case yang konsisten,
- parse timestamp bila tersedia,
- validasi kolom wajib,
- tandai missing columns atau malformed rows.

Aturan:
- row yang rusak tidak boleh diam-diam dibuang tanpa jejak,
- jika ada file kosong, notebook harus memberi warning yang jelas,
- error parsing harus diringkas per file.

### Cell 4: Normalize and Enrich
Cell ini menggabungkan data dari file-file yang terpisah.

Langkah:
- tambahkan kolom turunan untuk grouping,
- derive `pair_id` dari source/destination host,
- derive `scenario_group` bila diperlukan,
- satukan record-level metadata dengan run-level metadata bila tersedia.

Contoh enrichment:
- `algorithm_family` untuk membedakan single-path vs multipath bila nanti dipakai,
- `host_pair` untuk mempermudah agregasi,
- `duration_bucket` bila ingin analisis per window.

### Cell 5: Compute Summary Statistics
Cell ini menghasilkan metrik agregat yang akan dipakai pada plot.

Agregasi yang disarankan:
- mean, median, min, max, std untuk `throughput_mbps`.
- mean dan std untuk `runtime_ms`.
- mean `hop_count` dan `path_cost`.
- packet loss rata-rata per scenario.
- jumlah record sukses vs gagal per kombinasi topology/algorithm/scenario.

Group-by yang paling penting:
- `topology`
- `algorithm`
- `scenario_name`
- `scenario_phase`
- `source_host` dan `destination_host` bila ingin detail pair-level.

### Cell 6: Build Comparison Tables
Cell ini menyiapkan tabel final untuk dibaca cepat.

Tabel yang disarankan:
- per topology: ranking algorithm berdasarkan throughput dan runtime,
- per scenario: perubahan throughput sebelum/during/setelah failure,
- per host pair: record-level summary untuk investigasi detail,
- per scenario phase: ringkasan packet loss dan recovery timing.

### Cell 7: Visualize
Cell ini menghasilkan plot utama.

Plot yang disarankan:
- bar plot throughput per algorithm per topology,
- bar plot runtime per algorithm,
- box plot throughput per scenario,
- line plot atau slope chart untuk membandingkan pre-failure vs post-failure,
- heatmap packet loss atau recovery time bila data cukup.

Prinsip visual:
- satu plot untuk satu pertanyaan,
- label sumbu eksplisit,
- legend singkat,
- warna konsisten untuk algorithm yang sama di semua plot.

### Cell 8: Export Results
Cell ini menyimpan output turunan.

Output yang disarankan:
- CSV ringkasan agregasi,
- PNG atau SVG plot,
- tabel markdown untuk laporan,
- optional JSON summary untuk integrasi laporan otomatis.

Contoh folder output:
- `SPF/csv/analysis/`
- `SPF/img/analysis/`

---

## 4. Recommended Analysis Questions

Notebook ini sebaiknya menjawab pertanyaan berikut:

- Algoritma mana yang paling stabil pada throughput?
- Apakah topology tertentu menunjukkan packet loss lebih tinggi saat failure?
- Apakah runtime algoritma berkorelasi dengan throughput aktual?
- Bagaimana performa sebelum, saat, dan setelah failure terjadi?
- Apakah record yang gagal terkonsentrasi pada scenario tertentu?
- Apakah hasil berbeda secara material antar host pair?

---

## 5. Visualization Set

### Core Views
- **Throughput by Algorithm**: membandingkan `throughput_mbps` per algorithm.
- **Runtime by Algorithm**: membandingkan `runtime_ms` per algorithm.
- **Packet Loss by Scenario**: melihat impact failure terhadap loss.
- **Recovery View**: membandingkan phase `pre`, `during`, dan `post` bila tersedia.
- **Host Pair Detail**: tabel investigasi untuk satu pair yang bermasalah.

### Optional Views
- **Correlation plot** untuk melihat hubungan runtime dan throughput.
- **Distribution plot** untuk variasi antar repetition.
- **Top-N anomalies table** untuk record dengan loss atau error terbesar.

---

## 6. Validation Checklist

- [ ] Semua file CSV yang diharapkan berhasil ditemukan.
- [ ] Kolom wajib tervalidasi.
- [ ] Missing metadata ditandai sebagai gap, bukan disembunyikan.
- [ ] Agregasi menghasilkan tabel yang konsisten.
- [ ] Plot bisa direproduksi dari input CSV yang sama.
- [ ] Output analisis disimpan ke folder yang jelas.
- [ ] Notebook tidak mencampur data dari run berbeda tanpa `run_id` atau metadata pembeda.

---

## 7. Implementation Notes

- Notebook harus cukup ringan untuk dipakai ulang oleh reviewer.
- Jangan hard-code hanya satu topology atau satu scenario jika folder input sudah mengandung banyak kombinasi.
- Jika output CSV berasal dari banyak run, prioritaskan filter eksplisit berdasarkan `topology`, `algorithm`, dan `scenario_name`.
- Bila notebook memakai data packet-level dari `pcap-csv`, pertahankan nama host dan scenario agar tracing ke PCAP tetap mungkin.
- Jika ada gap di pipeline upstream, tandai di notebook sebagai limitation, bukan asumsi hasil.

---

## 8. Downstream Artifact

Dokumen ini adalah kontrak pipeline untuk notebook analisis yang akan dibangun di Python. Implementasi notebook yang disarankan adalah:

- `SPF/analysis/plot_results.ipynb`

Notebook tersebut sebaiknya mengikuti urutan cell di atas agar mudah dirawat dan mudah diaudit.

---

## 9. Summary

Pipeline analisis yang direkomendasikan adalah:

1. Load CSV hasil scenario run.
2. Validasi schema dan metadata.
3. Normalisasi data ke format analisis.
4. Hitung agregasi per topology, algorithm, dan scenario.
5. Visualisasikan metrik utama.
6. Ekspor tabel dan gambar untuk laporan.

Dengan alur ini, hasil `run_live_scenarios` bisa langsung dipakai untuk analisis notebook tanpa parsing manual ulang.
