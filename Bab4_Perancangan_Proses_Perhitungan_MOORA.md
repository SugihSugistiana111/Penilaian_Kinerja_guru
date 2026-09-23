# BAB IV: HASIL DAN PEMBAHASAN
## 4.5 Perancangan dan Penerapan Proses Perhitungan Metode MOORA

### 4.5.1 Konsep Dasar dan Tahapan Metode MOORA

Metode MOORA (*Multi-Objective Optimization on the basis of Ratio Analysis*) digunakan untuk menentukan perangkingan kinerja guru berdasarkan rasio optimal multiobjektif.

### 4.5.2 Kriteria Penilaian dan Bobot Preferensi

$$\sum_{j=1}^{n} w_j = 1.00 \quad (100\%$$

**Tabel 4.12. Daftar Kriteria, Bobot Preferensi, dan Sifat Atribut MOORA**

| No | Kode | Nama Kriteria Penilaian | Bobot (W) | Sifat / Atribut |
| :---: | :---: | :--- | :---: | :---: |
| 1 | `C1` | Kehadiran | 0.35 (35%) | BENEFIT |
| 2 | `C2` | Ketepatan Waktu | 0.25 (25%) | BENEFIT |
| 3 | `C3` | Kelengkapan Perangkat Pembelajaran | 0.25 (25%) | BENEFIT |
| 4 | `C4` | Kelengkapan Administrasi Penilaian | 0.15 (15%) | BENEFIT |

---

### 4.5.3 Data Alternatif Guru yang Dievaluasi

**Tabel 4.13. Daftar Alternatif Guru SMA Al-Ihsan Boarding School (Juni 2026)**

| No | Kode Alt | NIP | Nama Lengkap Guru | Tugas Mengajar |
| :---: | :---: | :---: | :--- | :--- |
| 1 | **A1** | `198406142009031007` | Muhammad Rizky, S.Pd.I. | Guru Pendidikan Agama Islam |
| 2 | **A2** | `198501152010011001` | Ahmad Fauzi, S.Pd. | Guru Matematika |
| 3 | **A3** | `198509172010021017` | Bambang Hermanto, S.Pd. | Guru Prakarya & Kewirausahaan |
| 4 | **A4** | `198612192010011011` | Dedi Supriyadi, S.Pd. | Guru Geografi |
| 5 | **A5** | `198703222011012002` | Siti Nurhaliza, M.Pd. | Guru Bahasa Indonesia |
| 6 | **A6** | `198708232011021013` | Fajar Nugroho, S.Pd. | Guru Sejarah Indonesia |
| 7 | **A7** | `198811112012011009` | Agus Setiawan, S.Pd. | Guru PJOK |
| 8 | **A8** | `198904102014021003` | Budi Santoso, S.Si. | Guru Fisika |
| 9 | **A9** | `198906202014012016` | Fitriani, S.Pd. | Guru Bimbingan Konseling (BK) |
| 10 | **A10** | `199005122015032004` | Ratna Dewi, S.Pd. | Guru Kimia |
| 11 | **A11** | `199009092015022010` | Eka Putri Rahayu, S.E. | Guru Ekonomi |
| 12 | **A12** | `199103052016021015` | Yusuf Habibi, S.Pd. | Guru Pendidikan Pancasila |
| 13 | **A13** | `199108182016011005` | Hendra Gunawan, S.Kom. | Guru Informatika |
| 14 | **A14** | `199202022017042006` | Dewi Sartika, M.Pd. | Guru Biologi |
| 15 | **A15** | `199204152017032012` | Rina Marlina, S.Sos. | Guru Sosiologi |
| 16 | **A16** | `199307252018022008` | Nurul Hidayah, S.Pd. | Guru Bahasa Inggris |
| 17 | **A17** | `199310082018032018` | Dian Kusuma, S.Pd. | Guru Bahasa Arab |
| 18 | **A18** | `199401302019012014` | Maya Anggraini, S.Sn. | Guru Seni Budaya |

---

### 4.5.4 Langkah 1: Pembentukan Matriks Keputusan (X)

$$X = \begin{bmatrix} x_{11} & x_{12} & \dots & x_{1n} \\ x_{21} & x_{22} & \dots & x_{2n} \\ \vdots & \vdots & \ddots & \vdots \\ x_{m1} & x_{m2} & \dots & x_{mn} \end{bmatrix}$$

**Tabel 4.14. Matriks Keputusan (X) Evaluasi Kinerja Guru**

| No | Alternatif | Nama Guru | C1 | C2 | C3 | C4 |
| :---: | :---: | :--- | :---: | :---: | :---: | :---: |
| 1 | **A1** | Muhammad Rizky, S.Pd.I. | 5.0 | 5.0 | 5.0 | 5.0 |
| 2 | **A2** | Ahmad Fauzi, S.Pd. | 5.0 | 5.0 | 5.0 | 5.0 |
| 3 | **A3** | Bambang Hermanto, S.Pd. | 4.0 | 5.0 | 4.0 | 4.0 |
| 4 | **A4** | Dedi Supriyadi, S.Pd. | 4.0 | 4.0 | 4.0 | 4.0 |
| 5 | **A5** | Siti Nurhaliza, M.Pd. | 5.0 | 5.0 | 5.0 | 5.0 |
| 6 | **A6** | Fajar Nugroho, S.Pd. | 5.0 | 4.0 | 5.0 | 4.0 |
| 7 | **A7** | Agus Setiawan, S.Pd. | 4.0 | 5.0 | 4.0 | 4.0 |
| 8 | **A8** | Budi Santoso, S.Si. | 5.0 | 4.0 | 5.0 | 4.0 |
| 9 | **A9** | Fitriani, S.Pd. | 5.0 | 5.0 | 4.0 | 5.0 |
| 10 | **A10** | Ratna Dewi, S.Pd. | 4.0 | 5.0 | 4.0 | 5.0 |
| 11 | **A11** | Eka Putri Rahayu, S.E. | 4.0 | 4.0 | 4.0 | 4.0 |
| 12 | **A12** | Yusuf Habibi, S.Pd. | 5.0 | 4.0 | 4.0 | 5.0 |
| 13 | **A13** | Hendra Gunawan, S.Kom. | 5.0 | 5.0 | 5.0 | 4.0 |
| 14 | **A14** | Dewi Sartika, M.Pd. | 4.0 | 5.0 | 4.0 | 4.0 |
| 15 | **A15** | Rina Marlina, S.Sos. | 4.0 | 4.0 | 4.0 | 3.0 |
| 16 | **A16** | Nurul Hidayah, S.Pd. | 5.0 | 4.0 | 4.0 | 4.0 |
| 17 | **A17** | Dian Kusuma, S.Pd. | 5.0 | 5.0 | 4.0 | 5.0 |
| 18 | **A18** | Maya Anggraini, S.Sn. | 4.0 | 4.0 | 5.0 | 4.0 |

---

### 4.5.5 Langkah 2: Proses Normalisasi Matriks (X*)

$$x^*_{ij} = \frac{x_{ij}}{\sqrt{\sum_{i=1}^{m} x_{ij}^2}}$$

- $|X_{C1}| = \sqrt{378.00} = 19.4422$
- $|X_{C2}| = \sqrt{378.00} = 19.4422$
- $|X_{C3}| = \sqrt{351.00} = 18.7350$
- $|X_{C4}| = \sqrt{344.00} = 18.5472$

**Tabel 4.15. Matriks Ternormalisasi (X*) Metode MOORA**

| No | Alternatif | Nama Guru | C1 (0.35) | C2 (0.25) | C3 (0.25) | C4 (0.15) |
| :---: | :---: | :--- | :---: | :---: | :---: | :---: |
| 1 | **A1** | Muhammad Rizky, S.Pd.I. | 0.2572 | 0.2572 | 0.2669 | 0.2696 |
| 2 | **A2** | Ahmad Fauzi, S.Pd. | 0.2572 | 0.2572 | 0.2669 | 0.2696 |
| 3 | **A3** | Bambang Hermanto, S.Pd. | 0.2057 | 0.2572 | 0.2135 | 0.2157 |
| 4 | **A4** | Dedi Supriyadi, S.Pd. | 0.2057 | 0.2057 | 0.2135 | 0.2157 |
| 5 | **A5** | Siti Nurhaliza, M.Pd. | 0.2572 | 0.2572 | 0.2669 | 0.2696 |
| 6 | **A6** | Fajar Nugroho, S.Pd. | 0.2572 | 0.2057 | 0.2669 | 0.2157 |
| 7 | **A7** | Agus Setiawan, S.Pd. | 0.2057 | 0.2572 | 0.2135 | 0.2157 |
| 8 | **A8** | Budi Santoso, S.Si. | 0.2572 | 0.2057 | 0.2669 | 0.2157 |
| 9 | **A9** | Fitriani, S.Pd. | 0.2572 | 0.2572 | 0.2135 | 0.2696 |
| 10 | **A10** | Ratna Dewi, S.Pd. | 0.2057 | 0.2572 | 0.2135 | 0.2696 |
| 11 | **A11** | Eka Putri Rahayu, S.E. | 0.2057 | 0.2057 | 0.2135 | 0.2157 |
| 12 | **A12** | Yusuf Habibi, S.Pd. | 0.2572 | 0.2057 | 0.2135 | 0.2696 |
| 13 | **A13** | Hendra Gunawan, S.Kom. | 0.2572 | 0.2572 | 0.2669 | 0.2157 |
| 14 | **A14** | Dewi Sartika, M.Pd. | 0.2057 | 0.2572 | 0.2135 | 0.2157 |
| 15 | **A15** | Rina Marlina, S.Sos. | 0.2057 | 0.2057 | 0.2135 | 0.1617 |
| 16 | **A16** | Nurul Hidayah, S.Pd. | 0.2572 | 0.2057 | 0.2135 | 0.2157 |
| 17 | **A17** | Dian Kusuma, S.Pd. | 0.2572 | 0.2572 | 0.2135 | 0.2696 |
| 18 | **A18** | Maya Anggraini, S.Sn. | 0.2057 | 0.2057 | 0.2669 | 0.2157 |

---

### 4.5.6 Langkah 3: Pembobotan Matriks Normalisasi (W x X*)

$$v_{ij} = w_j \times x^*_{ij}$$

**Tabel 4.16. Matriks Normalisasi Terbobot (W x X*)**

| No | Alternatif | Nama Guru | C1 (0.35) | C2 (0.25) | C3 (0.25) | C4 (0.15) |
| :---: | :---: | :--- | :---: | :---: | :---: | :---: |
| 1 | **A1** | Muhammad Rizky, S.Pd.I. | 0.0900 | 0.0643 | 0.0667 | 0.0404 |
| 2 | **A2** | Ahmad Fauzi, S.Pd. | 0.0900 | 0.0643 | 0.0667 | 0.0404 |
| 3 | **A3** | Bambang Hermanto, S.Pd. | 0.0720 | 0.0643 | 0.0534 | 0.0323 |
| 4 | **A4** | Dedi Supriyadi, S.Pd. | 0.0720 | 0.0514 | 0.0534 | 0.0323 |
| 5 | **A5** | Siti Nurhaliza, M.Pd. | 0.0900 | 0.0643 | 0.0667 | 0.0404 |
| 6 | **A6** | Fajar Nugroho, S.Pd. | 0.0900 | 0.0514 | 0.0667 | 0.0323 |
| 7 | **A7** | Agus Setiawan, S.Pd. | 0.0720 | 0.0643 | 0.0534 | 0.0323 |
| 8 | **A8** | Budi Santoso, S.Si. | 0.0900 | 0.0514 | 0.0667 | 0.0323 |
| 9 | **A9** | Fitriani, S.Pd. | 0.0900 | 0.0643 | 0.0534 | 0.0404 |
| 10 | **A10** | Ratna Dewi, S.Pd. | 0.0720 | 0.0643 | 0.0534 | 0.0404 |
| 11 | **A11** | Eka Putri Rahayu, S.E. | 0.0720 | 0.0514 | 0.0534 | 0.0323 |
| 12 | **A12** | Yusuf Habibi, S.Pd. | 0.0900 | 0.0514 | 0.0534 | 0.0404 |
| 13 | **A13** | Hendra Gunawan, S.Kom. | 0.0900 | 0.0643 | 0.0667 | 0.0323 |
| 14 | **A14** | Dewi Sartika, M.Pd. | 0.0720 | 0.0643 | 0.0534 | 0.0323 |
| 15 | **A15** | Rina Marlina, S.Sos. | 0.0720 | 0.0514 | 0.0534 | 0.0243 |
| 16 | **A16** | Nurul Hidayah, S.Pd. | 0.0900 | 0.0514 | 0.0534 | 0.0323 |
| 17 | **A17** | Dian Kusuma, S.Pd. | 0.0900 | 0.0643 | 0.0534 | 0.0404 |
| 18 | **A18** | Maya Anggraini, S.Sn. | 0.0720 | 0.0514 | 0.0667 | 0.0323 |

---

### 4.5.7 Langkah 4 & 5: Hasil Akhir Nilai Preferensi (Yi) dan Perankingan

$$Y_i = \sum_{j=1}^{g} v_{ij} - \sum_{j=g+1}^{n} v_{ij}$$

**Tabel 4.17. Hasil Akhir Nilai Preferensi (Yi) dan Peringkat Kinerja Guru (MOORA)**

| Ranking | Alternatif | NIP | Nama Lengkap Guru | Tugas Mengajar | Nilai Preferensi (Yi) | Predikat |
| :---: | :---: | :---: | :--- | :--- | :---: | :---: |
| **Peringkat 1** | **A1** | `198406142009031007` | Muhammad Rizky, S.Pd.I. | Guru Pendidikan Agama Islam | **0.2615** | Sangat Baik |
| **Peringkat 2** | **A2** | `198501152010011001` | Ahmad Fauzi, S.Pd. | Guru Matematika | **0.2615** | Sangat Baik |
| **Peringkat 3** | **A5** | `198703222011012002` | Siti Nurhaliza, M.Pd. | Guru Bahasa Indonesia | **0.2615** | Sangat Baik |
| **Peringkat 4** | **A13** | `199108182016011005` | Hendra Gunawan, S.Kom. | Guru Informatika | **0.2534** | Baik |
| **Peringkat 5** | **A9** | `198906202014012016` | Fitriani, S.Pd. | Guru Bimbingan Konseling (BK) | **0.2481** | Baik |
| **Peringkat 6** | **A17** | `199310082018032018` | Dian Kusuma, S.Pd. | Guru Bahasa Arab | **0.2481** | Baik |
| **Peringkat 7** | **A6** | `198708232011021013` | Fajar Nugroho, S.Pd. | Guru Sejarah Indonesia | **0.2405** | Baik |
| **Peringkat 8** | **A8** | `198904102014021003` | Budi Santoso, S.Si. | Guru Fisika | **0.2405** | Baik |
| **Peringkat 9** | **A12** | `199103052016021015` | Yusuf Habibi, S.Pd. | Guru Pendidikan Pancasila | **0.2353** | Baik |
| **Peringkat 10** | **A10** | `199005122015032004` | Ratna Dewi, S.Pd. | Guru Kimia | **0.2301** | Cukup |
| **Peringkat 11** | **A16** | `199307252018022008` | Nurul Hidayah, S.Pd. | Guru Bahasa Inggris | **0.2272** | Cukup |
| **Peringkat 12** | **A18** | `199401302019012014` | Maya Anggraini, S.Sn. | Guru Seni Budaya | **0.2225** | Cukup |
| **Peringkat 13** | **A3** | `198509172010021017` | Bambang Hermanto, S.Pd. | Guru Prakarya & Kewirausahaan | **0.2220** | Cukup |
| **Peringkat 14** | **A7** | `198811112012011009` | Agus Setiawan, S.Pd. | Guru PJOK | **0.2220** | Cukup |
| **Peringkat 15** | **A14** | `199202022017042006` | Dewi Sartika, M.Pd. | Guru Biologi | **0.2220** | Cukup |
| **Peringkat 16** | **A4** | `198612192010011011` | Dedi Supriyadi, S.Pd. | Guru Geografi | **0.2092** | Cukup |
| **Peringkat 17** | **A11** | `199009092015022010` | Eka Putri Rahayu, S.E. | Guru Ekonomi | **0.2092** | Cukup |
| **Peringkat 18** | **A15** | `199204152017032012` | Rina Marlina, S.Sos. | Guru Sosiologi | **0.2011** | Cukup |

---

### 4.5.8 Pembahasan Hasil Keputusan SPK MOORA

Berdasarkan hasil kalkulasi metode MOORA pada Juni 2026:
1. **Peringkat 1 (A1)**: Muhammad Rizky, S.Pd.I. (Guru Pendidikan Agama Islam) — Nilai Preferensi Yi = `0.2615` (Sangat Baik)
2. **Peringkat 2 (A2)**: Ahmad Fauzi, S.Pd. (Guru Matematika) — Nilai Preferensi Yi = `0.2615` (Sangat Baik)
3. **Peringkat 3 (A5)**: Siti Nurhaliza, M.Pd. (Guru Bahasa Indonesia) — Nilai Preferensi Yi = `0.2615` (Sangat Baik)
