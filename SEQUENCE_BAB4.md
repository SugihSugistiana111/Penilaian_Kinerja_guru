# BAB IV – PERANCANGAN SISTEM (SEQUENCE DIAGRAM)

## 4.3 Sequence Diagram

*Sequence Diagram* menggambarkan urutan interaksi dinamis antarobjek dan aktor dalam sistem berdasarkan urutan waktu (*chronological order*). Diagram ini disusun pada **tingkat abstraksi konseptual** yang sesuai untuk standar skripsi program sarjana (S1) Teknik Informatika, yaitu berfokus pada:
1. **Siapa yang berinteraksi (*Actor*)**;
2. **Antarmuka atau formulir sistem yang digunakan (*Interface/Boundary*)**;
3. **Bagaimana sistem memproses dan merespons (*Sistem SPK MOORA*)**;
4. **Data apa yang diambil, disimpan, atau diolah (*Data/Penyimpanan*)**.

Diagram tidak mendokumentasikan sintaks kode program (*source code*), *controller*, metode teknis, maupun *query database*, melainkan menyajikan interaksi fungsional sistem informasi secara utuh.

Berikut adalah 15 Sequence Diagram (**SD-01 s.d. SD-15**) yang memetakan seluruh *Use Case* sistem secara satu-ke-satu (*1-to-1 traceability*):

---

### 1. SD-01: Sequence Diagram Login
* **Use Case Terkait**: UC-01 Melakukan Login
* **Aktor**: Pengguna (*Administrator / Kepala Sekolah / Guru*)
* **Lifeline / Objek**: `Pengguna`, `Halaman Login`, `Sistem SPK MOORA`, `Data Pengguna`
* **Urutan Interaksi**:
  1. `1: Membuka Halaman Login`: Pengguna membuka halaman login pada aplikasi.
  2. `2: Menampilkan Formulir Login`: Halaman login menyajikan formulir isian username dan password.
  3. `3: Memasukkan Username & Password`: Pengguna memasukkan data login dan menekan tombol masuk.
  4. `4: Mengirim Data Login`: Halaman login meneruskan data kredensial ke sistem.
  5. `5: Memeriksa Data Pengguna`: Sistem memeriksa kecocokan data pengguna di penyimpanan data.
  6. `6: Mengembalikan Data Pengguna`: Data pengguna dikirimkan kembali ke sistem.
  7. `7: Memvalidasi Data Login & Hak Akses`: Sistem memvalidasi keabsahan kata sandi dan hak akses (*role*) pengguna.
  8. **Fragmen Alternatif (*alt*)**:
     * **[Data Login Valid]**:
       - `8: Memberikan Akses Sesuai Role`: Sistem menyetujui akses pengguna.
       - `9: Menampilkan Dashboard Utama`: Halaman login mengarahkan tampilan ke dashboard utama sesuai hak akses.
     * **[Data Login Tidak Valid]**:
       - `10: Menolak Akses`: Sistem menolak permintaan login.
       - `11: Menampilkan Pesan Kesalahan`: Halaman login menampilkan pesan peringatan bahwa username atau password tidak valid.

---

### 2. SD-02: Sequence Diagram Mengelola Data Pengguna
* **Use Case Terkait**: UC-02 Mengelola Data Pengguna
* **Aktor**: Administrator
* **Lifeline / Objek**: `Administrator`, `Halaman Data Pengguna`, `Sistem SPK MOORA`, `Data Pengguna`
* **Urutan Interaksi**:
  1. `1: Membuka Menu Data Pengguna`: Administrator memilih menu pengelolaan data pengguna.
  2. `2: Meminta Data Terkait`: Halaman meminta daftar seluruh akun pengguna.
  3. `3: Mengambil Data dari Penyimpanan`: Sistem mengambil seluruh rekaman data pengguna.
  4. `4: Mengirimkan Data`: Data pengguna diserahkan kepada sistem.
  5. `5: Menampilkan Tabel Data`: Halaman menyajikan data pengguna dalam tabel.
  6. `6: Memasukkan / Mengubah Data Pengguna`: Administrator mengisi formulir tambah, ubah, atau hapus data akun.
  7. `7: Mengirimkan Data Masukan`: Halaman meneruskan data pengguna ke sistem.
  8. `8: Memvalidasi Kelengkapan Data`: Sistem memvalidasi kelengkapan isian formulir.
  9. `9: Menyimpan Data Pengguna`: Sistem menyimpan perubahan data akun ke penyimpanan data.
  10. `10: Mengonfirmasi Penyimpanan`: Penyimpanan mengonfirmasi keberhasilan proses simpan.
  11. `11: Menampilkan Notifikasi Berhasil`: Sistem mengirimkan status sukses ke tampilan.
  12. `12: Menampilkan Pembaruan Data`: Halaman memperbarui tampilan tabel data pengguna.

---

### 3. SD-03: Sequence Diagram Mengelola Data Guru
* **Use Case Terkait**: UC-03 Mengelola Data Guru
* **Aktor**: Administrator / Kepala Sekolah
* **Lifeline / Objek**: `Admin / Kepala Sekolah`, `Halaman Data Guru`, `Sistem SPK MOORA`, `Data Guru`
* **Urutan Interaksi**:
  1. `1: Membuka Menu Data Guru`: Aktor membuka menu data master guru.
  2. `2: Meminta Data Terkait`: Halaman meminta daftar seluruh data guru.
  3. `3: Mengambil Data dari Penyimpanan`: Sistem mengambil data guru dari penyimpanan data.
  4. `4: Mengirimkan Data`: Data guru (NIP, nama, mata pelajaran) dikirimkan ke sistem.
  5. `5: Menampilkan Tabel Data`: Halaman menyajikan daftar data guru.
  6. `6: Memasukkan / Mengubah Data Guru`: Aktor menginput data baru atau mengubah profil data guru.
  7. `7: Mengirimkan Data Masukan`: Halaman mengirim data guru ke sistem.
  8. `8: Memvalidasi Format NIP & Kelengkapan`: Sistem memvalidasi format NIP dan kelengkapan biodata guru.
  9. `9: Menyimpan Data Guru`: Sistem menyimpan data guru ke penyimpanan data.
  10. `10: Mengonfirmasi Penyimpanan`: Penyimpanan data memberikan respon berhasil.
  11. `11: Menampilkan Notifikasi Berhasil`: Sistem memberikan respon sukses.
  12. `12: Menampilkan Pembaruan Data`: Halaman memperbarui tabel daftar guru.

---

### 4. SD-04: Sequence Diagram Mengelola Kriteria dan Bobot
* **Use Case Terkait**: UC-04 Mengelola Kriteria dan Bobot
* **Aktor**: Administrator
* **Lifeline / Objek**: `Administrator`, `Halaman Kriteria & Bobot`, `Sistem SPK MOORA`, `Data Kriteria`
* **Urutan Interaksi**:
  1. `1: Membuka Menu Kriteria & Bobot`: Administrator membuka menu kriteria dan bobot penilaian.
  2. `2: Meminta Data Terkait`: Halaman meminta data kriteria yang ada.
  3. `3: Mengambil Data dari Penyimpanan`: Sistem mengambil daftar kriteria dan bobot.
  4. `4: Mengirimkan Data`: Data kriteria, bobot, dan jenis (benefit/cost) dikirimkan ke sistem.
  5. `5: Menampilkan Tabel Data`: Halaman menyajikan data kriteria.
  6. `6: Mengubah Kriteria & Nilai Bobot`: Administrator memperbarui nilai bobot atau data kriteria.
  7. `7: Mengirimkan Data Masukan`: Halaman mengirim perubahan kriteria ke sistem.
  8. `8: Memvalidasi Total Bobot (100%)`: Sistem memverifikasi bahwa total akumulasi bobot bernilai 1.0 (100%).
  9. `9: Menyimpan Perubahan Kriteria`: Sistem menyimpan perubahan kriteria ke penyimpanan data.
  10. `10: Mengonfirmasi Penyimpanan`: Penyimpanan data mengonfirmasi perubahan berhasil.
  11. `11: Menampilkan Notifikasi Berhasil`: Sistem memberikan respon sukses.
  12. `12: Menampilkan Pembaruan Data`: Halaman menampilkan tabel kriteria terbaru.

---

### 5. SD-05: Sequence Diagram Mengelola Skala Penilaian
* **Use Case Terkait**: UC-05 Mengelola Skala Penilaian
* **Aktor**: Administrator
* **Lifeline / Objek**: `Administrator`, `Halaman Skala Penilaian`, `Sistem SPK MOORA`, `Data Skala Penilaian`
* **Urutan Interaksi**:
  1. `1: Membuka Menu Skala Penilaian`: Administrator membuka menu pengaturan skala penilaian.
  2. `2: Meminta Data Terkait`: Halaman meminta opsi skala per kriteria.
  3. `3: Mengambil Data dari Penyimpanan`: Sistem mengambil rincian skala dan rentang nilai.
  4. `4: Mengirimkan Data`: Data opsi skala dan bobot nilai dikirimkan ke sistem.
  5. `5: Menampilkan Tabel Data`: Halaman menampilkan daftar skala penilaian.
  6. `6: Memperbarui Opsi Skala & Nilai`: Administrator mengubah opsi deskripsi atau skor nilai skala.
  7. `7: Mengirimkan Data Masukan`: Halaman mengirim data perubahan ke sistem.
  8. `8: Memvalidasi Rentang Nilai Skala`: Sistem memvalidasi rentang nilai pada skala penilaian.
  9. `9: Menyimpan Data Skala Penilaian`: Sistem menyimpan data skala ke penyimpanan.
  10. `10: Mengonfirmasi Penyimpanan`: Penyimpanan data mengonfirmasi penyimpanan berhasil.
  11. `11: Menampilkan Notifikasi Berhasil`: Sistem mengirim respon berhasil.
  12. `12: Menampilkan Pembaruan Data`: Halaman menampilkan pembaruan data skala penilaian.

---

### 6. SD-06: Sequence Diagram Mengelola Periode Penilaian
* **Use Case Terkait**: UC-06 Mengelola Periode Penilaian
* **Aktor**: Administrator
* **Lifeline / Objek**: `Administrator`, `Halaman Periode Penilaian`, `Sistem SPK MOORA`, `Data Periode`
* **Urutan Interaksi**:
  1. `1: Membuka Menu Periode Penilaian`: Administrator membuka menu periode penilaian.
  2. `2: Meminta Data Terkait`: Halaman meminta riwayat seluruh periode.
  3. `3: Mengambil Data dari Penyimpanan`: Sistem mengambil data periode penilaian.
  4. `4: Mengirimkan Data`: Data periode (nama, tahun ajaran, status) dikirimkan ke sistem.
  5. `5: Menampilkan Tabel Data`: Halaman menyajikan tabel daftar periode.
  6. `6: Memasukkan / Mengubah Periode`: Administrator menambahkan periode baru atau mengubah status periode aktif.
  7. `7: Mengirimkan Data Masukan`: Halaman meneruskan data periode ke sistem.
  8. `8: Memvalidasi Status Periode Aktif`: Sistem memverifikasi status keaktifan periode.
  9. `9: Menyimpan Data Periode Penilaian`: Sistem menyimpan rekaman periode ke penyimpanan.
  10. `10: Mengonfirmasi Penyimpanan`: Penyimpanan data mengonfirmasi data tersimpan.
  11. `11: Menampilkan Notifikasi Berhasil`: Sistem memberikan notifikasi sukses.
  12. `12: Menampilkan Pembaruan Data`: Halaman menampilkan daftar periode penilaian terbaru.

---

### 7. SD-07: Sequence Diagram Melakukan Penilaian Kinerja Guru
* **Use Case Terkait**: UC-07 Melakukan Penilaian Kinerja Guru
* **Aktor**: Kepala Sekolah
* **Lifeline / Objek**: `Kepala Sekolah`, `Halaman Penilaian Kinerja`, `Sistem SPK MOORA`, `Data Penilaian`
* **Urutan Interaksi**:
  1. `1: Memilih Periode Aktif & Guru yang Dinilai`: Kepala Sekolah memilih periode dan nama guru.
  2. `2: Meminta Data Terkait`: Halaman meminta formulir butir-butir kriteria penilaian.
  3. `3: Mengambil Data dari Penyimpanan`: Sistem mengambil butir kriteria dan opsi nilai.
  4. `4: Mengirimkan Data`: Data butir kriteria dikirimkan ke sistem.
  5. `5: Menampilkan Tabel Data`: Halaman menampilkan formulir instrumen penilaian kinerja.
  6. `6: Memasukkan Nilai per Kriteria`: Kepala Sekolah memberikan skor nilai pada masing-masing kriteria.
  7. `7: Mengirimkan Data Masukan`: Halaman mengirim data evaluasi guru ke sistem.
  8. `8: Memvalidasi Kelengkapan Nilai`: Sistem memeriksa bahwa seluruh kriteria telah terisi lengkap.
  9. `9: Menyimpan Data Penilaian Guru`: Sistem menyimpan data evaluasi guru ke penyimpanan.
  10. `10: Mengonfirmasi Penyimpanan`: Penyimpanan mengonfirmasi penyimpanan berhasil.
  11. `11: Menampilkan Notifikasi Berhasil`: Sistem memberikan respon sukses.
  12. `12: Menampilkan Pembaruan Data`: Halaman menampilkan status bahwa guru telah selesai dinilai.

---

### 8. SD-08: Sequence Diagram Mencatat Hasil Penilaian
* **Use Case Terkait**: UC-08 Mencatat Hasil Penilaian
* **Aktor**: Administrator
* **Lifeline / Objek**: `Administrator`, `Halaman Pencatatan Penilaian`, `Sistem SPK MOORA`, `Data Penilaian`
* **Urutan Interaksi**:
  1. `1: Membuka Menu Pencatatan Penilaian`: Administrator membuka menu pencatatan penilaian.
  2. `2: Meminta Data Terkait`: Halaman meminta data penilaian guru yang telah diinput.
  3. `3: Mengambil Data dari Penyimpanan`: Sistem mengambil berkas penilaian dari penyimpanan data.
  4. `4: Mengirimkan Data`: Data penilaian dikirimkan kepada sistem.
  5. `5: Menampilkan Tabel Data`: Halaman menyajikan data penilaian untuk diverifikasi.
  6. `6: Memverifikasi Data Penilaian`: Administrator memeriksa dan menyetujui pencatatan nilai.
  7. `7: Mengirimkan Data Masukan`: Halaman mengirim konfirmasi persetujuan ke sistem.
  8. `8: Memeriksa Integritas Rekaman Data`: Sistem memeriksa validitas rekaman data penilaian.
  9. `9: Memperbarui Status Pencatatan`: Sistem memperbarui status penilaian menjadi tercatat resmi.
  10. `10: Mengonfirmasi Penyimpanan`: Penyimpanan mengonfirmasi status telah diperbarui.
  11. `11: Menampilkan Notifikasi Berhasil`: Sistem memberikan respon berhasil.
  12. `12: Menampilkan Pembaruan Data`: Halaman memperbarui tampilan konfirmasi pencatatan resmi.

---

### 9. SD-09: Sequence Diagram Mengolah Penilaian dengan MOORA
* **Use Case Terkait**: UC-09 Mengolah Penilaian dengan MOORA
* **Aktor**: Administrator
* **Lifeline / Objek**: `Administrator`, `Halaman Pengolahan MOORA`, `Sistem SPK MOORA`, `Data & Hasil MOORA`
* **Urutan Interaksi**:
  1. `1: Membuka Menu Pengolahan MOORA`: Administrator membuka menu perhitungan SPK MOORA.
  2. `2: Meminta Dataset Penilaian Periode Terpilih`: Halaman meminta data nilai seluruh guru pada periode aktif.
  3. `3: Mengambil Data Nilai & Bobot Kriteria`: Sistem mengambil data nilai penilaian dan bobot kriteria.
  4. `4: Mengirimkan Dataset Penilaian`: Data penilaian guru diserahkan kepada sistem.
  5. `5: Menampilkan Tabel Data Nilai Awal`: Halaman menyajikan data matriks nilai awal.
  6. `6: Memilih Hitung Metode MOORA`: Administrator menekan tombol perhitungan metode MOORA.
  7. `7: Memproses Perhitungan Algoritma MOORA`: Halaman meminta sistem menjalankan komputasi MOORA.
  8. `8: (1) Membentuk Matriks Keputusan (X)`: Sistem membentuk matriks keputusan nilai kinerja guru.
  9. `9: (2) Menghitung Normalisasi Matriks (X*)`: Sistem menghitung matriks ternormalisasi.
  10. `10: (3) Menghitung Matriks Terbobot (Wj)`: Sistem mengalikan matriks normalisasi dengan bobot kriteria.
  11. `11: (4) Menghitung Nilai Preferensi (Yi)`: Sistem menghitung nilai akhir optimasi/preferensi setiap guru.
  12. `12: (5) Menyimpan Nilai Preferensi & Peringkat`: Sistem menyimpan hasil preferensi dan urutan ranking ke penyimpanan.
  13. `13: Mengonfirmasi Penyimpanan Hasil`: Penyimpanan data mengonfirmasi penyimpanan berhasil.
  14. `14: Menampilkan Hasil Komputasi & Pemeringkatan`: Sistem mengirim hasil perhitungan ke halaman.
  15. `15: Menampilkan Hasil Perhitungan Lengkap`: Halaman menyajikan tabel tahapan matriks MOORA dan peringkat guru.

---

### 10. SD-10: Sequence Diagram Melihat Pemeringkatan MOORA
* **Use Case Terkait**: UC-10 Melihat Pemeringkatan MOORA
* **Aktor**: Administrator / Kepala Sekolah
* **Lifeline / Objek**: `Admin / Kepala Sekolah`, `Halaman Pemeringkatan MOORA`, `Sistem SPK MOORA`, `Hasil MOORA`
* **Urutan Interaksi**:
  1. `1: Membuka Menu Pemeringkatan MOORA`: Aktor membuka menu peringkat kinerja guru.
  2. `2: Memilih Filter Periode / Kategori`: Aktor memilih periode penilaian tertentu.
  3. `3: Meminta Data Informasi`: Halaman meminta daftar pemeringkatan guru.
  4. `4: Mengambil Data Peringkat Terurut`: Sistem mengambil data hasil MOORA yang telah diurutkan dari skor tertinggi.
  5. `5: Mengirimkan Data Hasil`: Hasil pemeringkatan dikirimkan kepada sistem.
  6. `6: Menampilkan Tabel Urutan Peringkat`: Sistem menyajikan data peringkat ke tampilan.
  7. `7: Menampilkan Data di Layar`: Halaman menampilkan daftar peringkat guru secara lengkap.

---

### 11. SD-11: Sequence Diagram Melihat Hasil Penilaian
* **Use Case Terkait**: UC-11 Melihat Hasil Penilaian
* **Aktor**: Pengguna (*Administrator / Kepala Sekolah / Guru*)
* **Lifeline / Objek**: `Pengguna`, `Halaman Hasil Penilaian`, `Sistem SPK MOORA`, `Data Penilaian`
* **Urutan Interaksi**:
  1. `1: Membuka Menu Hasil Penilaian`: Pengguna membuka menu hasil penilaian.
  2. `2: Memilih Filter Periode / Kategori`: Pengguna memilih periode atau filter data guru.
  3. `3: Meminta Data Informasi`: Halaman meminta rekaman hasil evaluasi.
  4. `4: Mengambil Data Hasil Penilaian`: Sistem mengambil data evaluasi sesuai hak akses pengguna.
  5. `5: Mengirimkan Data Hasil`: Data hasil penilaian dikirimkan kepada sistem.
  6. `6: Menampilkan Ringkasan Hasil Penilaian`: Sistem menyajikan data hasil ke tampilan.
  7. `7: Menampilkan Data di Layar`: Halaman menampilkan ringkasan nilai evaluasi kinerja guru.

---

### 12. SD-12: Sequence Diagram Melihat Detail Penilaian
* **Use Case Terkait**: UC-12 Melihat Detail Penilaian
* **Aktor**: Kepala Sekolah / Guru
* **Lifeline / Objek**: `Kepala Sekolah / Guru`, `Halaman Detail Penilaian`, `Sistem SPK MOORA`, `Data Penilaian`
* **Urutan Interaksi**:
  1. `1: Memilih Data Guru & Klik Lihat Detail`: Aktor memilih salah satu guru dan mengklik lihat detail.
  2. `2: Meminta Rincian Nilai per Kriteria`: Halaman meminta rincian skor indikator penilaian.
  3. `3: Mengambil Skor & Indikator Kriteria`: Sistem mengambil data rincian nilai per butir kriteria.
  4. `4: Mengirimkan Rincian Penilaian`: Data rincian penilaian dikirimkan kepada sistem.
  5. `5: Menampilkan Jendela Rincian Nilai`: Sistem menyajikan rincian nilai ke jendela informasi.
  6. `6: Menampilkan Detail Evaluasi Kinerja Guru`: Halaman menampilkan rincian nilai evaluasi per kriteria secara transparan.

---

### 13. SD-13: Sequence Diagram Monitoring Kinerja Guru
* **Use Case Terkait**: UC-13 Monitoring Kinerja Guru
* **Aktor**: Pengguna (*Administrator / Kepala Sekolah / Guru*)
* **Lifeline / Objek**: `Pengguna`, `Halaman Monitoring Kinerja`, `Sistem SPK MOORA`, `Data Monitoring`
* **Urutan Interaksi**:
  1. `1: Membuka Menu Monitoring Kinerja`: Pengguna membuka menu monitoring capaian guru.
  2. `2: Memilih Filter Periode / Kategori`: Pengguna menentukan periode monitoring.
  3. `3: Meminta Data Informasi`: Halaman meminta data progres penilaian dan statistik skor.
  4. `4: Mengambil Progres & Statistik Kinerja`: Sistem mengambil data statistik capaian guru.
  5. `5: Mengirimkan Data Hasil`: Data statistik dikirimkan kepada sistem.
  6. `6: Menampilkan Dashboard Monitoring Grafik`: Sistem menyajikan data dalam bentuk grafik visual.
  7. `7: Menampilkan Data di Layar`: Halaman menampilkan dashboard grafik monitoring kinerja guru.

---

### 14. SD-14: Sequence Diagram Melihat Riwayat Penilaian
* **Use Case Terkait**: UC-14 Melihat Riwayat Penilaian
* **Aktor**: Pengguna (*Administrator / Kepala Sekolah / Guru*)
* **Lifeline / Objek**: `Pengguna`, `Halaman Riwayat Penilaian`, `Sistem SPK MOORA`, `Data Riwayat Penilaian`
* **Urutan Interaksi**:
  1. `1: Membuka Menu Riwayat Penilaian`: Pengguna membuka menu arsip riwayat penilaian.
  2. `2: Memilih Filter Periode / Kategori`: Pengguna memilih periode tahun sebelumnya.
  3. `3: Meminta Data Informasi`: Halaman meminta data arsip penilaian masa lalu.
  4. `4: Mengambil Rekaman Arsip Penilaian`: Sistem mengambil rekaman arsip dari penyimpanan.
  5. `5: Mengirimkan Data Hasil`: Data riwayat dikirimkan kepada sistem.
  6. `6: Menampilkan Tabel Riwayat Penilaian`: Sistem menyajikan data arsip ke tampilan.
  7. `7: Menampilkan Data di Layar`: Halaman menampilkan tabel riwayat evaluasi kinerja guru lampau.

---

### 15. SD-15: Sequence Diagram Mencetak Laporan Penilaian
* **Use Case Terkait**: UC-15 Mencetak Laporan Penilaian
* **Aktor**: Administrator / Kepala Sekolah
* **Lifeline / Objek**: `Admin / Kepala Sekolah`, `Halaman Laporan Penilaian`, `Sistem SPK MOORA`, `Data Laporan`
* **Urutan Interaksi**:
  1. `1: Membuka Menu Laporan Penilaian`: Aktor membuka menu laporan penilaian.
  2. `2: Memilih Periode & Format Laporan`: Aktor menentukan periode penilaian dan jenis laporan.
  3. `3: Meminta Pratinjau Lembar Laporan`: Halaman meminta lembar pratinjau dokumen laporan.
  4. `4: Mengambil Data Rekap Penilaian & Peringkat`: Sistem mengambil data rekapitulasi penilaian dan peringkat.
  5. `5: Mengirimkan Rekap Data Laporan`: Data lengkap laporan dikirimkan kepada sistem.
  6. `6: Menampilkan Pratinjau Dokumen Laporan`: Halaman menampilkan pratinjau lembar laporan.
  7. `7: Memilih Cetak Dokumen PDF`: Aktor menekan tombol cetak laporan.
  8. `8: Meminta Pembuatan Berkas PDF`: Halaman meminta sistem membuat dokumen PDF resmi.
  9. `9: Menyusun Format Tata Letak Laporan`: Sistem menyusun format laporan (kop sekolah, tabel penilaian, ranking, dan tanda tangan).
  10. `10: Menghasilkan Berkas Laporan PDF`: Sistem menghasilkan berkas PDF siap cetak.
  11. `11: Mengunduh / Mencetak Dokumen Laporan`: Halaman menyajikan berkas PDF untuk diunduh atau dicetak oleh aktor.

---

### 📋 Matriks Pemetaan Sequence Diagram Konseptual

| Kode SD | Nama Sequence Diagram | Use Case Terkait | Aktor Utama | Lifeline Interface | Lifeline Sistem | Lifeline Data |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **SD-01** | Login | UC-01 | Pengguna | Halaman Login | Sistem SPK MOORA | Data Pengguna |
| **SD-02** | Mengelola Data Pengguna | UC-02 | Administrator | Halaman Data Pengguna | Sistem SPK MOORA | Data Pengguna |
| **SD-03** | Mengelola Data Guru | UC-03 | Admin / Kepala Sekolah | Halaman Data Guru | Sistem SPK MOORA | Data Guru |
| **SD-04** | Mengelola Kriteria dan Bobot | UC-04 | Administrator | Halaman Kriteria & Bobot | Sistem SPK MOORA | Data Kriteria |
| **SD-05** | Mengelola Skala Penilaian | UC-05 | Administrator | Halaman Skala Penilaian | Sistem SPK MOORA | Data Skala Penilaian |
| **SD-06** | Mengelola Periode Penilaian | UC-06 | Administrator | Halaman Periode Penilaian| Sistem SPK MOORA | Data Periode |
| **SD-07** | Melakukan Penilaian Kinerja Guru | UC-07 | Kepala Sekolah | Halaman Penilaian Kinerja| Sistem SPK MOORA| Data Penilaian |
| **SD-08** | Mencatat Hasil Penilaian | UC-08 | Administrator | Halaman Pencatatan Penilaian | Sistem SPK MOORA | Data Penilaian |
| **SD-09** | Mengolah Penilaian dengan MOORA | UC-09 | Administrator | Halaman Pengolahan MOORA | Sistem SPK MOORA | Data & Hasil MOORA |
| **SD-10** | Melihat Pemeringkatan MOORA | UC-10 | Admin / Kepala Sekolah | Halaman Pemeringkatan MOORA | Sistem SPK MOORA | Hasil MOORA |
| **SD-11** | Melihat Hasil Penilaian | UC-11 | Pengguna | Halaman Hasil Penilaian | Sistem SPK MOORA | Data Penilaian |
| **SD-12** | Melihat Detail Penilaian | UC-12 | Kepala Sekolah / Guru | Halaman Detail Penilaian | Sistem SPK MOORA | Data Penilaian |
| **SD-13** | Monitoring Kinerja Guru | UC-13 | Pengguna | Halaman Monitoring Kinerja | Sistem SPK MOORA | Data Monitoring |
| **SD-14** | Melihat Riwayat Penilaian | UC-14 | Pengguna | Halaman Riwayat Penilaian | Sistem SPK MOORA | Data Riwayat Penilaian |
| **SD-15** | Mencetak Laporan Penilaian | UC-15 | Admin / Kepala Sekolah | Halaman Laporan Penilaian | Sistem SPK MOORA | Data Laporan |
