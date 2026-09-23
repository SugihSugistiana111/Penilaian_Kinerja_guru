# DOKUMENTASI LENGKAP USE CASE DIAGRAM (BAB IV SKRIPSI)
## SISTEM PENDUKUNG KEPUTUSAN PENILAIAN KINERJA GURU METODE MOORA
### SMA AL-IHSAN BOARDING SCHOOL

---

## 1. Identifikasi Aktor (Actor Definition)

Berdasarkan audit menyeluruh terhadap implementasi sistem dan skema autentikasi, teridentifikasi 3 (tiga) aktor utama yang berinteraksi langsung dengan sistem:

| No | Nama Aktor | Deskripsi Peran & Hak Akses Aktual |
|---|---|---|
| 1 | **Administrator** | Bertindak sebagai pengelola sistem dan asisten administratif. Memiliki hak akses penuh untuk mengelola pengguna, mengelola data master guru, mengelola kriteria & bobot, mengelola skala penilaian, mengelola periode penilaian, mencatat hasil penilaian evaluasi Kepala Sekolah ke sistem, mengeksekusi perhitungan SPK metode MOORA, melihat pemeringkatan, memantau grafik monitoring kinerja, melihat riwayat penilaian, serta mencetak laporan keputusan penilaian. |
| 2 | **Kepala Sekolah** | Bertindak sebagai penilai utama (*decision maker*). Memiliki hak akses untuk melihat data guru, melakukan penilaian kinerja guru secara langsung, melihat hasil pemeringkatan MOORA, melihat detail perolehan nilai, memantau perkembangan kinerja guru melalui grafik monitoring, melihat riwayat penilaian, serta mencetak laporan keputusan penilaian. |
| 3 | **Guru** | Bertindak sebagai pihak yang dievaluasi (*evaluee*). Memiliki hak akses terbatas untuk masuk ke sistem, melihat nilai perolehan evaluasi diri sendiri, melihat rincian detail penilaian per kriteria, melihat riwayat penilaian mandiri dari periode-periode sebelumnya, serta memantau grafik perkembangan kinerja diri sendiri. |

---

## 2. Identifikasi, Penamaan, dan Pengelompokan Use Case (UC-01 s/d UC-15)

Daftar 15 Use Case fungsional dikelompokkan secara manual ke dalam 3 Area Spatial Presisi (*3-Area Spatial Layout*):

```text
                             [TOP CENTER — AUTENTIKASI]
                               +--------------------------+
                               | UC-01 Melakukan Login    |
                               +--------------------------+

 [AREA KIRI — ADMINISTRATOR]   [AREA TENGAH — INTI & SHARED]   [AREA KANAN — KEPSEK & GURU]
(Khusus Administrator Kiri)      (Proses Inti / Bersama)       (Kepala Sekolah & Guru Kanan)
+--------------------------+  +--------------------------+    +--------------------------+
| UC-02 Data Pengguna      |  | UC-03 Data Guru          |    | UC-15 Cetak Laporan      |
| UC-04 Kriteria & Bobot   |  | UC-07 Penilaian Guru     |    | UC-12 Detail Penilaian   |
| UC-05 Skala Penilaian    |  | UC-10 Pemeringkatan MOORA|    | UC-13 Monitoring Kinerja |
| UC-06 Periode Penilaian  |  | UC-11 Hasil Penilaian    |    | UC-14 Riwayat Penilaian  |
| UC-08 Catat Penilaian    |  +--------------------------+    +--------------------------+
| UC-09 Perhitungan MOORA  |
+--------------------------+
```

### Tabel Rincian Fungsional Use Case

| No | Kode | Nama Use Case | Area Topologi Spatial | Deskripsi Fungsi |
|:--:|:---:|:---|:---|:---|
| 1 | **UC-01** | Melakukan Login | Autentikasi (Top Center) | Proses autentikasi pengguna (Admin, Kepala Sekolah, Guru) untuk masuk ke dalam sistem sesuai role dan hak akses. |
| 2 | **UC-02** | Mengelola Data Pengguna | Area Kiri (Dominan Admin) | Mengelola data akun pengguna (tambah, lihat, ubah status, reset password). |
| 3 | **UC-03** | Mengelola Data Guru | Area Tengah (Admin & Kepsek) | Mengelola dan meninjau data profil guru (NIP, nama, jenis kelamin, rombel, jam ajar). |
| 4 | **UC-04** | Mengelola Kriteria dan Bobot | Area Kiri (Dominan Admin) | Mengatur 4 kriteria evaluasi (Pedagogik, Kepribadian, Sosial, Profesional) beserta bobot preferensi ($W_j$). |
| 5 | **UC-05** | Mengelola Skala Penilaian | Area Kiri (Dominan Admin) | Mengatur skala nilai 1 s/d 5 (Sangat Kurang, Kurang, Cukup, Baik, Sangat Baik). |
| 6 | **UC-06** | Mengelola Periode Penilaian | Area Kiri (Dominan Admin) | Mengatur periode evaluasi (bulan, tahun, status: DRAFT, AKTIF, SELESAI). |
| 7 | **UC-07** | Melakukan Penilaian Kinerja Guru | Area Tengah (Kepsek) | Memberikan skor nilai evaluasi terhadap guru per kriteria pada periode aktif oleh Kepala Sekolah. |
| 8 | **UC-08** | Mencatat Hasil Penilaian | Area Kiri (Dominan Admin) | Mencatat/menginput nilai hasil evaluasi Kepala Sekolah ke dalam sistem oleh Administrator. |
| 9 | **UC-09** | Mengolah Penilaian dengan MOORA | Area Kiri (Dominan Admin) | Menjalankan kalkulasi MOORA otomatis (Matriks Keputusan, Normalisasi Matriks, Nilai Optimasi Multiobjektif $y_i$). |
| 10 | **UC-10** | Melihat Pemeringkatan MOORA | Area Tengah (Admin & Kepsek) | Menampilkan tabel ranking urutan guru terbaik berdasarkan nilai optimasi $y_i$ tertinggi. |
| 11 | **UC-11** | Melihat Hasil Penilaian | Area Tengah (Admin, Kepsek & Guru) | Menampilkan ringkasan hasil nilai kinerja per guru pada periode tertentu. |
| 12 | **UC-12** | Melihat Detail Penilaian | Area Kanan (Kepsek & Guru) | Menampilkan rincian perolehan nilai setiap kriteria beserta predikat capaian. |
| 13 | **UC-13** | Monitoring Kinerja Guru | Area Kanan (Kepsek & Guru) | Menampilkan visualisasi grafik tren perkembangan kinerja antar-periode dan per kriteria. |
| 14 | **UC-14** | Melihat Riwayat Penilaian | Area Kanan (Kepsek & Guru) | Meninjau arsip riwayat penilaian kinerja dari seluruh periode sebelumnya yang telah selesai. |
| 15 | **UC-15** | Mencetak Laporan Penilaian | Area Kanan (Admin & Kepsek) | Mencetak dokumen rekapitulasi penilaian dan keputusan ranking ke format cetak/PDF resmi sekolah. |

---

## 3. Matriks Asosiasi Aktor dan Use Case (Traceability Matrix)

| No | Kode | Nama Use Case | Administrator | Kepala Sekolah | Guru |
|:--:|:---:|:---|:---:|:---:|:---:|
| 1 | UC-01 | Melakukan Login | ✓ | ✓ | ✓ |
| 2 | UC-02 | Mengelola Data Pengguna | ✓ | - | - |
| 3 | UC-03 | Mengelola Data Guru | ✓ | ✓ | - |
| 4 | UC-04 | Mengelola Kriteria dan Bobot | ✓ | - | - |
| 5 | UC-05 | Mengelola Skala Penilaian | ✓ | - | - |
| 6 | UC-06 | Mengelola Periode Penilaian | ✓ | - | - |
| 7 | UC-07 | Melakukan Penilaian Kinerja Guru | - | ✓ | - |
| 8 | UC-08 | Mencatat Hasil Penilaian | ✓ | - | - |
| 9 | UC-09 | Mengolah Penilaian dengan MOORA | ✓ | - | - |
| 10 | UC-10 | Melihat Pemeringkatan MOORA | ✓ | ✓ | - |
| 11 | UC-11 | Melihat Hasil Penilaian | ✓ | ✓ | ✓ |
| 12 | UC-12 | Melihat Detail Penilaian | - | ✓ | ✓ |
| 13 | UC-13 | Monitoring Kinerja Guru | ✓ | ✓ | ✓ |
| 14 | UC-14 | Melihat Riwayat Penilaian | ✓ | ✓ | ✓ |
| 15 | UC-15 | Mencetak Laporan Penilaian | ✓ | ✓ | - |
| **Total Asosiasi** | | | **13** | **9** | **5** |

---

## 4. Evaluasi Kepatuhan Kaidah UML Akademik (10 Kriteria Validasi)

Diagram pada berkas `usecase_diagram.drawio` secara ketat mematuhi 10 kriteria evaluasi skripsi bidang Teknik Informatika:

1. **Notasi Standar UML:** Aktor menggunakan bentuk *stick figure*, Use Case menggunakan bentuk oval/elips, dan *System Boundary* menggunakan bentuk persegi panjang bergaris tegas.
2. **Keterbebasan Asosiasi:** Menggunakan garis asosiasi lurus murni tanpa panah (`endArrow=none`), sesuai kaidah asosiasi dasar UML.
3. **Penyebaran Titik Keluar Vertikal Presisi (*Multipoint Exit Anchoring*):** Garis asosiasi keluar dari tubuh aktor secara teratur (`exitY = 0.10 s/d 0.95`), mengeliminasi pola kipas terpusat.
4. **Isolasi Batas Sistem (*Boundary Isolation*):** 100% dari 15 Use Case berada di dalam *System Boundary*, dan 100% dari 3 Aktor berada di luar *System Boundary*.
5. **Jarak Bebas Judul (*Spasial Header Clearance*):** Judul *System Boundary* diberikan ruang vertikal bebas 55px di atas `UC-01 Login` sehingga tidak ada bentrokan teks.
6. **Bebas Komponen Teknis:** Tanpa tabel database, class, API, controller, service, framework, atau komponen teknis internal program.
7. **Bebas Notasi Non-UML:** Tanpa notasi Flowchart, Activity, ERD, atau Sequence Diagram.
8. **Penggunaan Relationship <<include>> dan <<extend>> Yang Valid:** Hanya digunakan jika ada dasar fungsionalitas murni, tanpa memaksa dekorasi diagram.
9. **Kerapihan & Proporsi Cetak A4 Landscape:** Tersusun dalam 3 poros spatial (`x = 220`, `x = 520`, `x = 820`) yang seimbang, simetris, dan mudah dibaca saat dicetak.
10. **Format Formal Monokrom:** Menggunakan skema warna formal hitam-putih (`#ffffff`/`#000000`), font *Times New Roman*, tanpa gradien, tanpa efek 3D, dan tanpa ikon dekoratif non-standar.
