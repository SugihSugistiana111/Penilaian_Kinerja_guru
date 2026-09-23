# BAB IV: HASIL DAN PEMBAHASAN
## 4.3 Perancangan Struktur Tabel Basis Data

Perancangan basis data pada Sistem Pendukung Keputusan (SPK) Penilaian Kinerja Guru dengan metode MOORA di SMA Al-Ihsan Boarding School terdiri dari 11 (sebelas) tabel utama:

### 4.3.1 Struktur Tabel Role (tbl_role)

Tabel Role digunakan untuk menyimpan data tingkat hak akses atau peran pengguna dalam sistem (Administrator, Kepala Sekolah, dan Guru). Memiliki Primary Key `id`.

**Tabel 4.1. Struktur Tabel Role (tbl_role)**

| No | Field | Type | Size | Keterangan |
| :---: | :--- | :---: | :---: | :--- |
| 1 | `id` *(PK)* | VARCHAR | 30 | Primary Key, Identifier unik peran pengguna (CUID) |
| 2 | `namaRole` | VARCHAR | 50 | Nama hak akses pengguna (ADMIN, KEPALA_SEKOLAH, GURU), Unique |

---

### 4.3.2 Struktur Tabel User (tbl_user)

Tabel User digunakan untuk menyimpan data kredensial akun pengguna sistem untuk keperluan autentikasi dan otorisasi login. Memiliki Primary Key `id` dan Foreign Key `roleId -> Role(id), guruId -> Guru(id)`.

**Tabel 4.2. Struktur Tabel User (tbl_user)**

| No | Field | Type | Size | Keterangan |
| :---: | :--- | :---: | :---: | :--- |
| 1 | `id` *(PK)* | VARCHAR | 30 | Primary Key, Identifier unik akun pengguna (CUID) |
| 2 | `nama` | VARCHAR | 100 | Nama lengkap pengguna |
| 3 | `username` | VARCHAR | 50 | Username unik untuk autentikasi login (Unique) |
| 4 | `password` | VARCHAR | 255 | Password akun pengguna terenkripsi (Hash/Bcrypt) |
| 5 | `roleId` | VARCHAR | 30 | Foreign Key mengacu pada tabel Role (id) |
| 6 | `guruId` | VARCHAR | 30 | Foreign Key mengacu pada tabel Guru (id), Nullable |
| 7 | `status` | BOOLEAN | - | Status keaktifan akun pengguna (Default: true) |
| 8 | `createdAt` | DATETIME | - | Waktu pencatatan/pembuatan akun pengguna |
| 9 | `updatedAt` | DATETIME | - | Waktu pembaruan data pengguna terakhir |

---

### 4.3.3 Struktur Tabel Guru (tbl_guru)

Tabel Guru digunakan untuk menyimpan data master identitas guru, penugasan mengajar, dan beban kerja yang menjadi alternatif dalam penilaian kinerja. Memiliki Primary Key `id`.

**Tabel 4.3. Struktur Tabel Guru (tbl_guru)**

| No | Field | Type | Size | Keterangan |
| :---: | :--- | :---: | :---: | :--- |
| 1 | `id` *(PK)* | VARCHAR | 30 | Primary Key, Identifier unik data guru (CUID) |
| 2 | `nip` | VARCHAR | 30 | Nomor Induk Pegawai / NIK Guru (Unique) |
| 3 | `nama` | VARCHAR | 100 | Nama lengkap guru beserta gelar |
| 4 | `jenisKelamin` | VARCHAR | 10 | Jenis kelamin guru (L = Laki-laki / P = Perempuan) |
| 5 | `jabatanTugasMengajar` | VARCHAR | 100 | Mata pelajaran yang diampu / penugasan dinas |
| 6 | `tugasTambahanUtama` | VARCHAR | 100 | Tugas tambahan utama (e.g. Wali Kelas), Nullable |
| 7 | `tugasTambahanLain` | VARCHAR | 100 | Tugas tambahan lain yang diemban guru, Nullable |
| 8 | `jumlahSiswaPerRombel` | INTEGER | 4 | Rata-rata jumlah siswa per rombongan belajar |
| 9 | `jumlahJamAjar` | INTEGER | 4 | Total jam beban tatap muka mengajar per minggu |
| 10 | `mengajarKelas10` | BOOLEAN | - | Status mengajar kelas 10 (Default: false) |
| 11 | `mengajarKelas11` | BOOLEAN | - | Status mengajar kelas 11 (Default: false) |
| 12 | `mengajarKelas12` | BOOLEAN | - | Status mengajar kelas 12 (Default: false) |
| 13 | `statusAktif` | BOOLEAN | - | Status keaktifan status guru (Default: true) |
| 14 | `createdAt` | DATETIME | - | Waktu pertama kali data guru didaftarkan |
| 15 | `updatedAt` | DATETIME | - | Waktu pembaruan profil data guru terakhir |

---

### 4.3.4 Struktur Tabel Kriteria (tbl_kriteria)

Tabel Kriteria digunakan untuk mengelola data kriteria penilaian kinerja guru beserta bobot preferensi dan kategori sifat atribut MOORA (Benefit atau Cost). Memiliki Primary Key `id`.

**Tabel 4.4. Struktur Tabel Kriteria (tbl_kriteria)**

| No | Field | Type | Size | Keterangan |
| :---: | :--- | :---: | :---: | :--- |
| 1 | `id` *(PK)* | VARCHAR | 30 | Primary Key, Identifier unik kriteria penilaian (CUID) |
| 2 | `kode` | VARCHAR | 10 | Kode identifikasi kriteria (C1, C2, C3, C4, dst), Unique |
| 3 | `nama` | VARCHAR | 100 | Nama kriteria evaluasi kinerja guru |
| 4 | `bobot` | FLOAT | - | Nilai bobot preferensi kriteria (Rentang 0.00 - 1.00) |
| 5 | `jenis` | VARCHAR | 10 | Sifat kriteria dalam metode MOORA (BENEFIT / COST) |
| 6 | `status` | BOOLEAN | - | Status keaktifan kriteria dalam penilaian (Default: true) |
| 7 | `createdAt` | DATETIME | - | Waktu penambahan data kriteria |
| 8 | `updatedAt` | DATETIME | - | Waktu pembaruan konfigurasi kriteria terakhir |

---

### 4.3.5 Struktur Tabel Skala Penilaian (tbl_skala_penilaian)

Tabel Skala Penilaian digunakan untuk menyimpan rubrik tingkatan skor penilaian (sub-kriteria) dan indikator ketercapaian kompetensi. Memiliki Primary Key `id` dan Foreign Key `kriteriaId -> Kriteria(id)`.

**Tabel 4.5. Struktur Tabel Skala Penilaian (tbl_skala_penilaian)**

| No | Field | Type | Size | Keterangan |
| :---: | :--- | :---: | :---: | :--- |
| 1 | `id` *(PK)* | VARCHAR | 30 | Primary Key, Identifier unik skala nilai (CUID) |
| 2 | `kriteriaId` | VARCHAR | 30 | Foreign Key mengacu pada tabel Kriteria (id), Nullable |
| 3 | `nilai` | INTEGER | 2 | Tingkatan skor kuantitatif rubrik (Nilai 1 - 5) |
| 4 | `label` | VARCHAR | 50 | Label predikat (Sangat Baik, Baik, Cukup, Kurang, Sangat Kurang) |
| 5 | `keterangan` | TEXT | - | Deskripsi indikator ketercapaian rubrik penilaian, Nullable |

---

### 4.3.6 Struktur Tabel Periode Penilaian (tbl_periode_penilaian)

Tabel Periode Penilaian digunakan untuk mencatat dan mengorganisir gelombang evaluasi kinerja guru berkala (bulanan/semesteran/tahunan). Memiliki Primary Key `id`.

**Tabel 4.6. Struktur Tabel Periode Penilaian (tbl_periode_penilaian)**

| No | Field | Type | Size | Keterangan |
| :---: | :--- | :---: | :---: | :--- |
| 1 | `id` *(PK)* | VARCHAR | 30 | Primary Key, Identifier unik periode penilaian (CUID) |
| 2 | `bulan` | VARCHAR | 20 | Nama bulan pelaksanaan evaluasi (Januari - Desember) |
| 3 | `tahun` | INTEGER | 4 | Tahun pelaksanaan evaluasi (e.g. 2026) |
| 4 | `namaPeriode` | VARCHAR | 50 | Label nama periode evaluasi (e.g. 'Juni 2026') |
| 5 | `status` | VARCHAR | 20 | Status operasional periode (DRAFT, AKTIF, SELESAI) |
| 6 | `createdAt` | DATETIME | - | Waktu pembuatan agenda periode |
| 7 | `updatedAt` | DATETIME | - | Waktu pembaruan status periode |

---

### 4.3.7 Struktur Tabel Penilaian (tbl_penilaian)

Tabel Penilaian digunakan untuk menyimpan data transaksi evaluasi kinerja setiap guru pada periode penilaian tertentu. Memiliki Primary Key `id` dan Foreign Key `guruId -> Guru(id), periodeId -> PeriodePenilaian(id)`.

**Tabel 4.7. Struktur Tabel Penilaian (tbl_penilaian)**

| No | Field | Type | Size | Keterangan |
| :---: | :--- | :---: | :---: | :--- |
| 1 | `id` *(PK)* | VARCHAR | 30 | Primary Key, Identifier transaksi penilaian (CUID) |
| 2 | `guruId` | VARCHAR | 30 | Foreign Key mengacu pada tabel Guru (id) |
| 3 | `periodeId` | VARCHAR | 30 | Foreign Key mengacu pada tabel PeriodePenilaian (id) |
| 4 | `dinilaiOleh` | VARCHAR | 100 | Nama evaluator/penilai (e.g. Kepala Sekolah), Nullable |
| 5 | `status` | VARCHAR | 20 | Status status evaluasi (DRAFT / SELESAI) |
| 6 | `catatan` | TEXT | - | Catatan kualitatif saran dan evaluasi penilai, Nullable |
| 7 | `createdAt` | DATETIME | - | Waktu perekaman entri penilaian |
| 8 | `updatedAt` | DATETIME | - | Waktu perubahan skor atau catatan penilaian |

---

### 4.3.8 Struktur Tabel Detail Penilaian (tbl_detail_penilaian)

Tabel Detail Penilaian digunakan untuk menyimpan rincian skor nilai asli (raw score) pada masing-masing kriteria untuk setiap guru. Memiliki Primary Key `id` dan Foreign Key `penilaianId -> Penilaian(id), kriteriaId -> Kriteria(id)`.

**Tabel 4.8. Struktur Tabel Detail Penilaian (tbl_detail_penilaian)**

| No | Field | Type | Size | Keterangan |
| :---: | :--- | :---: | :---: | :--- |
| 1 | `id` *(PK)* | VARCHAR | 30 | Primary Key, Identifier unik detail penilaian (CUID) |
| 2 | `penilaianId` | VARCHAR | 30 | Foreign Key mengacu pada tabel Penilaian (id) |
| 3 | `kriteriaId` | VARCHAR | 30 | Foreign Key mengacu pada tabel Kriteria (id) |
| 4 | `nilai` | FLOAT | - | Nilai skor kriteria yang diberikan penilai (Skala 1.0 - 5.0) |

---

### 4.3.9 Struktur Tabel Hasil MOORA (tbl_hasil_moora)

Tabel Hasil MOORA digunakan untuk menyimpan nilai akhir preferensi optimasi multiobjektif (Yi) dan urutan peringkat (ranking) kinerja guru. Memiliki Primary Key `id` dan Foreign Key `guruId -> Guru(id), periodeId -> PeriodePenilaian(id)`.

**Tabel 4.9. Struktur Tabel Hasil MOORA (tbl_hasil_moora)**

| No | Field | Type | Size | Keterangan |
| :---: | :--- | :---: | :---: | :--- |
| 1 | `id` *(PK)* | VARCHAR | 30 | Primary Key, Identifier unik hasil kalkulasi MOORA (CUID) |
| 2 | `guruId` | VARCHAR | 30 | Foreign Key mengacu pada tabel Guru (id) |
| 3 | `periodeId` | VARCHAR | 30 | Foreign Key mengacu pada tabel PeriodePenilaian (id) |
| 4 | `nilaiPreferensi` | FLOAT | - | Nilai akhir preferensi MOORA (Nilai Yi = Max Benefit - Min Cost) |
| 5 | `ranking` | INTEGER | 4 | Urutan ranking kinerja guru berdasarkan nilai preferensi tertinggi |
| 6 | `createdAt` | DATETIME | - | Waktu pemrosesan kalkulasi SPK MOORA |

---

### 4.3.10 Struktur Tabel Detail MOORA (tbl_detail_moora)

Tabel Detail MOORA digunakan untuk menyimpan jejak matriks per kriteria (matriks keputusan X, matriks ternormalisasi X*, bobot W, dan matriks terbobot). Memiliki Primary Key `id` dan Foreign Key `hasilMooraId -> HasilMoora(id), kriteriaId -> Kriteria(id)`.

**Tabel 4.10. Struktur Tabel Detail MOORA (tbl_detail_moora)**

| No | Field | Type | Size | Keterangan |
| :---: | :--- | :---: | :---: | :--- |
| 1 | `id` *(PK)* | VARCHAR | 30 | Primary Key, Identifier unik detail matriks MOORA (CUID) |
| 2 | `hasilMooraId` | VARCHAR | 30 | Foreign Key mengacu pada tabel HasilMoora (id) |
| 3 | `kriteriaId` | VARCHAR | 30 | Foreign Key mengacu pada tabel Kriteria (id) |
| 4 | `nilaiAwal` | FLOAT | - | Nilai asli skor kriteria (Matriks Keputusan Xij) |
| 5 | `nilaiNormalisasi` | FLOAT | - | Nilai matriks setelah normalisasi vektor MOORA (X*ij) |
| 6 | `bobot` | FLOAT | - | Bobot preferensi kriteria yang diaplikasikan (Wj) |
| 7 | `nilaiTerbobot` | FLOAT | - | Nilai matriks setelah dikalikan bobot kriteria (Wj * X*ij) |

---

### 4.3.11 Struktur Tabel Log Aktivitas (tbl_log_aktivitas)

Tabel Log Aktivitas digunakan untuk mencatat riwayat audit trail setiap tindakan pengguna pada sistem guna menjaga keamanan data. Memiliki Primary Key `id` dan Foreign Key `userId -> User(id)`.

**Tabel 4.11. Struktur Tabel Log Aktivitas (tbl_log_aktivitas)**

| No | Field | Type | Size | Keterangan |
| :---: | :--- | :---: | :---: | :--- |
| 1 | `id` *(PK)* | VARCHAR | 30 | Primary Key, Identifier unik log aktivitas (CUID) |
| 2 | `userId` | VARCHAR | 30 | Foreign Key mengacu pada tabel User (id), Nullable |
| 3 | `aktivitas` | VARCHAR | 255 | Deskripsi aktivitas atau transaksi yang dijalankan pengguna |
| 4 | `modul` | VARCHAR | 100 | Nama modul sistem terkait (e.g. Master Guru, Penilaian, MOORA) |
| 5 | `dataId` | VARCHAR | 50 | Identifier rekaman data yang dimanipulasi, Nullable |
| 6 | `waktu` | DATETIME | - | Waktu pencatatan aktivitas berlangsung (Timestamp) |
| 7 | `alamatIp` | VARCHAR | 50 | Alamat IP perangkat pengguna (IP Address), Nullable |

---

