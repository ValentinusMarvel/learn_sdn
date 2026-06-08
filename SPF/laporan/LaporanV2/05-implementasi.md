# 4.6 Implementasi

> [!TIP]
> **PANDUAN PENULISAN IMPLEMENTASI (Skor Maksimal: 5/5):**
> *   **Panjang**: Total berkisar antara **1–2 halaman** (sekitar 400–600 kata).
> *   **Pembahasan Kode**: Jangan lampirkan seluruh file kode. Tampilkan hanya cuplikan logika kritis (fungsi utama) dengan batas maksimal **30 baris** per cuplikan.
> *   **Kejujuran Akademik**: Uraikan kendala teknis nyata yang dihadapi (seperti inkonsistensi bandwidth JSON vs iperf3 throttling, isolasi node, atau skalabilitas Packet-In) dan jelaskan solusi konkretnya.

---

## 4.6.1 Integrasi dengan Repositori

> [!IMPORTANT]
> **PETUNJUK PENULISAN INTEGRASI REPOSITORI:**
> *   Jelaskan bagaimana struktur kode program proyek diintegrasikan dalam repositori `learn_sdn`.
> *   Sebutkan berkas-berkas utama yang digunakan, seperti berkas pengendali dasar `base_controller.py`, berkas subclasses pengendali algoritme (`astar_osken_controller.py`, `bellman_ford_osken_controller.py`, `widest_path_osken_controller.py`), skrip topologi Mininet, dan berkas modul pustaka routing murni.

### [TEMPLAT DRAFT INTEGRASI REPOSITORI]
Implementasi perutean SPF terintegrasi dengan struktur modular repositori `learn_sdn`. Pengkodean dibagi menjadi beberapa bagian utama:
1.  **Kelas Induk Pengendali (`base_controller.py`)**: Menyediakan kerangka dasar yang menangani penemuan topologi, penanganan event OpenFlow, serta pemasangan flow aturan aliran ke switch.
2.  **Kelas Anak Algoritmik** (`*_osken_controller.py`): Subclasses khusus yang mewarisi fungsi dari `base_controller.py` dan bertugas melakukan overriding pada fungsi `compute_path()` untuk memicu algoritme perutean spesifik.
3.  **Modul Algoritme Routing Murni** (`SPF/algorithms/`): Kode Python terisolasi untuk penyelesaian pencarian rute pada graf terlepas dari dependensi OpenFlow/OS-Ken, memudahkan debugging dan unit testing.
4.  **Skrip Eksperimen Otomatis** (`SPF/testing-code/run_live_scenarios.py`): Mengintegrasikan pengendali dan topologi Mininet serta merekam data performa.

---

## 4.6.2 Modifikasi yang Dilakukan

> [!IMPORTANT]
> **PETUNJUK PENULISAN MODIFIKASI KODE:**
> *   Jelaskan logika modifikasi yang dilakukan pada controller untuk mencapai tujuan proyek:
>     1.  **Fungsi `_packet_in_handler`**: Penanganan paket baru dan pembelajaran alamat MAC host.
>     2.  **Fungsi `_install_unicast_flow` / `install_path`**: Pemasangan flow rule bidirectional (maju-mundur) dengan pendekatan *delete-then-add* untuk menjamin idempotensi.
>     3.  **Fungsi `get_topology_data`**: Penemuan topologi dinamis via LLDP dan pembersihan/re-kalkulasi rute saat terjadi perubahan tautan.
> *   Lampirkan cuplikan kode kritis maksimal 30 baris per fungsi.

### [TEMPLAT DRAFT CUPLIKAN KODE KONTROLER]

#### 1. Mekanisme Rerouting Otomatis (Event LLDP)
Untuk menjamin resiliensi dinamis terhadap kegagalan link, pengendali memantau perubahan topologi signature dan secara proaktif meng-flush flow rule lama serta memasang jalur baru:

```python
# Berkas base_controller.py (maksimal 30 baris)
@set_ev_cls(TOPOLOGY_EVENTS)
def get_topology_data(self, ev):
    # Parse switches dan links aktual dari modul OS-Ken
    sw_list = get_switch(self.topology_api_app, None)
    links_list = get_link(self.topology_api_app, None)
    
    # Validasi perubahan topologi menggunakan signature hash
    new_sig = self._calculate_signature(sw_list, links_list)
    if self.old_sig != new_sig:
        self.old_sig = new_sig
        self._flush_all_flows()             # Hapus flow lama
        self._build_broadcast_tree()        # Bangun spanning tree BFS
        self._reinstall_all_known_routes()  # Rerouting proaktif
```

#### 2. Mekanisme Instalasi Flow Rule Bidirectional
Aturan aliran dipasang secara dua arah pada switch di sepanjang rute untuk memastikan lalu lintas data TCP iperf3 berjalan lancar menggunakan parameter prioritasi:

```python
# Berkas base_controller.py (maksimal 30 baris)
def _install_unicast_flow(self, datapath, in_port, out_port, src_mac, dst_mac):
    parser = datapath.ofproto_parser
    ofproto = datapath.ofproto
    match = parser.OFPMatch(in_port=in_port, eth_src=src_mac, eth_dst=dst_mac)
    actions = [parser.OFPActionOutput(out_port)]
    inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions)]
    
    # Delete-then-add untuk menjamin idempotency saat rerouting
    datapath.send_msg(parser.OFPFlowMod(
        datapath=datapath, cookie=self.FLOW_COOKIE,
        command=ofproto.OFPFC_DELETE_STRICT, priority=FLOW_PRIORITY,
        match=match, out_port=ofproto.OFPP_ANY, out_group=ofproto.OFPG_ANY
    ))
    datapath.send_msg(parser.OFPFlowMod(
        datapath=datapath, cookie=self.FLOW_COOKIE,
        command=ofproto.OFPFC_ADD, priority=FLOW_PRIORITY,
        match=match, instructions=inst
    ))
```

---

## 4.6.3 Kendala Selama Implementasi

> [!IMPORTANT]
> **PETUNJUK PENULISAN KENDALA & SOLUSI:**
> *   Ceritakan secara jujur kegagalan, kendala teknis, atau perilaku anomali yang ditemui selama implementasi dan bagaimana kelompok menyelesaikannya.
> *   *Kendala 1 (Inkonsistensi State)*: Controller membaca data link weights statis dari JSON sehingga tidak menyadari pembatasan bandwidth dinamis dari Mininet (anomali throttling). Solusi teoretis: mengusulkan monitoring QoS dinamis.
> *   *Kendala 2 (Packet-In Bottleneck)*: Overload Packet-In awal saat max_pairs=20 memicu latensi tinggi. Solusi: optimasi cache rute atau pre-computation.
> *   *Kendala 3 (Switch Down Isolation)*: Kegagalan switch memotong koneksi host mutlak sehingga iperf3 error. Solusi: memisahkan analisis data error dengan data sukses agar tidak merusak validitas rata-rata metrik lainnya.

### [TEMPLAT DRAFT KENDALA & SOLUSI]
Selama proses implementasi dan Benchmark pengujian, beberapa kendala teknis penting diidentifikasi:
1.  **Masalah Data Tautan Statis vs Dinamis**:
    *   *Kendala*: Pengendali Bellman-Ford dan Widest Path mengacu pada berkas konfigurasi statis `link_weights.json`. Ketika tautan fisik dibatasi dinamis oleh Mininet pada detik ke-1, pengendali tidak mengetahui penurunan kapasitas tersebut karena tidak adanya dynamic monitoring.
    *   *Solusi*: Menggunakan pendekatan analitik dalam laporan untuk menafsirkan anomali ini sebagai bias representasi matriks biaya, serta mengusulkan penggunaan modul `OFPPortStatsRequest` sebagai perbaikan di masa depan.
2.  **Latensi Akumulasi Packet-In**:
    *   *Kendala*: Pada eksekusi `max_pairs=20`, inisialisasi awal memicu badai Packet-In (*packet-in storm*) saat host-host mulai saling mengirim ARP secara bersamaan. Hal ini memicu antrean kalkulasi rute pada controller dan meningkatkan latensi runtime.
    *   *Solusi*: Dipasang batas waktu *drop flow* timeout selama 5 detik untuk host yang tidak memiliki rute guna mencegah beban komputasi berulang di sisi pengendali.
3.  **Isolasi Host pada Skenario Switch Down**:
    *   *Kendala*: Skenario switch_down pada Ring-5 langsung memutus koneksi host akses secara mutlak, memicu error transmisi iperf3 karena ketiadaan rute fisik.
    *   *Solusi*: Modifikasi skrip Jupyter Notebook analisis data agar memisahkan baris status `error` ke dataset `df_errors` tersendiri, sehingga nilai throughput rata-rata algoritme pada data sukses (`df_ok`) tidak terdistorsi menjadi nol.
