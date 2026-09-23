# BAB IV – PERANCANGAN SISTEM (ACTIVITY DIAGRAM)
## SISTEM PENDUKUNG KEPUTUSAN PENILAIAN KINERJA GURU METODE MOORA

---

## 4.2 Activity Diagram

*Activity Diagram* mendeskripsikan alur kerja (*workflow*) fungsionalitas sistem dari sudut pandang pengguna (*actor*) dan reaksi aplikasi (*system*). Seluruh 15 Activity Diagram dikembangkan secara terpisah untuk merepresentasikan secara presisi 15 Use Case fungsional (`UC-01` s/d `UC-15`). Setiap diagram disusun menggunakan notasi UML akademik formal (*Swimlane Aktor | Sistem*, *Initial Node*, *Control Flow*, *Decision Node*, dan *Activity Final Node*).

---

## Pemetaan Use Case dengan Activity Diagram (AD-01 s/d AD-15)

| Kode Use Case | Kode Activity Diagram | Nama Activity Diagram | Swimlane Aktor | Swimlane Sistem |
|:---:|:---:|:---|:---|:---|
| **UC-01** | **AD-01** | Login | Pengguna (Admin / Kepsek / Guru) | Sistem SPK MOORA |
| **UC-02** | **AD-02** | Mengelola Data Pengguna | Administrator | Sistem SPK MOORA |
| **UC-03** | **AD-03** | Mengelola Data Guru | Administrator / Kepala Sekolah | Sistem SPK MOORA |
| **UC-04** | **AD-04** | Mengelola Kriteria dan Bobot | Administrator | Sistem SPK MOORA |
| **UC-05** | **AD-05** | Mengelola Skala Penilaian | Administrator | Sistem SPK MOORA |
| **UC-06** | **AD-06** | Mengelola Periode Penilaian | Administrator | Sistem SPK MOORA |
| **UC-07** | **AD-07** | Melakukan Penilaian Kinerja Guru | Kepala Sekolah | Sistem SPK MOORA |
| **UC-08** | **AD-08** | Mencatat Hasil Penilaian | Administrator | Sistem SPK MOORA |
| **UC-09** | **AD-09** | Mengolah Penilaian dengan MOORA | Administrator | Sistem SPK MOORA |
| **UC-10** | **AD-10** | Melihat Pemeringkatan MOORA | Administrator / Kepala Sekolah | Sistem SPK MOORA |
| **UC-11** | **AD-11** | Melihat Hasil Penilaian | Pengguna (Admin / Kepsek / Guru) | Sistem SPK MOORA |
| **UC-12** | **AD-12** | Melihat Detail Penilaian | Kepala Sekolah / Guru | Sistem SPK MOORA |
| **UC-13** | **AD-13** | Monitoring Kinerja Guru | Pengguna (Admin / Kepsek / Guru) | Sistem SPK MOORA |
| **UC-14** | **AD-14** | Melihat Riwayat Penilaian | Pengguna (Admin / Kepsek / Guru) | Sistem SPK MOORA |
| **UC-15** | **AD-15** | Mencetak Laporan Penilaian | Administrator / Kepala Sekolah | Sistem SPK MOORA |

---

## Rincian Alur Aktivitas Akademik (AD-01 s/d AD-15)

### AD-01: Activity Diagram Login
* **Swimlane:** Pengguna (Admin / Kepsek / Guru) | Sistem SPK MOORA
* **Alur:**
  1. *Initial Node* $\rightarrow$ Pengguna: **Membuka Halaman Login**.
  2. Sistem: **Menampilkan Formulir Login**.
  3. Pengguna: **Memasukkan Username dan Password & Mengklik Tombol Login**.
  4. Sistem: **Memvalidasi Data Login** (*Decision Node: Data Login Valid?*):
     - **[Tidak Valid]:** Sistem **Menampilkan Pesan Kesalahan** $\rightarrow$ Kembali ke formulir masukan pengguna.
     - **[Valid]:** Sistem **Memverifikasi Hak Akses & Menampilkan Dashboard Sesuai Hak Akses**.
  5. *Activity Final Node*.

---

### AD-02: Activity Diagram Mengelola Data Pengguna
* **Swimlane:** Administrator | Sistem SPK MOORA
* **Alur:**
  1. *Initial Node* $\rightarrow$ Administrator: **Membuka Menu Manajemen Pengguna**.
  2. Sistem: **Menampilkan Data Pengguna**.
  3. Administrator: **Memilih Tindakan (Tambah/Ubah/Hapus) & Memasukkan Data Pengguna**.
  4. Sistem: Memvalidasi masukan (*Decision Node: Data Pengguna Valid?*):
     - **[Tidak Valid]:** Sistem **Menampilkan Pesan Kesalahan Data** $\rightarrow$ Kembali ke formulir.
     - **[Valid]:** Sistem **Menyimpan Perubahan Data Pengguna** $\rightarrow$ **Menampilkan Hasil Pengelolaan Data**.
  5. *Activity Final Node*.

---

### AD-03: Activity Diagram Mengelola Data Guru
* **Swimlane:** Administrator / Kepala Sekolah | Sistem SPK MOORA
* **Alur:**
  1. *Initial Node* $\rightarrow$ Aktor: **Membuka Menu Data Guru**.
  2. Sistem: **Menampilkan Data Guru**.
  3. Aktor: **Memasukkan / Memperbarui Data Guru**.
  4. Sistem: Memvalidasi data guru (*Decision Node: Data Guru Valid?*):
     - **[Tidak Valid]:** Sistem **Menampilkan Pesan Kesalahan Data** $\rightarrow$ Kembali ke formulir.
     - **[Valid]:** Sistem **Menyimpan Perubahan Data Guru** $\rightarrow$ **Menampilkan Hasil Data Guru**.
  5. *Activity Final Node*.

---

### AD-04: Activity Diagram Mengelola Kriteria dan Bobot
* **Swimlane:** Administrator | Sistem SPK MOORA
* **Alur:**
  1. *Initial Node* $\rightarrow$ Administrator: **Membuka Menu Kriteria dan Bobot**.
  2. Sistem: **Menampilkan Data Kriteria dan Bobot**.
  3. Administrator: **Mengubah Data Kriteria dan Bobot Penilaian**.
  4. Sistem: Memvalidasi kelayakan bobot (*Decision Node: Data Bobot Valid?*):
     - **[Tidak Valid]:** Sistem **Menampilkan Pesan Kesalahan Bobot** $\rightarrow$ Kembali ke pengisian.
     - **[Valid]:** Sistem **Menyimpan Perubahan Kriteria dan Bobot** $\rightarrow$ **Menampilkan Hasil Kriteria dan Bobot**.
  5. *Activity Final Node*.

---

### AD-05: Activity Diagram Mengelola Skala Penilaian
* **Swimlane:** Administrator | Sistem SPK MOORA
* **Alur:**
  1. *Initial Node* $\rightarrow$ Administrator: **Membuka Menu Skala Penilaian**.
  2. Sistem: **Menampilkan Data Skala Penilaian**.
  3. Administrator: **Mengubah Data Skala Penilaian**.
  4. Sistem: Memvalidasi rentang skala (*Decision Node: Data Skala Valid?*):
     - **[Tidak Valid]:** Sistem **Menampilkan Pesan Kesalahan Skala** $\rightarrow$ Kembali.
     - **[Valid]:** Sistem **Menyimpan Perubahan Skala Penilaian** $\rightarrow$ **Menampilkan Hasil Skala Penilaian**.
  5. *Activity Final Node*.

---

### AD-06: Activity Diagram Mengelola Periode Penilaian
* **Swimlane:** Administrator | Sistem SPK MOORA
* **Alur:**
  1. *Initial Node* $\rightarrow$ Administrator: **Membuka Menu Periode Penilaian**.
  2. Sistem: **Menampilkan Data Periode Penilaian**.
  3. Administrator: **Membuat Periode / Mengubah Status Periode**.
  4. Sistem: Memvalidasi periode (*Decision Node: Data Periode Valid?*):
     - **[Tidak Valid]:** Sistem **Menampilkan Pesan Kesalahan Periode** $\rightarrow$ Kembali.
     - **[Valid]:** Sistem **Menyimpan Perubahan Periode Penilaian** $\rightarrow$ **Menampilkan Hasil Periode Penilaian**.
  5. *Activity Final Node*.

---

### AD-07: Activity Diagram Melakukan Penilaian Kinerja Guru
* **Swimlane:** Kepala Sekolah | Sistem SPK MOORA
* **Alur:**
  1. *Initial Node* $\rightarrow$ Kepala Sekolah: **Memilih Periode & Memilih Guru**.
  2. Sistem: **Menampilkan Kriteria Penilaian**.
  3. Kepala Sekolah: **Memberikan Nilai Kriteria Penilaian**.
  4. Sistem: Memvalidasi masukan skor (*Decision Node: Nilai Valid & Lengkap?*):
     - **[Tidak Valid]:** Sistem **Menampilkan Pesan Peringatan Nilai** $\rightarrow$ Kembali ke pengisian.
     - **[Valid]:** Sistem **Menyimpan Penilaian Kinerja Guru** $\rightarrow$ **Menampilkan Hasil & Status Penilaian**.
  5. *Activity Final Node*.

---

### AD-08: Activity Diagram Mencatat Hasil Penilaian
* **Swimlane:** Administrator | Sistem SPK MOORA
* **Alur:**
  1. *Initial Node* $\rightarrow$ Administrator: **Memilih Data / Hasil Penilaian Guru**.
  2. Sistem: **Menampilkan Form Pencatatan**.
  3. Administrator: **Mencatat Data Hasil Penilaian**.
  4. Sistem: Memeriksa data (*Decision Node: Pemeriksaan Data Valid?*):
     - **[Tidak Valid]:** Sistem **Menampilkan Pesan Kesalahan Data** $\rightarrow$ Kembali.
     - **[Valid]:** Sistem **Menyimpan Hasil Penilaian** $\rightarrow$ **Menampilkan Konfirmasi Hasil Penyimpanan**.
  5. *Activity Final Node*.

---

### AD-09: Activity Diagram Mengolah Penilaian dengan MOORA
* **Swimlane:** Administrator | Sistem SPK MOORA
* **Alur:**
  1. *Initial Node* $\rightarrow$ Administrator: **Memilih Menu Pengolahan MOORA**.
  2. Sistem: **Menampilkan Data Penilaian**.
  3. Administrator: **Menjalankan Proses Perhitungan MOORA**.
  4. Sistem: Memeriksa kesiapan data (*Decision Node: Data Penilaian Cukup?*):
     - **[Tidak Cukup]:** Sistem **Menampilkan Pesan Data Belum Lengkap** $\rightarrow$ Batal/Kembali.
     - **[Cukup]:** Sistem mengeksekusi tahapan algoritma MOORA:
       - **Membentuk Matriks Keputusan**
       - **Melakukan Normalisasi Matriks**
       - **Melakukan Pembobotan Matriks**
       - **Menghitung Nilai Optimasi / Preferensi**
       - **Menghasilkan & Menyimpan Hasil Perhitungan**
  5. Sistem: **Menampilkan Hasil Perhitungan MOORA**.
  6. *Activity Final Node*.

---

### AD-10: Activity Diagram Melihat Pemeringkatan MOORA
* **Swimlane:** Administrator / Kepala Sekolah | Sistem SPK MOORA
* **Alur:**
  1. *Initial Node* $\rightarrow$ Aktor: **Memilih Menu Pemeringkatan MOORA**.
  2. Sistem: **Menampilkan Pilihan Periode / Data**.
  3. Aktor: **Memilih Periode Penilaian**.
  4. Sistem: **Mengambil Hasil Perhitungan & Menampilkan Hasil Pemeringkatan MOORA**.
  5. *Activity Final Node*.

---

### AD-11: Activity Diagram Melihat Hasil Penilaian
* **Swimlane:** Pengguna (Admin / Kepsek / Guru) | Sistem SPK MOORA
* **Alur:**
  1. *Initial Node* $\rightarrow$ Pengguna: **Membuka Hasil Penilaian**.
  2. Sistem: **Mengambil Data Hasil Penilaian**.
  3. Pengguna: **Memilih Periode / Guru**.
  4. Sistem: **Menampilkan Hasil Penilaian**.
  5. *Activity Final Node*.

---

### AD-12: Activity Diagram Melihat Detail Penilaian
* **Swimlane:** Kepala Sekolah / Guru | Sistem SPK MOORA
* **Alur:**
  1. *Initial Node* $\rightarrow$ Aktor: **Memilih Hasil Penilaian & Mengklik Lihat Detail**.
  2. Sistem: **Mengambil Detail Penilaian**.
  3. Sistem: **Menampilkan Rincian Penilaian**.
  4. *Activity Final Node*.

---

### AD-13: Activity Diagram Monitoring Kinerja Guru
* **Swimlane:** Pengguna (Admin / Kepsek / Guru) | Sistem SPK MOORA
* **Alur:**
  1. *Initial Node* $\rightarrow$ Pengguna: **Membuka Menu Monitoring Kinerja**.
  2. Sistem: **Mengambil Data Monitoring Kinerja**.
  3. Pengguna: **Memilih Data / Periode Monitoring**.
  4. Sistem: **Menampilkan Informasi Monitoring Kinerja**.
  5. *Activity Final Node*.

---

### AD-14: Activity Diagram Melihat Riwayat Penilaian
* **Swimlane:** Pengguna (Admin / Kepsek / Guru) | Sistem SPK MOORA
* **Alur:**
  1. *Initial Node* $\rightarrow$ Pengguna: **Membuka Riwayat Penilaian**.
  2. Sistem: **Mengambil Data Riwayat Penilaian**.
  3. Pengguna: **Memilih Periode / Data Riwayat**.
  4. Sistem: **Menampilkan Riwayat Penilaian**.
  5. *Activity Final Node*.

---

### AD-15: Activity Diagram Mencetak Laporan Penilaian
* **Swimlane:** Administrator / Kepala Sekolah | Sistem SPK MOORA
* **Alur:**
  1. *Initial Node* $\rightarrow$ Aktor: **Membuka Menu Laporan**.
  2. Sistem: **Menyiapkan Data Laporan**.
  3. Aktor: **Memilih Periode / Data Laporan**.
  4. Sistem: **Menampilkan / Menyiapkan Laporan**.
  5. Aktor: **Memilih Cetak Laporan**.
  6. Sistem: **Menghasilkan Laporan**.
  7. *Activity Final Node*.