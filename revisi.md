
Saya ingin **merevisi tampilan UI yang sudah ada**, bukan membuat ulang fungsi sistem.

## TUJUAN UTAMA

Buat tampilan aplikasi yang:

* terlihat seperti aplikasi administrasi sekolah yang benar-benar dirancang dan digunakan oleh sekolah;
* profesional, sederhana, natural, dan manusiawi;
* tidak terlihat seperti hasil generate AI;
* tidak terlihat seperti template dashboard SaaS;
* tidak terlihat seperti landing page startup;
* tidak terlalu futuristik;
* tidak terlalu dekoratif;
* tidak terlalu banyak card;
* tidak terlalu banyak badge/pill;
* tidak menggunakan visual yang berlebihan;
* mengutamakan informasi dan fungsi dibanding dekorasi;
* cocok digunakan dalam lingkungan sekolah;
* pantas ditampilkan dalam presentasi dan sidang skripsi.

**Jangan mengubah fungsi, alur bisnis, database, role, metode MOORA, maupun struktur halaman yang sudah berjalan. Fokus hanya pada peningkatan UI/UX dan konsistensi visual.**

---

# 1. HINDARI KESAN AI-GENERATED

Jangan menggunakan pola desain yang membuat aplikasi terlihat seperti hasil prompt AI, seperti:

* hero section besar dengan tulisan "Selamat Datang";
* terlalu banyak floating card;
* empat atau lima statistic card yang semuanya memiliki icon besar;
* card bertumpuk di dalam card;
* terlalu banyak rounded container;
* badge berbentuk pill di hampir setiap bagian;
* gradient modern yang tidak diperlukan;
* glassmorphism;
* efek blur;
* shadow yang terlalu jelas;
* dekorasi abstrak;
* ilustrasi generik;
* icon besar hanya untuk dekorasi;
* heading yang terlalu besar;
* teks promosi seperti website startup;
* layout dashboard yang terlalu kosong;
* terlalu banyak whitespace yang tidak memiliki fungsi;
* animasi berlebihan;
* hover effect yang terlalu mencolok;
* warna terlalu banyak;
* penggunaan emoji sebagai elemen UI;
* visual "premium SaaS dashboard";
* tampilan seperti template Admin Dashboard dari marketplace;
* komponen yang terlihat dibuat hanya untuk mempercantik halaman.

**Prinsip utama:**

> Jika sebuah elemen tidak membantu pengguna memahami data atau melakukan tindakan, jangan tambahkan elemen tersebut hanya untuk mempercantik tampilan.

---

# 2. KARAKTER VISUAL

Gunakan karakter:

**"Administrasi Sekolah Profesional dan Sederhana"**

Bayangkan aplikasi ini benar-benar dibuat untuk digunakan oleh:

* Kepala Sekolah;
* Administrator;
* Guru.

Bukan untuk perusahaan teknologi.

Tampilan harus terasa seperti sistem informasi sekolah yang matang, bukan demo UI.

Gunakan prinsip:

```text
Simple
Formal
Clean
Functional
Natural
Readable
Consistent
Academic
```

---

# 3. LAYOUT DASHBOARD

Jangan gunakan hero/banner besar pada dashboard.

Hapus atau sederhanakan bagian seperti:

```text
PIMPINAN SEKOLAH

Selamat Datang, Dr. H. Mulyadi, M.Pd.

Sistem pendukung keputusan siap membantu...
```

Ganti dengan header sederhana:

```text
Dashboard Kepala Sekolah
Ringkasan penilaian kinerja guru

Periode Aktif: Juni 2026
```

Header harus terasa seperti bagian dari aplikasi, bukan bagian dari landing page.

---

# 4. SIDEBAR

Pertahankan sidebar kiri karena cocok untuk aplikasi desktop.

Gunakan struktur:

```text
SPK KINERJA GURU
SMA Al-Ihsan Boarding School

Dr. H. Mulyadi, M.Pd.
Kepala Sekolah

UTAMA
Dashboard

PENILAIAN & EVALUASI
Data Guru
Penilaian Kinerja

HASIL & KEPUTUSAN
Hasil Ranking
Monitoring Kinerja
Riwayat Penilaian
Laporan

AKUN
Profil
Keluar
```

Sidebar harus:

* sederhana;
* tidak terlalu banyak dekorasi;
* tidak menggunakan gradient;
* tidak menggunakan efek glass;
* tidak menggunakan icon besar;
* active menu cukup menggunakan background hijau lembut;
* icon menggunakan Lucide;
* teks mudah dibaca.

Jangan membuat sidebar terlihat seperti dashboard startup.

---

# 5. HEADER

Header cukup berisi:

```text
Dashboard Kepala Sekolah
Ringkasan penilaian kinerja guru

                         Periode Aktif
                         Juni 2026

                         Dr. H. Mulyadi, M.Pd.
                         Kepala Sekolah
```

Jangan gunakan terlalu banyak badge.

Gunakan informasi yang benar-benar diperlukan.

---

# 6. STATISTIK

Gunakan maksimal 4 ringkasan informasi.

Jangan membuat setiap statistik seperti kartu SaaS yang besar.

Informasi:

```text
Guru Aktif
18 Guru

Sudah Dinilai
18 Guru

Belum Dinilai
0 Guru

Periode
Juni 2026
```

Card boleh digunakan, tetapi:

* ukurannya proporsional;
* icon kecil;
* padding tidak berlebihan;
* tidak menggunakan efek 3D;
* tidak menggunakan gradient;
* tidak menggunakan shadow berat;
* radius cukup 12px;
* border tipis;
* typography sederhana.

Jangan membuat angka terlihat seperti elemen hero.

---

# 7. STATUS PENILAIAN

Buat bagian status penilaian yang sederhana.

Contoh:

```text
Status Penilaian

Juni 2026

18 dari 18 guru telah dinilai

[████████████████████] 100%

Penilaian periode ini sudah lengkap.
```

Gunakan progress bar sederhana.

Jangan membuat status menjadi card dekoratif besar.

Jika belum lengkap:

```text
Status Penilaian

16 dari 18 guru telah dinilai

[████████████████░░░░] 89%

2 guru belum memiliki penilaian.
Perhitungan MOORA belum dapat dilakukan.
```

---

# 8. HASIL RANKING

Jangan menampilkan ranking menggunakan tiga card besar atau podium seperti aplikasi kompetisi.

Gunakan tabel sederhana.

Contoh:

```text
Hasil Penilaian Terbaru

Periode: Juni 2026

No | Nama Guru | Nilai MOORA | Ranking | Status
--------------------------------------------------
1  | Guru A    | 0.8421      | 1       | Sangat Baik
2  | Guru B    | 0.8214      | 2       | Sangat Baik
3  | Guru C    | 0.8032      | 3       | Baik
```

Gunakan:

* table header jelas;
* garis/border halus;
* row height proporsional;
* hover sangat ringan;
* ranking cukup berupa angka;
* status menggunakan badge sederhana hanya jika memang diperlukan.

Jangan membuat setiap ranking menjadi card.

---

# 9. MONITORING

Gunakan grafik hanya jika memang memberikan informasi.

Untuk dashboard Kepala Sekolah gunakan satu grafik utama:

```text
Perkembangan Kinerja Guru
```

Grafik dapat menggunakan line chart sederhana.

Jangan menggunakan:

* grafik 3D;
* gradient area berlebihan;
* terlalu banyak warna;
* animasi berlebihan;
* chart dekoratif.

Gunakan warna hijau utama dan warna netral.

Jika terlalu banyak data, berikan filter:

```text
Guru [ Semua Guru ▼ ]
Periode [ 2026 ▼ ]
```

---

# 10. WARNA

Pertahankan identitas visual dari RPD.

Gunakan:

```text
Hijau Utama       #86A889
Hijau Muda        #DCEBDD
Hijau Sangat Muda #F3F8F3
Kuning Muda       #F7E7A8
Kuning Sangat Muda#FFF9DF
Putih             #FFFFFF
Teks Utama        #26352A
Teks Sekunder     #68756C
```

Gunakan warna secara hemat.

Aturan:

```text
Hijau  → aksi utama / status berhasil / menu aktif
Kuning → periode / perhatian
Merah lembut → kesalahan
Abu     → informasi sekunder
Putih   → background dan area utama
```

Jangan menambahkan warna baru tanpa kebutuhan.

Jangan gunakan gradient.

---

# 11. TYPOGRAPHY

Gunakan Inter atau Geist.

Namun jangan membuat heading terlalu besar.

Contoh:

```text
Dashboard Kepala Sekolah
24px / semibold

Ringkasan penilaian kinerja guru
14–15px / regular

Judul section
18px / semibold

Isi tabel
14px

Informasi sekunder
13px
```

Hindari typography yang terlihat seperti landing page.

Jangan membuat:

```text
SELAMAT DATANG
```

dengan font 30–40px.

---

# 12. CARD

Card tetap boleh digunakan, tetapi harus terasa seperti komponen administrasi.

Gunakan:

```text
background: white
border: 1px solid
border-radius: 12px
shadow: sangat ringan atau tanpa shadow
```

Jangan:

```text
gradient
glass effect
blur
shadow besar
border terlalu tebal
icon raksasa
```

Jangan membuat card di dalam card kecuali memang dibutuhkan.

---

# 13. BUTTON

Button harus terlihat seperti tombol aplikasi administrasi.

Primary:

```text
[ Simpan Penilaian ]
```

Secondary:

```text
[ Batal ]
[ Kembali ]
```

Action:

```text
[ Lihat Detail ]
[ Cetak Laporan ]
```

Gunakan icon kecil bila membantu.

Jangan membuat tombol terlalu besar.

Jangan menggunakan gradient.

---

# 14. FORM PENILAIAN

Halaman penilaian harus menjadi salah satu halaman paling sederhana.

Struktur:

```text
Penilaian Kinerja Guru

Periode
[ Juni 2026 ▼ ]

Guru
[ Pilih Guru ▼ ]

--------------------------------

Data Guru

Nama Guru
Jabatan
Jumlah Jam Ajar
Kelas yang Diajar

--------------------------------

Penilaian

C1 Kehadiran
○ 1   ○ 2   ○ 3   ○ 4   ○ 5

C2 Ketepatan Waktu
○ 1   ○ 2   ○ 3   ○ 4   ○ 5

C3 Kelengkapan Perangkat Pembelajaran
○ 1   ○ 2   ○ 3   ○ 4   ○ 5

C4 Kelengkapan Administrasi Penilaian
○ 1   ○ 2   ○ 3   ○ 4   ○ 5

Catatan
[...................................]

              [Simpan Penilaian]
```

Jangan membuat form menjadi kumpulan card kecil yang terlalu banyak.

Fokuskan perhatian pengguna pada proses penilaian.

---

# 15. HALAMAN DATA GURU

Karena data guru cukup banyak, desktop gunakan tabel.

Gunakan:

```text
Data Guru

[ Cari Guru... ] [ Status ▼ ] [ Tambah Guru ]

----------------------------------------------------------
No | Nama | L/P | Jabatan | Jam Ajar | Kelas | Status | Aksi
----------------------------------------------------------
```

Gunakan horizontal scroll jika diperlukan.

Jangan memaksakan semua kolom agar masuk layar dengan font terlalu kecil.

Untuk mobile gunakan card/list sederhana.

---

# 16. DETAIL MOORA

Halaman detail MOORA harus terlihat akademis dan transparan, bukan seperti dashboard visual.

Gunakan urutan:

```text
Detail Perhitungan MOORA

A. Data Awal

B. Matriks Keputusan

C. Matriks Normalisasi

D. Matriks Terbobot

E. Nilai Optimasi

F. Ranking
```

Gunakan tabel.

Utamakan keterbacaan angka.

Jangan menambahkan grafik jika tidak diperlukan.

Halaman ini harus mudah dibandingkan dengan perhitungan manual dalam skripsi.

---

# 17. HALAMAN RANKING

Ranking harus terlihat seperti hasil sistem pendukung keputusan.

Gunakan:

```text
Hasil Ranking Guru

Periode: Juni 2026

[ Cari Guru ] [ Filter Periode ]

------------------------------------------------------
Ranking | Nama Guru | C1 | C2 | C3 | C4 | Nilai
------------------------------------------------------
1       | Guru A    |... |... |... |... | 0.8421
2       | Guru B    |... |... |... |... | 0.8214
3       | Guru C    |... |... |... |... | 0.8032
```

Jangan menggunakan podium emas/perak/perunggu.

Jangan membuat ranking seperti aplikasi kompetisi.

---

# 18. LAPORAN

Halaman laporan harus terasa seperti sistem administrasi sekolah.

Gunakan:

```text
Laporan Penilaian Kinerja Guru

Periode
[ Juni 2026 ▼ ]

[ Tampilkan ]

------------------------------------------------

Ringkasan Laporan

Daftar Guru
Nilai C1
Nilai C2
Nilai C3
Nilai C4
Nilai MOORA
Ranking

                         [ Cetak ]
                         [ PDF ]
```

---

# 19. RESPONSIVE

Desktop:

```text
Sidebar + Content
```

Tablet:

```text
Collapsible Sidebar + Content
```

Mobile:

```text
Topbar
Content
Bottom Navigation / Drawer
```

Jangan sekadar mengecilkan layout desktop.

Untuk tabel:

```text
Desktop → tabel
Tablet  → tabel dengan kolom prioritas
Mobile  → card/list
```

---

# 20. ANIMASI

Gunakan animasi seminimal mungkin.

Boleh:

* hover ringan;
* transition 150–200ms;
* loading state;
* dialog transition.

Jangan menggunakan:

* floating animation;
* bouncing;
* parallax;
* gradient animation;
* card animation;
* efek masuk halaman yang berlebihan.

Aplikasi sekolah tidak membutuhkan motion design yang kompleks.

---

# 21. ICON

Gunakan Lucide Icons.

Icon harus berfungsi sebagai pendukung informasi, bukan dekorasi utama.

Ukuran umum:

```text
16px
18px
20px
```

Hindari icon 32–48px pada setiap card.

---

# 22. EMPTY STATE

Gunakan empty state yang sederhana.

Contoh:

```text
Belum ada data penilaian.

Belum terdapat penilaian pada periode ini.

[ Tambah Penilaian ]
```

Jangan menggunakan ilustrasi AI atau ilustrasi besar.

---

# 23. KONSISTENSI ANTAR HALAMAN

Semua halaman harus terasa berasal dari satu sistem.

Gunakan pola yang konsisten:

```text
Page Header
↓
Filter / Action
↓
Content
↓
Pagination / Footer
```

Jangan membuat setiap halaman memiliki layout berbeda hanya supaya terlihat menarik.

---

# 24. PRINSIP PALING PENTING

Saya lebih memilih UI yang terlihat:

> "sederhana tetapi benar-benar dibuat untuk sekolah"

daripada:

> "sangat cantik tetapi terlihat seperti hasil AI."

Jangan mengejar desain yang terlalu modern.

Jangan menambahkan komponen hanya karena terlihat bagus.

Jangan membuat halaman terlihat penuh dengan card.

Jangan membuat dashboard seperti produk SaaS.

Jangan membuat dashboard seperti template admin premium.

Buat seperti sistem informasi sekolah yang benar-benar akan dipakai Kepala Sekolah dan Administrator setiap bulan.

---

# 25. PERTAHANKAN RPD

Pastikan revisi visual tetap mengikuti kebutuhan RPD:

* tiga role: Administrator, Kepala Sekolah, Guru;
* penilaian kinerja dilakukan berkala berdasarkan periode bulan dan tahun;
* Kepala Sekolah merupakan penilai utama;
* Administrator membantu pengelolaan dan pencatatan;
* Guru hanya melihat hasil miliknya;
* terdapat validasi kelengkapan penilaian;
* MOORA dijalankan setelah data lengkap;
* hasil disimpan berdasarkan periode;
* terdapat ranking;
* terdapat monitoring;
* terdapat riwayat;
* terdapat laporan;
* keputusan akhir tetap berada pada Kepala Sekolah.

---

# 26. ATURAN IMPLEMENTASI

Sebelum mengubah kode:

1. Periksa komponen UI yang sudah ada.
2. Pertahankan fungsi dan logic yang sudah berjalan.
3. Jangan mengubah struktur database.
4. Jangan mengubah endpoint/API.
5. Jangan mengubah proses MOORA.
6. Jangan mengubah hak akses.
7. Jangan menghapus fitur yang sudah sesuai RPD.
8. Fokus pada layout, spacing, typography, warna, hierarchy, dan UX.
9. Gunakan komponen reusable.
10. Hindari duplikasi komponen.

Jika ada komponen yang terlalu dekoratif, sederhanakan.

Jika ada card yang tidak diperlukan, ubah menjadi section atau table.

Jika ada hero section yang terlalu besar, ubah menjadi page header sederhana.

Jika ada terlalu banyak badge, sisakan hanya badge yang benar-benar informatif.

---

# HASIL YANG SAYA INGINKAN

Setelah revisi, ketika seseorang melihat aplikasi ini, kesan pertamanya harus:

> "Ini sistem penilaian kinerja guru milik sekolah."

Bukan:

> "Ini dashboard SaaS yang dibuat AI."

Dan bukan:

> "Ini template admin dashboard."

Prioritas:

**Fungsionalitas → keterbacaan → konsistensi → kesederhanaan → estetika.**

Jangan mengorbankan keterbacaan dan kesederhanaan hanya untuk membuat UI terlihat modern.

---

# STATUS IMPLEMENTASI REVISI

> Dokumen ini mencatat status penerapan setiap arahan revisi di atas.

## ✅ SELESAI DIIMPLEMENTASIKAN (SEMUA HALAMAN)

### Komponen Inti
- **Sidebar** (`components/navigasi/Sidebar.tsx`) — Struktur navigasi formal dengan grup menu sesuai Section 4, logo SVG otentik SMA Al-Ihsan, tanpa gradient, warna hijau aktif
- **Topbar** (`components/navigasi/Topbar.tsx`) — Header clean berisi nama halaman, subtitle, info periode aktif dan user sesuai Section 5
- **KartuStatistik** (`components/dashboard/KartuStatistik.tsx`) — Card sederhana 12px radius, icon 16px, tanpa gradient/shadow berat, sesuai Section 6 & 12
- **AppLayout** (`components/dashboard/AppLayout.tsx`) — Layout responsif sidebar+content sesuai Section 19
- **Logo** (`components/ui/Logo.tsx`) — SVG kop surat otentik dengan lambang bunga teratai 5 kelopak

### Halaman Login
- **Login** (`app/login/page.tsx`) — Form login bersih dengan logo resmi, tanpa hero section

### Dashboard
- **Admin Dashboard** (`app/admin/dashboard/page.tsx`) — 4 statistik card sederhana, progress bar status penilaian, tabel ranking (bukan podium), log aktivitas
- **Kepsek Dashboard** (`app/kepala-sekolah/dashboard/page.tsx`) — Layout sama dengan admin tanpa hero banner
- **Guru Dashboard** (`app/guru/dashboard/page.tsx`) — Ringkasan skor personal 4 kriteria dan tabel kriteria

### Penilaian
- **Admin Penilaian** (`app/admin/penilaian/page.tsx`) — Form dua kolom (daftar guru kiri, form penilaian skala 1-5 kanan) sesuai Section 14
- **Kepsek Penilaian** (`app/kepala-sekolah/penilaian/page.tsx`) — Struktur identik

### Ranking
- **Admin Ranking** (`app/admin/ranking/page.tsx`) — Tabel akademis tanpa podium/kompetisi, sesuai Section 8 & 17
- **Kepsek Ranking** (`app/kepala-sekolah/ranking/page.tsx`) — Tabel identik

### Detail MOORA
- **Detail MOORA** (`app/admin/moora/[periodeId]/page.tsx`) — 6 tab akademis: A. Kriteria, B. Matriks Keputusan, C. Normalisasi, D. Terbobot, E. Nilai Optimasi, F. Ranking, sesuai Section 16

### Data Guru
- **Admin Data Guru** (`app/admin/guru/page.tsx`) — Tabel horizontal scroll 10 kolom, modal tambah/edit sederhana, sesuai Section 15
- **Kepsek Data Guru** (`app/kepala-sekolah/guru/page.tsx`) — Tabel read-only dengan detail modal

### Monitoring
- **Admin Monitoring** (`app/admin/monitoring/page.tsx`) — Line chart Recharts tren 4 kriteria + nilai MOORA, warna sekolah, sesuai Section 9
- **Kepsek Monitoring** (`app/kepala-sekolah/monitoring/page.tsx`) — Identik

### Riwayat
- **Kepsek Riwayat** (`app/kepala-sekolah/riwayat/page.tsx`) — Tabel histori multi-periode dengan search dan filter tahun
- **Guru Riwayat** (`app/guru/riwayat/page.tsx`) — Tabel ringkasan mandiri per periode

### Master Data Admin
- **Kriteria** (`app/admin/kriteria/page.tsx`) — Tabel bobot dengan indikator total 100%, tanpa dekorasi
- **Skala Penilaian** (`app/admin/skala-penilaian/page.tsx`) — Tabel 5 skala Likert dengan inline edit modal
- **Periode** (`app/admin/periode/page.tsx`) — Tabel siklus periode, aksi ubah status, modal tambah periode
- **MOORA Proses** (`app/admin/moora/page.tsx`) — Card validasi kelengkapan, progress bar, tombol hitung, tabel hasil tersimpan
- **Pengguna** (`app/admin/pengguna/page.tsx`) — Tabel manajemen akun dengan filter role, edit/reset password modal

### Halaman Guru Mandiri
- **Hasil** (`app/guru/hasil/page.tsx`) — Tabel 4 kriteria dengan selector periode, nilai MOORA & ranking
- **Monitoring** (`app/guru/monitoring/page.tsx`) — Line chart tren kinerja mandiri
- **Guru Profil** (`app/guru/profil/page.tsx`) — Halaman profil kepegawaian sederhana
- **Laporan Admin** (`app/admin/laporan/page.tsx`) — Toolbar sederhana + lembar kop surat resmi + tabel cetak sesuai Section 18
- **Laporan Kepsek** (`app/kepala-sekolah/laporan/page.tsx`) — Identik dengan laporan admin

## ✅ SEMUA HALAMAN TELAH DIREVISI

> **Catatan**: Seluruh perubahan bersifat UI-only. Tidak ada perubahan pada fungsi, API, database, atau logika MOORA.
