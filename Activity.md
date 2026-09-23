Buat dan revisi SELURUH Activity Diagram AD-01 sampai AD-15 berdasarkan sistem aktual yang terdapat pada project.

Gunakan Use Case Diagram yang sudah ada sebagai acuan utama untuk aktor, fungsi, dan hak akses.

Jangan mengubah fungsi sistem, aktor, hak akses, nama Use Case, maupun proses yang memang terdapat pada sistem.

Saya ingin hasil Activity Diagram yang mengikuti standar UML dan gaya akademik skripsi S1 Teknik Informatika.

==================================================
DAFTAR ACTIVITY DIAGRAM
==================================================

AD-01 Login
→ UC-01 Melakukan Login

AD-02 Mengelola Data Pengguna
→ UC-02 Mengelola Data Pengguna

AD-03 Mengelola Data Guru
→ UC-03 Mengelola Data Guru

AD-04 Mengelola Kriteria dan Bobot
→ UC-04 Mengelola Kriteria dan Bobot

AD-05 Mengelola Skala Penilaian
→ UC-05 Mengelola Skala Penilaian

AD-06 Mengelola Periode Penilaian
→ UC-06 Mengelola Periode Penilaian

AD-07 Melakukan Penilaian Kinerja Guru
→ UC-07 Melakukan Penilaian Kinerja Guru

AD-08 Mencatat Hasil Penilaian
→ UC-08 Mencatat Hasil Penilaian

AD-09 Mengolah Penilaian dengan MOORA
→ UC-09 Mengolah Penilaian dengan MOORA

AD-10 Melihat Pemeringkatan MOORA
→ UC-10 Melihat Pemeringkatan MOORA

AD-11 Melihat Hasil Penilaian
→ UC-11 Melihat Hasil Penilaian

AD-12 Melihat Detail Penilaian
→ UC-12 Melihat Detail Penilaian

AD-13 Monitoring Kinerja Guru
→ UC-13 Monitoring Kinerja Guru

AD-14 Melihat Riwayat Penilaian
→ UC-14 Melihat Riwayat Penilaian

AD-15 Mencetak Laporan Penilaian
→ UC-15 Mencetak Laporan Penilaian


==================================================
1. PRINSIP UTAMA
==================================================

Setiap Use Case dibuat menjadi SATU Activity Diagram.

Gunakan pasangan kode:

UC-01 → AD-01
UC-02 → AD-02
UC-03 → AD-03
UC-04 → AD-04
UC-05 → AD-05
UC-06 → AD-06
UC-07 → AD-07
UC-08 → AD-08
UC-09 → AD-09
UC-10 → AD-10
UC-11 → AD-11
UC-12 → AD-12
UC-13 → AD-13
UC-14 → AD-14
UC-15 → AD-15

Sebelum membuat masing-masing diagram, periksa terlebih dahulu implementasi sistem dan Use Case yang bersangkutan.

Jangan membuat alur berdasarkan asumsi umum apabila sistem aktual menunjukkan alur yang berbeda.


==================================================
2. SWIMLANE
==================================================

Gunakan swimlane sederhana berdasarkan pihak yang melakukan aktivitas.

Secara umum gunakan:

| Pengguna/Aktor | Sistem SPK MOORA |

Jika satu Use Case hanya melibatkan Administrator, gunakan:

| Administrator | Sistem SPK MOORA |

Jika melibatkan Kepala Sekolah:

| Kepala Sekolah | Sistem SPK MOORA |

Jika melibatkan Guru:

| Guru | Sistem SPK MOORA |

Jika proses memang melibatkan lebih dari satu aktor, gunakan swimlane sesuai kebutuhan aktual.

Jangan membuat swimlane berdasarkan:

- Controller
- API
- Service
- Database
- Prisma
- Framework
- File program
- Fungsi pemrograman

Activity Diagram harus menunjukkan interaksi pengguna dengan sistem pada tingkat konseptual.


==================================================
3. STRUKTUR ALUR
==================================================

Setiap Activity Diagram harus memiliki:

Initial Node
↓
Aktivitas pengguna
↓
Aktivitas sistem
↓
Decision jika diperlukan
↓
Aktivitas lanjutan
↓
Hasil proses
↓
Activity Final Node

Tidak semua diagram harus memiliki Decision Node.

Gunakan Decision Node hanya apabila proses aktual memang memiliki kondisi atau percabangan.

Jika ada percabangan, beri guard condition yang jelas:

[Valid]
[Tidak Valid]

atau kondisi yang sesuai dengan proses aktual.


==================================================
4. POLA INTERAKSI
==================================================

Gunakan pola sederhana:

PENGGUNA
→ melakukan tindakan

SISTEM
→ memproses/menampilkan hasil

PENGGUNA
→ memberikan input atau memilih tindakan berikutnya

SISTEM
→ memberikan respons

Jangan membuat Activity Diagram hanya berisi aktivitas sistem.

Harus terlihat siapa yang melakukan aktivitas.


==================================================
5. TINGKAT DETAIL
==================================================

Gunakan tingkat detail MENENGAH.

Diagram harus cukup detail untuk menjelaskan proses, tetapi tidak terlalu teknis.

Gunakan istilah akademik yang sederhana.

Contoh:

BENAR:
"Memasukkan Data Guru"

"Memvalidasi Data"

"Menyimpan Data"

"Menampilkan Data Guru"

"Melakukan Perhitungan MOORA"

"Menampilkan Hasil Pemeringkatan"

HINDARI:
"POST /api/guru"

"Execute createGuru()"

"Query database"

"Prisma create()"

"JWT verification"

"bcrypt.compare()"

Nama file, fungsi, API, framework, dan kode program tidak boleh ditampilkan sebagai aktivitas.


==================================================
6. KHUSUS AD-01 LOGIN
==================================================

Gunakan alur:

Mulai
→ Membuka Halaman Login
→ Sistem Menampilkan Formulir Login
→ Memasukkan Username dan Password
→ Sistem Memvalidasi Data Login
→ Decision "Data Login Valid?"

[Tidak Valid]
→ Menampilkan Pesan Kesalahan
→ Kembali ke Formulir Login

[Valid]
→ Memverifikasi Hak Akses
→ Menampilkan Dashboard Sesuai Hak Akses
→ Selesai

Sesuaikan dengan sistem aktual apabila terdapat perbedaan.


==================================================
7. AD-02 SAMPAI AD-06
==================================================

Untuk proses pengelolaan data, gunakan pola umum:

Membuka menu
→ Sistem menampilkan data
→ Pengguna memilih tindakan
→ Tambah/Ubah/Hapus sesuai fitur aktual
→ Sistem melakukan validasi
→ Decision jika diperlukan
→ Sistem menyimpan perubahan
→ Sistem menampilkan hasil
→ Selesai

Sesuaikan aktivitas dengan fitur aktual masing-masing Use Case.

Jangan menambahkan operasi CRUD apabila operasi tersebut tidak tersedia pada sistem.


==================================================
8. AD-07 PENILAIAN KINERJA GURU
==================================================

Gambarkan alur aktual Kepala Sekolah dalam melakukan penilaian.

Secara konseptual:

Memilih periode
→ Memilih guru
→ Sistem menampilkan kriteria penilaian
→ Memberikan nilai
→ Sistem memvalidasi nilai
→ Menyimpan penilaian
→ Menampilkan hasil/status penilaian
→ Selesai

Sesuaikan dengan implementasi aktual.


==================================================
9. AD-08 MENCATAT HASIL PENILAIAN
==================================================

Gambarkan proses pencatatan hasil penilaian.

Tunjukkan:

data/hasil penilaian
→ pemeriksaan data
→ penyimpanan hasil
→ konfirmasi hasil penyimpanan

Jangan memasukkan detail struktur database.


==================================================
10. AD-09 PENGOLAHAN MOORA
==================================================

Ini merupakan Activity Diagram khusus proses algoritma MOORA.

Gambarkan tahapan secara konseptual berdasarkan implementasi aktual.

Jika tahapan tersebut memang terdapat dalam sistem, gunakan urutan:

Data Penilaian
→ Membentuk Matriks Keputusan
→ Melakukan Normalisasi
→ Melakukan Pembobotan
→ Menghitung Nilai Optimasi/Preferensi
→ Menghasilkan Hasil Perhitungan
→ Menyimpan Hasil
→ Selesai

Jangan memasukkan rumus panjang ke dalam Activity Diagram.

Rumus dan penjelasan matematis MOORA dijelaskan pada bagian perancangan/perhitungan MOORA.

Gunakan istilah yang mudah dipahami mahasiswa S1.


==================================================
11. AD-10 PEMERINGKATAN MOORA
==================================================

Gambarkan:

Memilih periode/data
→ Sistem mengambil hasil perhitungan
→ Sistem mengurutkan nilai preferensi
→ Sistem menampilkan pemeringkatan
→ Selesai

Sesuaikan dengan sistem aktual.


==================================================
12. AD-11 HASIL PENILAIAN
==================================================

Gambarkan proses:

Membuka hasil penilaian
→ Sistem mengambil data hasil
→ Sistem menampilkan hasil penilaian
→ Selesai

Jika terdapat pemilihan periode atau guru, tampilkan sesuai sistem.


==================================================
13. AD-12 DETAIL PENILAIAN
==================================================

Gambarkan:

Memilih hasil penilaian
→ Sistem mengambil detail
→ Sistem menampilkan rincian penilaian
→ Selesai


==================================================
14. AD-13 MONITORING KINERJA GURU
==================================================

Gambarkan:

Membuka menu monitoring
→ Memilih data/periode jika tersedia
→ Sistem mengambil data
→ Sistem menampilkan informasi monitoring
→ Selesai

Gunakan aktivitas yang benar-benar tersedia pada sistem.


==================================================
15. AD-14 RIWAYAT PENILAIAN
==================================================

Gambarkan:

Membuka riwayat
→ Memilih periode/data jika tersedia
→ Sistem mengambil riwayat
→ Sistem menampilkan riwayat penilaian
→ Selesai


==================================================
16. AD-15 MENCETAK LAPORAN PENILAIAN
==================================================

Gambarkan:

Membuka menu laporan
→ Memilih periode/data laporan
→ Sistem menyiapkan data
→ Sistem menampilkan/menyiapkan laporan
→ Pengguna memilih cetak
→ Sistem menghasilkan laporan
→ Selesai

Sesuaikan dengan mekanisme pencetakan yang benar-benar tersedia pada sistem.


==================================================
17. NOTASI UML
==================================================

Gunakan notasi Activity Diagram UML yang benar:

● Initial Node
○ Action/Activity
◇ Decision Node
● Activity Final Node

Gunakan Control Flow untuk menghubungkan aktivitas.

Gunakan Merge Node jika memang diperlukan.

Jangan menggunakan simbol flowchart yang tidak sesuai dengan UML.


==================================================
18. GAYA VISUAL
==================================================

Gunakan gaya akademik skripsi S1 Teknik Informatika.

Gunakan:

- background putih;
- garis hitam;
- bentuk UML standar;
- font formal;
- ukuran elemen konsisten;
- jarak antaraktivitas proporsional;
- swimlane jelas;
- layout sederhana;
- orientasi atas ke bawah atau kiri ke kanan secara konsisten.

Jangan menggunakan:

- warna dekoratif berlebihan;
- ikon;
- ilustrasi;
- gradient;
- efek 3D;
- elemen dekoratif;
- tampilan seperti infografis.


==================================================
19. KETERBACAAN
==================================================

Setiap diagram harus mudah dibaca ketika dimasukkan ke BAB IV skripsi.

Hindari:

- garis menyilang;
- control flow terlalu panjang;
- aktivitas bertumpuk;
- teks bertabrakan;
- decision node terlalu kompleks;
- alur berputar tanpa alasan.

Jangan memperbanyak aktivitas hanya untuk membuat diagram terlihat detail.


==================================================
20. KONSISTENSI DENGAN USE CASE
==================================================

Setiap Activity Diagram harus menjawab:

"Bagaimana Use Case ini berjalan?"

Bukan:

"Bagaimana source code menjalankan fitur ini?"

Karena itu, Activity Diagram harus berada pada tingkat perancangan sistem.

Pastikan setiap aktivitas memang mendukung tujuan Use Case.

Jangan menambahkan aktivitas yang tidak diperlukan.


==================================================
21. VALIDASI SETIAP DIAGRAM
==================================================

Sebelum menyelesaikan masing-masing Activity Diagram, periksa:

- aktor sudah benar;
- hak akses sudah benar;
- aktivitas sesuai Use Case;
- alur dimulai dari Initial Node;
- alur berakhir pada Final Node;
- decision memiliki cabang yang jelas;
- tidak ada alur yang terputus;
- tidak ada aktivitas yang tidak relevan;
- tidak ada detail source code;
- diagram mudah dibaca.


==================================================
22. OUTPUT
==================================================

Buat 15 Activity Diagram secara terpisah:

AD-01 Login
AD-02 Mengelola Data Pengguna
AD-03 Mengelola Data Guru
AD-04 Mengelola Kriteria dan Bobot
AD-05 Mengelola Skala Penilaian
AD-06 Mengelola Periode Penilaian
AD-07 Melakukan Penilaian Kinerja Guru
AD-08 Mencatat Hasil Penilaian
AD-09 Mengolah Penilaian dengan MOORA
AD-10 Melihat Pemeringkatan MOORA
AD-11 Melihat Hasil Penilaian
AD-12 Melihat Detail Penilaian
AD-13 Monitoring Kinerja Guru
AD-14 Melihat Riwayat Penilaian
AD-15 Mencetak Laporan Penilaian

Jangan menggabungkan seluruh Activity Diagram menjadi satu diagram besar.

Pertahankan kode AD-01 sampai AD-15.

Setiap diagram harus berdiri sendiri dan siap digunakan sebagai gambar pada BAB IV.

Gunakan gaya penulisan aktivitas yang singkat, akademik, dan tidak terlalu teknis.

Prioritas akhir:

1. Kesesuaian dengan sistem aktual.
2. Ketepatan UML.
3. Konsistensi dengan Use Case Diagram.
4. Keterbacaan.
5. Kesederhanaan.
6. Kerapian visual.

Jangan mengorbankan ketepatan proses hanya demi membuat diagram lebih sederhana.