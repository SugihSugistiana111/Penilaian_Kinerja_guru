# RPD

## RANCANG BANGUN SISTEM PENDUKUNG KEPUTUSAN BERBASIS WEB UNTUK PENILAIAN KINERJA GURU MENGGUNAKAN METODE MOORA PADA SMA AL-IHSAN BOARDING SCHOOL

---

## 1. IDENTITAS PROYEK

**Nama Sistem:**
Sistem Pendukung Keputusan Penilaian Kinerja Guru

**Nama Singkat Sistem:**
SPK Kinerja Guru

**Objek Penelitian:**
SMA Al-Ihsan Boarding School

**Platform:**
Web Responsive

**Framework Frontend/Backend:**
Next.js + TypeScript

**Arsitektur:**
Next.js App Router + Server Components + Server Actions/API

**Database:**
PostgreSQL

**ORM:**
Prisma ORM

**Styling:**
Tailwind CSS

**Komponen UI:**
shadcn/ui

**Visualisasi:**
Recharts

**Autentikasi:**
Session-based authentication dengan password yang di-hash menggunakan bcrypt

**Metode SPK:**
MOORA — Multi-Objective Optimization on the Basis of Ratio Analysis

**Role Pengguna:**

1. Administrator
2. Kepala Sekolah
3. Guru

---

# 2. TUJUAN SISTEM

Sistem dikembangkan untuk membantu SMA Al-Ihsan Boarding School dalam mengelola penilaian kinerja guru secara berkala.

Sistem tidak menggantikan PKG tahunan yang telah berjalan, tetapi menjadi alat bantu untuk:

* mengelola data guru;
* mengelola periode penilaian;
* mengelola kriteria dan bobot;
* mencatat hasil penilaian;
* melakukan validasi kelengkapan penilaian;
* melakukan perhitungan MOORA secara otomatis;
* menghasilkan nilai preferensi;
* menghasilkan ranking guru;
* menyimpan riwayat penilaian;
* memantau perkembangan kinerja guru;
* menyediakan laporan bagi Kepala Sekolah;
* memberikan transparansi hasil kepada Guru.

Sistem harus mempertahankan prinsip bahwa keputusan akhir tetap berada pada Kepala Sekolah. Hal tersebut sesuai dengan posisi SPK dalam penelitian, yaitu sebagai alat bantu pengambilan keputusan.

---

# 3. DASAR KEBUTUHAN SISTEM

Sistem dibangun berdasarkan permasalahan bahwa penilaian kinerja guru belum memiliki mekanisme terintegrasi untuk rekapitulasi dan pengolahan data secara berkala.

Sistem yang dikembangkan harus mampu mengintegrasikan:

```text
Data Guru
    ↓
Periode Penilaian
    ↓
Data Penilaian
    ↓
Validasi Kelengkapan
    ↓
Normalisasi MOORA
    ↓
Pembobotan
    ↓
Nilai Optimasi
    ↓
Ranking
    ↓
Riwayat
    ↓
Monitoring
    ↓
Laporan
```

Sistem yang diusulkan dalam laporan memang melibatkan Administrator sebagai pengelola data, Kepala Sekolah sebagai penilai utama, dan Guru sebagai pihak yang melihat hasil penilaiannya sendiri.

---

# 4. ROLE DAN HAK AKSES

## 4.1 Administrator

Administrator merupakan pengelola sistem dan asisten administratif Kepala Sekolah.

### Hak akses:

* Login
* Dashboard Administrator
* Kelola pengguna
* Kelola data guru
* Kelola periode penilaian
* Kelola kriteria
* Kelola bobot
* Kelola skala penilaian
* Input/mencatat nilai berdasarkan hasil penilaian Kepala Sekolah
* Memeriksa kelengkapan penilaian
* Menjalankan proses perhitungan MOORA setelah data lengkap
* Melihat hasil ranking
* Melihat riwayat
* Melihat detail penilaian
* Mencetak laporan

Administrator **tidak boleh menentukan nilai kinerja secara mandiri**. Nilai berasal dari hasil penilaian Kepala Sekolah. Ketentuan ini mengikuti pembagian kewenangan dalam laporan skripsi.

---

## 4.2 Kepala Sekolah

Kepala Sekolah merupakan penilai utama.

### Hak akses:

* Login
* Dashboard Kepala Sekolah
* Melihat data guru
* Melakukan penilaian guru
* Melihat status kelengkapan penilaian
* Melihat hasil MOORA
* Melihat ranking
* Melihat detail penilaian
* Melihat riwayat penilaian
* Monitoring perkembangan kinerja guru
* Melihat grafik perkembangan
* Mencetak laporan

Kepala Sekolah menjadi pihak yang memberikan nilai berdasarkan empat kriteria penelitian.

---

## 4.3 Guru

Guru merupakan pihak yang dinilai.

### Hak akses:

* Login
* Dashboard Guru
* Melihat profil sendiri
* Melihat hasil penilaian sendiri
* Melihat nilai setiap kriteria
* Melihat nilai preferensi MOORA
* Melihat riwayat penilaian sendiri
* Melihat grafik perkembangan kinerja sendiri

Guru **tidak dapat**:

* mengubah nilai;
* melihat nilai guru lain;
* mengubah kriteria;
* mengubah bobot;
* menjalankan proses MOORA;
* mengelola pengguna.

---

# 5. DATA GURU

Data guru harus mengikuti struktur yang diberikan dan tidak hanya menyimpan nama serta jabatan.

## Struktur data guru

| No | Field                              | Keterangan                        |
| -- | ---------------------------------- | --------------------------------- |
| 1  | Nomor                              | Nomor urut                        |
| 2  | Nama Guru                          | Nama lengkap guru                 |
| 3  | L/P                                | Jenis kelamin                     |
| 4  | Jabatan/Tugas Mengajar             | Jabatan atau tugas utama mengajar |
| 5  | Tugas Tambahan Utama               | Tugas tambahan utama              |
| 6  | Tugas Tambahan Lain yang Ekuivalen | Tugas tambahan lain               |
| 7  | Jumlah Siswa per Rombel            | Jumlah siswa dalam rombel         |
| 8  | Jumlah Jam Ajar                    | Total jam mengajar                |
| 9  | Kelas 10                           | Kelas yang diajar                 |
| 10 | Kelas 11                           | Kelas yang diajar                 |
| 11 | Kelas 12                           | Kelas yang diajar                 |

### Tambahan data teknis

Untuk database, data tersebut sebaiknya tidak dibuat sebagai satu kolom teks panjang.

Contoh:

```text
guru
├── id
├── nip
├── nama
├── jenis_kelamin
├── jabatan_tugas_mengajar
├── tugas_tambahan_utama
├── tugas_tambahan_lain
├── jumlah_siswa_per_rombel
├── jumlah_jam_ajar
├── mengajar_kelas_10
├── mengajar_kelas_11
├── mengajar_kelas_12
├── status_aktif
├── created_at
└── updated_at
```

Untuk `mengajar_kelas_10`, `mengajar_kelas_11`, dan `mengajar_kelas_12`, sistem dapat menggunakan boolean:

```text
true  = mengajar
false = tidak mengajar
```

---

# 6. KRITERIA MOORA

Sesuai laporan skripsi:

| Kode | Kriteria                           | Bobot | Tipe    |
| ---- | ---------------------------------- | ----: | ------- |
| C1   | Kehadiran                          |   35% | Benefit |
| C2   | Ketepatan Waktu                    |   25% | Benefit |
| C3   | Kelengkapan Perangkat Pembelajaran |   25% | Benefit |
| C4   | Kelengkapan Administrasi Penilaian |   15% | Benefit |

Total:

```text
35% + 25% + 25% + 15% = 100%
```

Bobot tersebut berasal dari hasil identifikasi dan kesepakatan pihak sekolah sebagaimana dijelaskan dalam laporan.

---

# 7. SKALA PENILAIAN

Sistem harus menyediakan master skala penilaian.

Contoh struktur:

```text
1 = Sangat Kurang
2 = Kurang
3 = Cukup
4 = Baik
5 = Sangat Baik
```

Namun nilai skala final harus dapat dikonfigurasi Administrator berdasarkan ketentuan penelitian/sekolah.

Jangan meng-hardcode skala di dalam komponen React.

---

# 8. PERIODE PENILAIAN

Periode menggunakan format:

```text
Bulan + Tahun
```

Contoh:

```text
Januari 2026
Februari 2026
Maret 2026
April 2026
...
```

Setiap data penilaian harus mempunyai:

```text
periode_id
guru_id
```

Sehingga sistem dapat membedakan penilaian guru pada periode yang berbeda.

Laporan skripsi menetapkan penilaian berdasarkan bulan kalender dan menyimpan hasil berdasarkan bulan dan tahun.

---

# 9. ALUR SISTEM TO-BE

Alur utama sistem harus mengikuti BPMN To-Be:

```text
START
  ↓
Login
  ↓
Validasi Username & Password
  ↓
Apakah Login Valid?
  ├── Tidak → Kembali ke Login
  │
  └── Ya
       ↓
Dashboard sesuai Role
       ↓
Pengelolaan Data Master
       ↓
Pengelolaan Periode Penilaian
       ↓
Kepala Sekolah melakukan penilaian
       ↓
Administrator membantu pencatatan hasil penilaian
       ↓
Validasi Kelengkapan Data
       ↓
Apakah Data Lengkap?
  ├── Tidak → Lengkapi Data
  │
  └── Ya
       ↓
Perhitungan MOORA
       ↓
Nilai Preferensi
       ↓
Pemeringkatan Guru
       ↓
Simpan Riwayat
       ↓
Monitoring Kinerja
       ↓
Laporan
       ↓
Guru melihat hasil miliknya
       ↓
END
```

BPMN To-Be dalam laporan menyatakan bahwa setelah seluruh data penilaian lengkap, sistem menjalankan MOORA, menyimpan hasil sebagai riwayat, memperbarui monitoring, dan menyediakan laporan serta akses hasil bagi Guru.

---

# 10. DASHBOARD ADMINISTRATOR

Dashboard harus sederhana dan tidak terlalu padat.

### Ringkasan utama:

```text
┌─────────────────────────────────────────────────────┐
│ Selamat Datang, Administrator                      │
├────────────┬────────────┬────────────┬─────────────┤
│ 18 Guru    │ Periode    │ Penilaian  │ Status      │
│ Aktif      │ Aktif      │ Selesai    │ Periode     │
├────────────┴────────────┴────────────┴─────────────┤
│ Status Penilaian Periode                           │
│ ████████████████████████████ 18/18 Lengkap        │
├─────────────────────────────────────────────────────┤
│ Aktivitas Terbaru                                  │
└─────────────────────────────────────────────────────┘
```

### Menu Administrator

```text
Dashboard
Data Master
  ├── Pengguna
  ├── Data Guru
  ├── Kriteria
  ├── Bobot Kriteria
  └── Skala Penilaian

Penilaian
  ├── Periode Penilaian
  ├── Input Penilaian
  └── Validasi Penilaian

SPK MOORA
  ├── Proses Perhitungan
  ├── Hasil Ranking
  └── Detail Perhitungan

Monitoring
  └── Riwayat Penilaian

Laporan
Profil
Keluar
```

---

# 11. DASHBOARD KEPALA SEKOLAH

Dashboard harus berorientasi pada pengambilan keputusan.

### Komponen:

```text
┌─────────────────────────────────────────────────────┐
│ Dashboard Kepala Sekolah                            │
├────────────┬────────────┬────────────┬─────────────┤
│ 18 Guru    │ Periode    │ Sudah      │ Belum       │
│ Aktif      │ Juni 2026  │ Dinilai    │ Dinilai     │
├────────────┴────────────┴────────────┴─────────────┤
│ Ringkasan Ranking                                  │
│ 1. Guru A                         0.8421            │
│ 2. Guru B                         0.8114            │
│ 3. Guru C                         0.7932            │
├─────────────────────────────────────────────────────┤
│ Grafik Perkembangan Kinerja                        │
└─────────────────────────────────────────────────────┘
```

Menu:

```text
Dashboard
Data Guru
Penilaian Guru
Hasil Ranking
Detail Penilaian
Monitoring Kinerja
Riwayat
Laporan
Profil
Keluar
```

---

# 12. DASHBOARD GURU

Dashboard Guru dibuat sederhana.

```text
Dashboard
│
├── Nilai Terakhir
├── Ranking
├── Detail Penilaian
├── Riwayat
├── Grafik Perkembangan
└── Profil
```

Guru hanya dapat melihat data miliknya sendiri.

---

# 13. HALAMAN DATA GURU

Karena jumlah kolom cukup banyak, desktop menggunakan tabel horizontal dengan fitur:

* pencarian;
* filter;
* pagination;
* sorting;
* tambah guru;
* edit;
* nonaktifkan guru;
* detail guru;
* import Excel opsional.

### Kolom tabel:

```text
No
Nama Guru
L/P
Jabatan/Tugas Mengajar
Tugas Tambahan Utama
Tugas Tambahan Lain
Jumlah Siswa/Rombel
Jumlah Jam Ajar
Kelas 10
Kelas 11
Kelas 12
Status
Aksi
```

Pada mobile, tabel tidak dipaksakan mengecil.

Gunakan:

```text
Desktop → tabel responsif horizontal
Tablet  → tabel dengan kolom prioritas
Mobile  → card/list guru
```

---

# 14. HALAMAN PENILAIAN

Kepala Sekolah memilih:

```text
Periode:
[ Juni 2026 ▼ ]

Guru:
[ Pilih Guru ▼ ]
```

Kemudian sistem menampilkan:

```text
Nama Guru
Jabatan
Jumlah Jam Ajar
Kelas yang Diajar
```

Dilanjutkan form:

```text
C1 Kehadiran
[ 1 ] [ 2 ] [ 3 ] [ 4 ] [ 5 ]

C2 Ketepatan Waktu
[ 1 ] [ 2 ] [ 3 ] [ 4 ] [ 5 ]

C3 Kelengkapan Perangkat Pembelajaran
[ 1 ] [ 2 ] [ 3 ] [ 4 ] [ 5 ]

C4 Kelengkapan Administrasi Penilaian
[ 1 ] [ 2 ] [ 3 ] [ 4 ] [ 5 ]

Catatan:
[................................]

[Simpan Penilaian]
```

---

# 15. VALIDASI KELENGKAPAN

Sebelum MOORA dijalankan:

```text
Jumlah Guru Aktif = 18

Guru sudah dinilai = 18
Guru belum dinilai = 0

Status:
✓ Data Lengkap

[Proses MOORA]
```

Jika:

```text
Guru sudah dinilai = 16
Guru belum dinilai = 2
```

Maka:

```text
⚠ Data penilaian belum lengkap.

2 guru belum memiliki penilaian pada periode Juni 2026.

Proses MOORA belum dapat dijalankan.
```

Hal ini sesuai kebutuhan sistem bahwa data yang belum lengkap tidak boleh diteruskan ke perhitungan MOORA.

---

# 16. PROSES MOORA

Sistem harus melakukan proses secara otomatis.

## Tahap 1 — Decision Matrix

```text
Guru     C1     C2     C3     C4
Guru 1   x11    x12    x13    x14
Guru 2   x21    x22    x23    x24
...
Guru 18  x181   x182   x183   x184
```

## Tahap 2 — Normalisasi

Gunakan:

```text
xij
───────
√Σxij²
```

## Tahap 3 — Pembobotan

```text
C1 × 0.35
C2 × 0.25
C3 × 0.25
C4 × 0.15
```

## Tahap 4 — Nilai Optimasi

Karena seluruh kriteria merupakan benefit:

```text
Yi =
(0.35 × X1)
+
(0.25 × X2)
+
(0.25 × X3)
+
(0.15 × X4)
```

## Tahap 5 — Ranking

Urutkan:

```text
nilai preferensi terbesar
        ↓
peringkat 1
```

dan seterusnya.

---

# 17. HALAMAN HASIL RANKING

Contoh:

| Ranking | Guru   |  C1 |  C2 |  C3 |  C4 | Nilai MOORA |
| ------: | ------ | --: | --: | --: | --: | ----------: |
|       1 | Guru A | 4.8 | 4.7 | 4.9 | 4.6 |      0.8421 |
|       2 | Guru B | 4.7 | 4.6 | 4.8 | 4.5 |      0.8214 |
|       3 | Guru C | 4.6 | 4.5 | 4.7 | 4.4 |      0.8032 |

Data di atas hanya contoh UI, bukan data penelitian.

Fitur:

```text
Filter Periode
Cari Guru
Lihat Detail
Lihat Perhitungan
Cetak Laporan
```

---

# 18. DETAIL PERHITUNGAN MOORA

Halaman detail harus transparan.

Tampilkan:

### A. Data awal

```text
Guru
C1
C2
C3
C4
```

### B. Matriks normalisasi

```text
Guru | C1 | C2 | C3 | C4
```

### C. Matriks terbobot

```text
Guru | C1 × 0.35 | C2 × 0.25 | C3 × 0.25 | C4 × 0.15
```

### D. Nilai optimasi

```text
Nilai Yi
```

### E. Ranking

```text
Peringkat
```

Tujuannya agar hasil sistem dapat dibandingkan dengan perhitungan manual sebagaimana kebutuhan validasi MOORA dalam skripsi.

---

# 19. MONITORING KINERJA

Monitoring tidak hanya menggunakan ranking.

Sistem harus menyediakan grafik berdasarkan nilai kriteria.

Contoh:

```text
Guru: Ahmad

        Jan Feb Mar Apr Mei Jun
C1       4   4   5   4   5   5
C2       3   4   4   4   5   5
C3       4   4   4   5   5   5
C4       3   4   4   4   4   5
```

Tampilkan menggunakan:

* Line Chart
* Bar Chart
* tabel riwayat

Jangan hanya menampilkan perubahan nilai MOORA karena laporan skripsi menekankan perkembangan dapat dilihat melalui skor masing-masing kriteria yang tersimpan setiap periode.

---

# 20. RIWAYAT PENILAIAN

Struktur:

```text
Periode
Nama Guru
C1
C2
C3
C4
Nilai MOORA
Ranking
Status
```

Filter:

```text
Tahun
Bulan
Guru
```

---

# 21. LAPORAN

Kepala Sekolah dapat menghasilkan:

```text
Laporan Penilaian Kinerja Guru
Periode Juni 2026
```

Isi laporan:

```text
Identitas sekolah
Periode
Daftar guru
Nilai C1
Nilai C2
Nilai C3
Nilai C4
Nilai MOORA
Ranking
```

Output:

```text
Print
PDF
```

---

# 22. STRUKTUR DATABASE POSTGRESQL

Nama database:

```text
spk_kinerja_guru_alihsan
```

Tabel utama:

```text
users
roles
guru
kriteria
skala_penilaian
periode_penilaian
penilaian
detail_penilaian
hasil_moora
detail_moora
```

---

## 22.1 Relasi database

```text
roles
  │
  └──── users

guru
  │
  ├──── penilaian
  │          │
  │          └──── detail_penilaian
  │
  └──── hasil_moora
               │
               └──── detail_moora

kriteria
  │
  ├──── skala_penilaian
  │
  └──── detail_penilaian

periode_penilaian
  │
  ├──── penilaian
  │
  └──── hasil_moora
```

---

# 23. STRUKTUR TABEL

## users

```text
id
nama
username
password
role_id
guru_id
status
created_at
updated_at
```

## roles

```text
id
nama_role
```

Data:

```text
ADMIN
KEPALA_SEKOLAH
GURU
```

## guru

```text
id
nip
nama
jenis_kelamin
jabatan_tugas_mengajar
tugas_tambahan_utama
tugas_tambahan_lain
jumlah_siswa_per_rombel
jumlah_jam_ajar
mengajar_kelas_10
mengajar_kelas_11
mengajar_kelas_12
status_aktif
created_at
updated_at
```

## kriteria

```text
id
kode
nama
bobot
jenis
status
created_at
updated_at
```

Seed:

```text
C1 | Kehadiran | 0.35 | BENEFIT
C2 | Ketepatan Waktu | 0.25 | BENEFIT
C3 | Kelengkapan Perangkat Pembelajaran | 0.25 | BENEFIT
C4 | Kelengkapan Administrasi Penilaian | 0.15 | BENEFIT
```

## skala_penilaian

```text
id
kriteria_id
nilai
label
keterangan
```

## periode_penilaian

```text
id
bulan
tahun
nama_periode
status
created_at
updated_at
```

Status:

```text
DRAFT
AKTIF
SELESAI
```

## penilaian

```text
id
guru_id
periode_id
dinilai_oleh
status
catatan
created_at
updated_at
```

## detail_penilaian

```text
id
penilaian_id
kriteria_id
nilai
```

## hasil_moora

```text
id
guru_id
periode_id
nilai_preferensi
ranking
created_at
```

## detail_moora

```text
id
hasil_moora_id
kriteria_id
nilai_awal
nilai_normalisasi
bobot
nilai_terbobot
```

Struktur detail MOORA sengaja disimpan agar proses perhitungan dapat ditelusuri dan divalidasi.

---

# 24. STRUKTUR FOLDER NEXT.JS

Gunakan struktur:

```text
spk-kinerja-guru/
│
├── app/
│   ├── (auth)/
│   │   └── login/
│   │       └── page.tsx
│   │
│   ├── admin/
│   │   ├── dashboard/
│   │   │   └── page.tsx
│   │   │
│   │   ├── pengguna/
│   │   │   └── page.tsx
│   │   │
│   │   ├── guru/
│   │   │   ├── page.tsx
│   │   │   ├── tambah/
│   │   │   │   └── page.tsx
│   │   │   └── [id]/
│   │   │       └── page.tsx
│   │   │
│   │   ├── kriteria/
│   │   │   └── page.tsx
│   │   │
│   │   ├── skala-penilaian/
│   │   │   └── page.tsx
│   │   │
│   │   ├── periode/
│   │   │   └── page.tsx
│   │   │
│   │   ├── penilaian/
│   │   │   ├── page.tsx
│   │   │   └── [periodeId]/
│   │   │       └── page.tsx
│   │   │
│   │   ├── moora/
│   │   │   ├── page.tsx
│   │   │   └── [periodeId]/
│   │   │       └── page.tsx
│   │   │
│   │   ├── ranking/
│   │   │   └── page.tsx
│   │   │
│   │   ├── monitoring/
│   │   │   └── page.tsx
│   │   │
│   │   └── laporan/
│   │       └── page.tsx
│   │
│   ├── kepala-sekolah/
│   │   ├── dashboard/
│   │   ├── guru/
│   │   ├── penilaian/
│   │   ├── ranking/
│   │   ├── monitoring/
│   │   ├── riwayat/
│   │   └── laporan/
│   │
│   ├── guru/
│   │   ├── dashboard/
│   │   ├── hasil/
│   │   ├── riwayat/
│   │   ├── monitoring/
│   │   └── profil/
│   │
│   ├── api/
│   │   └── ...
│   │
│   ├── layout.tsx
│   ├── page.tsx
│   └── globals.css
│
├── components/
│   ├── ui/
│   ├── navigasi/
│   ├── dashboard/
│   ├── guru/
│   ├── penilaian/
│   ├── moora/
│   ├── monitoring/
│   ├── laporan/
│   └── formulir/
│
├── lib/
│   ├── prisma.ts
│   ├── autentikasi.ts
│   ├── otorisasi.ts
│   ├── validasi.ts
│   └── utilitas.ts
│
├── services/
│   ├── layanan-guru.ts
│   ├── layanan-penilaian.ts
│   ├── layanan-periode.ts
│   ├── layanan-moora.ts
│   ├── layanan-monitoring.ts
│   └── layanan-laporan.ts
│
├── prisma/
│   ├── schema.prisma
│   ├── seed.ts
│   └── migrations/
│
├── types/
│   ├── pengguna.ts
│   ├── guru.ts
│   ├── penilaian.ts
│   └── moora.ts
│
├── public/
│   ├── logo/
│   └── gambar/
│
├── middleware.ts
├── .env
├── package.json
├── tsconfig.json
├── next.config.ts
└── README.md
```

Nama folder dan file menggunakan istilah yang mudah dipahami dalam bahasa Indonesia.

---

# 25. ATURAN PENAMAAN KODE

Walaupun framework menggunakan Next.js dan TypeScript, komentar kode wajib menggunakan bahasa Indonesia.

Contoh:

```typescript
// Mengambil seluruh data guru aktif untuk periode penilaian
const daftarGuru = await prisma.guru.findMany({
  where: {
    statusAktif: true,
  },
});
```

Komentar harus menjelaskan **tujuan proses**, bukan komentar yang tidak diperlukan.

Contoh fungsi:

```typescript
/**
 * Menghitung nilai MOORA berdasarkan data penilaian
 * pada satu periode tertentu.
 */
export async function hitungMoora(periodeId: string) {
  // Mengambil seluruh data penilaian yang sudah lengkap
  // sebelum proses normalisasi dilakukan.

  // Melakukan normalisasi setiap nilai kriteria.

  // Mengalikan nilai normalisasi dengan bobot kriteria.

  // Menjumlahkan nilai terbobot untuk mendapatkan nilai preferensi.

  // Mengurutkan guru berdasarkan nilai preferensi terbesar.
}
```

---

# 26. PEMISAHAN LOGIKA MOORA

Logika MOORA **tidak boleh diletakkan langsung di komponen halaman**.

Gunakan:

```text
services/
└── layanan-moora.ts
```

Struktur:

```text
ambilDataPenilaian()
        ↓
validasiKelengkapan()
        ↓
buatMatriksKeputusan()
        ↓
normalisasiMatriks()
        ↓
hitungNilaiTerbobot()
        ↓
hitungNilaiOptimasi()
        ↓
buatPeringkat()
        ↓
simpanHasilMoora()
```

Hal ini penting agar perhitungan dapat diuji secara terpisah dari antarmuka.

---

# 27. KEAMANAN

Sistem wajib menerapkan:

```text
Password Hash
        ↓
Session
        ↓
Role Validation
        ↓
Route Protection
        ↓
Data Access Protection
```

Contoh:

```text
/admin/*
```

hanya:

```text
ADMIN
```

Contoh:

```text
/kepala-sekolah/*
```

hanya:

```text
KEPALA_SEKOLAH
```

Contoh:

```text
/guru/*
```

hanya:

```text
GURU
```

Selain pembatasan halaman, API/server action juga harus memvalidasi role.

Jangan hanya mengandalkan penyembunyian menu di frontend.

---

# 28. ATURAN DATA GURU

Administrator dapat:

```text
Tambah
Lihat
Edit
Nonaktifkan
Detail
```

Tidak disarankan menghapus guru secara permanen apabila guru tersebut sudah mempunyai riwayat penilaian.

Gunakan:

```text
status_aktif = false
```

sehingga histori tetap aman.

---

# 29. ATURAN PERIODE

Hanya satu periode yang boleh berstatus:

```text
AKTIF
```

untuk proses penilaian aktif.

Periode yang sudah diproses:

```text
SELESAI
```

tidak boleh diubah sembarangan.

Jika sudah memiliki hasil MOORA:

```text
Jangan hapus
Jangan ubah bobot historis
Jangan mengubah nilai lama
```

Tujuannya agar histori penelitian tetap konsisten.

---

# 30. USER EXPERIENCE

Desain harus:

* minimalis;
* bersih;
* manusiawi;
* tidak terlalu banyak warna;
* mudah dipahami pengguna non-teknis;
* responsive;
* nyaman pada PC;
* nyaman pada tablet;
* nyaman pada smartphone.

Gunakan prinsip:

```text
Desktop
Sidebar + Content

Tablet
Sidebar collapsible + Content

Mobile
Topbar + Bottom/Drawer Navigation
```

---

# 31. PALET WARNA

Gunakan kombinasi hijau muda dan kuning muda.

### Warna utama

```text
Hijau Utama:
#86A889

Hijau Muda:
#DCEBDD

Hijau Sangat Muda:
#F3F8F3

Kuning Muda:
#F7E7A8

Kuning Sangat Muda:
#FFF9DF

Putih:
#FFFFFF

Teks Utama:
#26352A

Teks Sekunder:
#68756C
```

Jangan menggunakan terlalu banyak warna.

Status:

```text
Berhasil  → hijau
Peringatan → kuning
Kesalahan → merah lembut
Informasi → hijau/abu
```

---

# 32. GAYA UI

Gunakan:

```text
Border radius: 12–16px
Card: subtle border + shadow ringan
Button: rounded-lg
Input: rounded-lg
Table: clean
Typography: Inter atau Geist
Icon: Lucide
```

Hindari:

```text
Gradient berlebihan
Shadow berat
Animasi berlebihan
Card terlalu banyak
Warna mencolok
Dashboard penuh angka
```

---

# 33. RESPONSIVE

### Breakpoint

```text
Mobile  < 640px
Tablet  640px – 1024px
Desktop > 1024px
```

### Mobile

Tabel guru diubah menjadi:

```text
┌────────────────────────────┐
│ Ahmad Fauzi                │
│ Guru Matematika            │
│                            │
│ Jam Ajar : 24 Jam          │
│ Kelas    : 10, 11          │
│ Status   : Aktif           │
│                            │
│ [Detail]                   │
└────────────────────────────┘
```

Sedangkan tabel ranking dapat tetap menggunakan horizontal scroll.

---

# 34. KOMPONEN UI UTAMA

Buat komponen reusable:

```text
Tombol
Input
Select
Dialog
Modal
Badge
Card
Table
Pagination
Dropdown
Toast
Alert
Loading
EmptyState
ConfirmDialog
DatePicker
Chart
Sidebar
Topbar
Breadcrumb
```

Untuk komponen khusus:

```text
KartuStatistik
TabelGuru
FormGuru
FormPenilaian
TabelRanking
TabelPerhitunganMoora
GrafikPerkembangan
FilterPeriode
StatusKelengkapan
```

---

# 35. DASHBOARD CARD

Jangan menggunakan terlalu banyak statistik.

Administrator:

```text
Guru Aktif
Periode Aktif
Penilaian Lengkap
Penilaian Belum Lengkap
```

Kepala Sekolah:

```text
Guru Dinilai
Guru Belum Dinilai
Ranking Teratas
Periode
```

Guru:

```text
Nilai Terakhir
Ranking
Periode
Status Penilaian
```

---

# 36. NOTIFIKASI SISTEM

Gunakan notifikasi yang jelas.

Contoh:

```text
✓ Data guru berhasil disimpan.

✓ Penilaian berhasil disimpan.

✓ Perhitungan MOORA berhasil dilakukan.

⚠ Data penilaian belum lengkap.

⚠ Belum semua guru memiliki nilai.

✓ Hasil MOORA berhasil disimpan sebagai riwayat.
```

---

# 37. VALIDASI FORM

Gunakan validasi server dan client.

Contoh:

```text
Nama guru wajib diisi.

Jenis kelamin wajib dipilih.

Jumlah jam ajar harus berupa angka.

Nilai C1 wajib diisi.

Nilai C2 wajib diisi.

Nilai C3 wajib diisi.

Nilai C4 wajib diisi.
```

Gunakan:

```text
Zod
+
React Hook Form
```

---

# 38. SEED DATABASE

Database awal harus otomatis mempunyai:

### Role

```text
ADMIN
KEPALA_SEKOLAH
GURU
```

### Kriteria

```text
C1 Kehadiran 35%
C2 Ketepatan Waktu 25%
C3 Kelengkapan Perangkat Pembelajaran 25%
C4 Kelengkapan Administrasi Penilaian 15%
```

### User demo

```text
Administrator
Kepala Sekolah
Guru
```

Password demo hanya untuk development dan wajib diganti ketika deployment.

---

# 39. DATA SIMULASI

Karena laporan menjelaskan bahwa sekolah belum memiliki rekap penilaian bulanan, aplikasi harus menyediakan data simulasi/development untuk 18 guru.

Data tersebut harus diberi penanda:

```text
DATA SIMULASI
```

Jangan menyatakan data simulasi sebagai data penilaian sekolah yang sebenarnya.

Hal ini konsisten dengan laporan bahwa data uji digunakan untuk merepresentasikan skenario penilaian karena belum tersedia rekap penilaian kinerja guru bulanan.

---

# 40. HALAMAN LOGIN

Desain:

```text
┌─────────────────────────────────────────────┐
│                                             │
│             LOGO SMA AL-IHSAN              │
│                                             │
│       Sistem Penilaian Kinerja Guru        │
│                                             │
│ Username                                    │
│ ┌─────────────────────────────────────────┐ │
│ │ Masukkan username                       │ │
│ └─────────────────────────────────────────┘ │
│                                             │
│ Password                                    │
│ ┌─────────────────────────────────────────┐ │
│ │ •••••••••••                            │ │
│ └─────────────────────────────────────────┘ │
│                                             │
│              [ Masuk ]                     │
│                                             │
└─────────────────────────────────────────────┘
```

---

# 41. ALUR AUTHENTICATION

```text
Login
 ↓
Validasi input
 ↓
Cari username
 ↓
Verifikasi password
 ↓
Ambil role
 ↓
Buat session
 ↓
Redirect berdasarkan role
```

Redirect:

```text
ADMIN
→ /admin/dashboard

KEPALA_SEKOLAH
→ /kepala-sekolah/dashboard

GURU
→ /guru/dashboard
```

---

# 42. ALUR PENILAIAN

```text
Kepala Sekolah
      ↓
Pilih periode
      ↓
Pilih guru
      ↓
Isi C1
      ↓
Isi C2
      ↓
Isi C3
      ↓
Isi C4
      ↓
Simpan
      ↓
Database
```

Administrator:

```text
Melihat status
      ↓
Membantu pencatatan
      ↓
Memeriksa kelengkapan
```

---

# 43. ALUR PROSES MOORA

```text
Data Penilaian
       ↓
Validasi
       ↓
Matriks Keputusan
       ↓
Normalisasi
       ↓
Pembobotan
       ↓
Nilai Optimasi
       ↓
Ranking
       ↓
Simpan hasil
       ↓
Monitoring
       ↓
Laporan
```

---

# 44. AUDIT TRAIL

Untuk meningkatkan keamanan dan keterlacakan, sistem dapat memiliki tabel:

```text
log_aktivitas
```

Field:

```text
id
user_id
aktivitas
modul
data_id
waktu
alamat_ip
```

Contoh:

```text
Administrator menambahkan data guru
Kepala Sekolah memberikan penilaian
Administrator menjalankan proses MOORA
Kepala Sekolah mencetak laporan
```

---

# 45. ATURAN BISNIS PENTING

### RB-01

Guru aktif menjadi alternatif MOORA.

### RB-02

Guru nonaktif tidak dimasukkan dalam penilaian periode baru.

### RB-03

Setiap guru hanya boleh memiliki satu penilaian pada satu periode.

```text
UNIQUE(guru_id, periode_id)
```

### RB-04

Semua kriteria harus memiliki nilai sebelum MOORA dijalankan.

### RB-05

Seluruh guru aktif pada periode tersebut harus memiliki penilaian sebelum perhitungan final.

### RB-06

Bobot kriteria harus berjumlah:

```text
1.00
```

atau:

```text
100%
```

### RB-07

Hasil MOORA disimpan berdasarkan periode.

### RB-08

Hasil periode yang telah selesai tidak boleh berubah tanpa proses administrasi khusus.

### RB-09

Guru hanya dapat melihat data dirinya.

### RB-10

Keputusan akhir tetap berada pada Kepala Sekolah.

---

# 46. KEBUTUHAN NONFUNGSIONAL

Sistem harus memenuhi:

| Aspek           | Implementasi                                         |
| --------------- | ---------------------------------------------------- |
| Keamanan        | Login, session, hashing password, role authorization |
| Usability       | UI sederhana dan konsisten                           |
| Performance     | Query database efisien                               |
| Compatibility   | Chrome, Edge, Firefox                                |
| Responsive      | Mobile, tablet, desktop                              |
| Reliability     | Data tersimpan berdasarkan periode                   |
| Maintainability | Struktur folder modular                              |
| Scalability     | Data dapat bertambah                                 |
| Validation      | Client + server validation                           |

Hal ini mengikuti kebutuhan nonfungsional dalam laporan yang mencakup keamanan, usability, kinerja, kompatibilitas, keandalan, dan pemeliharaan.

---

# 47. TEKNOLOGI

Gunakan:

```text
Next.js
TypeScript
React
Tailwind CSS
shadcn/ui
Prisma ORM
PostgreSQL
Zod
React Hook Form
Lucide React
Recharts
bcrypt
```

Tidak perlu menggunakan terlalu banyak library tambahan.

Prinsip:

```text
Simple
Stable
Maintainable
Academic-friendly
Easy to explain in thesis
```

---

# 48. ENVIRONMENT

Contoh `.env`:

```env
# Koneksi database PostgreSQL
DATABASE_URL="postgresql://postgres:password@localhost:5432/spk_kinerja_guru_alihsan"

# Kunci session aplikasi
AUTH_SECRET="ganti-dengan-kunci-rahasia"

# URL aplikasi
NEXT_PUBLIC_APP_URL="http://localhost:3000"
```

Jangan memasukkan password database asli ke Git.

---

# 49. PERINTAH DEVELOPMENT

```bash
# Membuat project Next.js
npx create-next-app@latest spk-kinerja-guru

# Menginstal Prisma
npm install prisma @prisma/client

# Menginstal validasi
npm install zod react-hook-form @hookform/resolvers

# Menginstal bcrypt
npm install bcrypt

# Menginstal chart
npm install recharts

# Menginstal icon
npm install lucide-react

# Inisialisasi Prisma
npx prisma init

# Membuat migration
npx prisma migrate dev --name inisialisasi_database

# Menjalankan seed
npx prisma db seed

# Menjalankan aplikasi
npm run dev
```

---

# 50. README

README harus menjelaskan:

```text
1. Deskripsi sistem
2. Tujuan
3. Teknologi
4. Persyaratan instalasi
5. Konfigurasi PostgreSQL
6. Konfigurasi .env
7. Migrasi database
8. Seed database
9. Menjalankan aplikasi
10. Akun demo
11. Struktur folder
12. Penjelasan metode MOORA
13. Role pengguna
14. Pengujian
```

---

# 51. PENGUJIAN BLACK BOX

Fitur minimal yang diuji:

```text
Login
Logout
Hak akses role
Kelola pengguna
Kelola guru
Kelola kriteria
Kelola bobot
Kelola skala
Kelola periode
Input penilaian
Validasi penilaian
Perhitungan MOORA
Ranking
Detail MOORA
Riwayat
Monitoring
Laporan
Akses Guru
```

Laporan skripsi memang menetapkan Black Box Testing untuk autentikasi, data guru, kriteria, penilaian, MOORA, ranking, dan pembatasan akses.

---

# 52. VALIDASI PERHITUNGAN

Untuk kebutuhan skripsi, sistem harus menyediakan halaman:

```text
Detail Perhitungan MOORA
```

agar dapat dibandingkan dengan:

```text
Perhitungan Manual
        VS
Perhitungan Sistem
```

Yang dibandingkan:

```text
1. Matriks keputusan
2. Nilai normalisasi
3. Nilai terbobot
4. Nilai optimasi
5. Ranking
```

Hasil harus identik atau memiliki perbedaan hanya akibat pembulatan.

---

# 53. URUTAN IMPLEMENTASI

Pengembangan dilakukan secara bertahap.

### Tahap 1 — Setup

```text
Next.js
TypeScript
Tailwind
shadcn/ui
Prisma
PostgreSQL
```

### Tahap 2 — Database

```text
roles
users
guru
kriteria
skala_penilaian
periode_penilaian
penilaian
detail_penilaian
hasil_moora
detail_moora
```

### Tahap 3 — Authentication

```text
Login
Session
Role
Middleware
Logout
```

### Tahap 4 — Master Data

```text
Pengguna
Guru
Kriteria
Bobot
Skala
Periode
```

### Tahap 5 — Penilaian

```text
Form penilaian
Validasi
Penyimpanan
Status kelengkapan
```

### Tahap 6 — MOORA

```text
Matriks
Normalisasi
Bobot
Optimasi
Ranking
Penyimpanan hasil
```

### Tahap 7 — Monitoring

```text
Riwayat
Grafik
Detail
Perbandingan periode
```

### Tahap 8 — Laporan

```text
Preview
Print
PDF
```

### Tahap 9 — Testing

```text
Black Box
Validasi MOORA
Role testing
Responsive testing
```

---

# 54. PRIORITAS FITUR

## PRIORITAS P0 — WAJIB

```text
Login
Role management
Data guru
Kriteria
Bobot
Periode
Penilaian
Validasi kelengkapan
MOORA
Ranking
Riwayat
Guru melihat hasil
```

## PRIORITAS P1 — WAJIB UNTUK PRESENTASI/SKRIPSI

```text
Dashboard
Detail MOORA
Monitoring
Grafik
Laporan
Responsive UI
Black Box testing support
```

## PRIORITAS P2 — TAMBAHAN

```text
Import Excel
Export Excel
Audit log
Notifikasi
Dark mode
```

P2 tidak boleh mengganggu penyelesaian fitur inti.

---

# 55. KRITERIA ACCEPTANCE SISTEM

Sistem dianggap berhasil apabila:

```text
[✓] Administrator dapat login
[✓] Kepala Sekolah dapat login
[✓] Guru dapat login

[✓] Administrator dapat mengelola data guru
[✓] Administrator dapat mengelola kriteria
[✓] Administrator dapat mengelola bobot
[✓] Administrator dapat mengelola periode

[✓] Kepala Sekolah dapat memberikan penilaian
[✓] Sistem dapat memvalidasi kelengkapan
[✓] Sistem menolak MOORA jika data belum lengkap

[✓] Sistem dapat melakukan normalisasi
[✓] Sistem dapat melakukan pembobotan
[✓] Sistem dapat menghitung nilai optimasi
[✓] Sistem dapat menghasilkan ranking

[✓] Hasil disimpan berdasarkan periode
[✓] Riwayat dapat ditampilkan
[✓] Monitoring dapat ditampilkan

[✓] Kepala Sekolah dapat melihat ranking
[✓] Kepala Sekolah dapat mencetak laporan
[✓] Guru hanya dapat melihat data sendiri

[✓] Sistem responsive mobile
[✓] Sistem responsive desktop
[✓] Hak akses terlindungi
```

---

# 56. PRINSIP UTAMA PEMBANGUNAN

Aplikasi harus dibangun dengan prinsip:

```text
BPMN To-Be
      ↓
Analisis Bab III
      ↓
Kebutuhan Sistem
      ↓
Use Case
      ↓
Database
      ↓
UI/UX
      ↓
Implementasi
      ↓
MOORA
      ↓
Testing
```

Jangan membuat fitur yang tidak mempunyai hubungan dengan kebutuhan penelitian tanpa alasan yang jelas.

Fokus utama sistem tetap:

> **Mengelola penilaian kinerja guru secara bulanan, mengolahnya menggunakan MOORA, menghasilkan pemeringkatan, menyimpan riwayat, dan menyediakan informasi pendukung bagi Kepala Sekolah.**

Hal tersebut konsisten dengan tujuan penelitian dan kebutuhan sistem dalam laporan skripsi.

---

# 57. OUTPUT AKHIR YANG DIHARAPKAN

Hasil akhir aplikasi:

```text
                SPK KINERJA GURU
                       │
        ┌──────────────┼──────────────┐
        │              │              │
   ADMINISTRATOR  KEPALA SEKOLAH     GURU
        │              │              │
        ↓              ↓              ↓
   Data Master      Penilaian      Hasil Sendiri
   Periode          Ranking        Riwayat
   Penilaian        Monitoring     Monitoring
        │              │
        └───────┬──────┘
                ↓
          ENGINE MOORA
                ↓
          NILAI PREFERENSI
                ↓
             RANKING
                ↓
           RIWAYAT
                ↓
             LAPORAN
```

Sistem harus terasa seperti **aplikasi administrasi sekolah yang sederhana**, bukan dashboard perusahaan yang penuh grafik. Prioritas desain adalah keterbacaan, kemudahan Kepala Sekolah saat melakukan penilaian, dan kemudahan Guru saat melihat hasil.
