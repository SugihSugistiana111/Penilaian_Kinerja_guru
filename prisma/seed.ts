import { PrismaClient } from '@prisma/client';
import bcrypt from 'bcryptjs';

const prisma = new PrismaClient();

async function main() {
  console.log('--- Memulai Seeding Data SPK Penilaian Kinerja Guru SMA Al-Ihsan Boarding School ---');

  // Bersihkan data lama jika ada
  await prisma.detailMoora.deleteMany();
  await prisma.hasilMoora.deleteMany();
  await prisma.detailPenilaian.deleteMany();
  await prisma.penilaian.deleteMany();
  await prisma.logAktivitas.deleteMany();
  await prisma.user.deleteMany();
  await prisma.guru.deleteMany();
  await prisma.skalaPenilaian.deleteMany();
  await prisma.kriteria.deleteMany();
  await prisma.periodePenilaian.deleteMany();
  await prisma.role.deleteMany();

  // 1. Roles
  const roleAdmin = await prisma.role.create({ data: { namaRole: 'ADMIN' } });
  const roleKepsek = await prisma.role.create({ data: { namaRole: 'KEPALA_SEKOLAH' } });
  const roleGuru = await prisma.role.create({ data: { namaRole: 'GURU' } });

  // 2. Kriteria (Sesuai Bab III / README.MD)
  const kriteriaC1 = await prisma.kriteria.create({
    data: {
      kode: 'C1',
      nama: 'Kehadiran',
      bobot: 0.35,
      jenis: 'BENEFIT',
      status: true,
    },
  });

  const kriteriaC2 = await prisma.kriteria.create({
    data: {
      kode: 'C2',
      nama: 'Ketepatan Waktu',
      bobot: 0.25,
      jenis: 'BENEFIT',
      status: true,
    },
  });

  const kriteriaC3 = await prisma.kriteria.create({
    data: {
      kode: 'C3',
      nama: 'Kelengkapan Perangkat Pembelajaran',
      bobot: 0.25,
      jenis: 'BENEFIT',
      status: true,
    },
  });

  const kriteriaC4 = await prisma.kriteria.create({
    data: {
      kode: 'C4',
      nama: 'Kelengkapan Administrasi Penilaian',
      bobot: 0.15,
      jenis: 'BENEFIT',
      status: true,
    },
  });

  const allKriteria = [kriteriaC1, kriteriaC2, kriteriaC3, kriteriaC4];

  // 3. Skala Penilaian
  const skalaData = [
    { nilai: 1, label: 'Sangat Kurang', keterangan: 'Kinerja jauh di bawah standar (1.00 - 1.99)' },
    { nilai: 2, label: 'Kurang', keterangan: 'Kinerja belum memenuhi standar (2.00 - 2.99)' },
    { nilai: 3, label: 'Cukup', keterangan: 'Kinerja memenuhi standar minimal (3.00 - 3.99)' },
    { nilai: 4, label: 'Baik', keterangan: 'Kinerja melampaui standar (4.00 - 4.49)' },
    { nilai: 5, label: 'Sangat Baik', keterangan: 'Kinerja istimewa dan teladan (4.50 - 5.00)' },
  ];

  for (const k of allKriteria) {
    for (const s of skalaData) {
      await prisma.skalaPenilaian.create({
        data: {
          kriteriaId: k.id,
          nilai: s.nilai,
          label: s.label,
          keterangan: s.keterangan,
        },
      });
    }
  }

  // 4. Data 18 Guru SMA Al-Ihsan Boarding School
  const daftarGuruData = [
    {
      nip: '198501152010011001',
      nama: 'Ahmad Fauzi, S.Pd.',
      jenisKelamin: 'L',
      jabatanTugasMengajar: 'Guru Matematika',
      tugasTambahanUtama: 'Wakil Kepala Sekolah Bid. Kurikulum',
      tugasTambahanLain: 'Pembina OSIS',
      jumlahSiswaPerRombel: 30,
      jumlahJamAjar: 24,
      mengajarKelas10: true,
      mengajarKelas11: true,
      mengajarKelas12: false,
    },
    {
      nip: '198703222011012002',
      nama: 'Siti Nurhaliza, M.Pd.',
      jenisKelamin: 'P',
      jabatanTugasMengajar: 'Guru Bahasa Indonesia',
      tugasTambahanUtama: 'Kepala Perpustakaan',
      tugasTambahanLain: 'Pembina Mading & Literasi',
      jumlahSiswaPerRombel: 32,
      jumlahJamAjar: 26,
      mengajarKelas10: true,
      mengajarKelas11: true,
      mengajarKelas12: true,
    },
    {
      nip: '198904102014021003',
      nama: 'Budi Santoso, S.Si.',
      jenisKelamin: 'L',
      jabatanTugasMengajar: 'Guru Fisika',
      tugasTambahanUtama: 'Kepala Laboratorium IPA',
      tugasTambahanLain: 'Pembina Olimpiade Sains',
      jumlahSiswaPerRombel: 28,
      jumlahJamAjar: 24,
      mengajarKelas10: false,
      mengajarKelas11: true,
      mengajarKelas12: true,
    },
    {
      nip: '199005122015032004',
      nama: 'Ratna Dewi, S.Pd.',
      jenisKelamin: 'P',
      jabatanTugasMengajar: 'Guru Kimia',
      tugasTambahanUtama: 'Wali Kelas 11 MIPA 1',
      tugasTambahanLain: 'Koordinator Karya Ilmiah Remaja',
      jumlahSiswaPerRombel: 28,
      jumlahJamAjar: 24,
      mengajarKelas10: true,
      mengajarKelas11: true,
      mengajarKelas12: false,
    },
    {
      nip: '199108182016011005',
      nama: 'Hendra Gunawan, S.Kom.',
      jenisKelamin: 'L',
      jabatanTugasMengajar: 'Guru Informatika',
      tugasTambahanUtama: 'Kepala Lab Komputer & IT',
      tugasTambahanLain: 'Pengelola Website Sekolah',
      jumlahSiswaPerRombel: 30,
      jumlahJamAjar: 24,
      mengajarKelas10: true,
      mengajarKelas11: true,
      mengajarKelas12: true,
    },
    {
      nip: '199202022017042006',
      nama: 'Dewi Sartika, M.Pd.',
      jenisKelamin: 'P',
      jabatanTugasMengajar: 'Guru Biologi',
      tugasTambahanUtama: 'Wali Kelas 10 MIPA 2',
      tugasTambahanLain: 'Pembina PMR',
      jumlahSiswaPerRombel: 30,
      jumlahJamAjar: 26,
      mengajarKelas10: true,
      mengajarKelas11: true,
      mengajarKelas12: false,
    },
    {
      nip: '198406142009031007',
      nama: 'Muhammad Rizky, S.Pd.I.',
      jenisKelamin: 'L',
      jabatanTugasMengajar: 'Guru Pendidikan Agama Islam',
      tugasTambahanUtama: 'Wakil Kepala Sekolah Bid. Kesiswaan',
      tugasTambahanLain: 'Pembina Tahfidz & Keasramaan',
      jumlahSiswaPerRombel: 32,
      jumlahJamAjar: 28,
      mengajarKelas10: true,
      mengajarKelas11: true,
      mengajarKelas12: true,
    },
    {
      nip: '199307252018022008',
      nama: 'Nurul Hidayah, S.Pd.',
      jenisKelamin: 'P',
      jabatanTugasMengajar: 'Guru Bahasa Inggris',
      tugasTambahanUtama: 'Wali Kelas 12 Bahasa',
      tugasTambahanLain: 'Pembina English Club',
      jumlahSiswaPerRombel: 28,
      jumlahJamAjar: 24,
      mengajarKelas10: true,
      mengajarKelas11: false,
      mengajarKelas12: true,
    },
    {
      nip: '198811112012011009',
      nama: 'Agus Setiawan, S.Pd.',
      jenisKelamin: 'L',
      jabatanTugasMengajar: 'Guru PJOK',
      tugasTambahanUtama: 'Koordinator Ekstrakurikuler Olahraga',
      tugasTambahanLain: 'Pembina Futsal & Basket',
      jumlahSiswaPerRombel: 32,
      jumlahJamAjar: 24,
      mengajarKelas10: true,
      mengajarKelas11: true,
      mengajarKelas12: true,
    },
    {
      nip: '199009092015022010',
      nama: 'Eka Putri Rahayu, S.E.',
      jenisKelamin: 'P',
      jabatanTugasMengajar: 'Guru Ekonomi',
      tugasTambahanUtama: 'Wali Kelas 11 IPS 1',
      tugasTambahanLain: 'Pembina Koperasi Sekolah',
      jumlahSiswaPerRombel: 30,
      jumlahJamAjar: 24,
      mengajarKelas10: true,
      mengajarKelas11: true,
      mengajarKelas12: false,
    },
    {
      nip: '198612192010011011',
      nama: 'Dedi Supriyadi, S.Pd.',
      jenisKelamin: 'L',
      jabatanTugasMengajar: 'Guru Geografi',
      tugasTambahanUtama: 'Wali Kelas 12 IPS 2',
      tugasTambahanLain: 'Pembina Pramuka',
      jumlahSiswaPerRombel: 30,
      jumlahJamAjar: 24,
      mengajarKelas10: false,
      mengajarKelas11: true,
      mengajarKelas12: true,
    },
    {
      nip: '199204152017032012',
      nama: 'Rina Marlina, S.Sos.',
      jenisKelamin: 'P',
      jabatanTugasMengajar: 'Guru Sosiologi',
      tugasTambahanUtama: 'Wali Kelas 10 IPS 1',
      tugasTambahanLain: 'Pembina Debat Sosial',
      jumlahSiswaPerRombel: 30,
      jumlahJamAjar: 24,
      mengajarKelas10: true,
      mengajarKelas11: true,
      mengajarKelas12: false,
    },
    {
      nip: '198708232011021013',
      nama: 'Fajar Nugroho, S.Pd.',
      jenisKelamin: 'L',
      jabatanTugasMengajar: 'Guru Sejarah Indonesia',
      tugasTambahanUtama: 'Wakil Kepala Sekolah Bid. Humas',
      tugasTambahanLain: 'Pengelola Museum Sekolah',
      jumlahSiswaPerRombel: 32,
      jumlahJamAjar: 24,
      mengajarKelas10: true,
      mengajarKelas11: true,
      mengajarKelas12: true,
    },
    {
      nip: '199401302019012014',
      nama: 'Maya Anggraini, S.Sn.',
      jenisKelamin: 'P',
      jabatanTugasMengajar: 'Guru Seni Budaya',
      tugasTambahanUtama: 'Wali Kelas 10 MIPA 1',
      tugasTambahanLain: 'Pembina Paduan Suara & Teater',
      jumlahSiswaPerRombel: 32,
      jumlahJamAjar: 24,
      mengajarKelas10: true,
      mengajarKelas11: true,
      mengajarKelas12: true,
    },
    {
      nip: '199103052016021015',
      nama: 'Yusuf Habibi, S.Pd.',
      jenisKelamin: 'L',
      jabatanTugasMengajar: 'Guru Pendidikan Pancasila',
      tugasTambahanUtama: 'Wali Kelas 11 IPS 2',
      tugasTambahanLain: 'Pembina Paskibra',
      jumlahSiswaPerRombel: 30,
      jumlahJamAjar: 24,
      mengajarKelas10: true,
      mengajarKelas11: true,
      mengajarKelas12: true,
    },
    {
      nip: '198906202014012016',
      nama: 'Fitriani, S.Pd.',
      jenisKelamin: 'P',
      jabatanTugasMengajar: 'Guru Bimbingan Konseling (BK)',
      tugasTambahanUtama: 'Koordinator BK & Karir Siswa',
      tugasTambahanLain: 'Konselor Asrama',
      jumlahSiswaPerRombel: 32,
      jumlahJamAjar: 24,
      mengajarKelas10: true,
      mengajarKelas11: true,
      mengajarKelas12: true,
    },
    {
      nip: '198509172010021017',
      nama: 'Bambang Hermanto, S.Pd.',
      jenisKelamin: 'L',
      jabatanTugasMengajar: 'Guru Prakarya & Kewirausahaan',
      tugasTambahanUtama: 'Wakil Kepala Sekolah Bid. Sarpras',
      tugasTambahanLain: 'Pembina Inkubator Bisnis Santri',
      jumlahSiswaPerRombel: 30,
      jumlahJamAjar: 24,
      mengajarKelas10: true,
      mengajarKelas11: true,
      mengajarKelas12: false,
    },
    {
      nip: '199310082018032018',
      nama: 'Dian Kusuma, S.Pd.',
      jenisKelamin: 'P',
      jabatanTugasMengajar: 'Guru Bahasa Arab',
      tugasTambahanUtama: 'Wali Kelas 12 MIPA 1',
      tugasTambahanLain: 'Pembina Arabic Club & Pidato',
      jumlahSiswaPerRombel: 30,
      jumlahJamAjar: 26,
      mengajarKelas10: true,
      mengajarKelas11: true,
      mengajarKelas12: true,
    },
  ];

  const createdGurus: any[] = [];
  for (const g of daftarGuruData) {
    const guru = await prisma.guru.create({ data: g });
    createdGurus.push(guru);
  }

  // 5. Password hashing
  const salt = await bcrypt.genSalt(10);
  const passwordAdminHash = await bcrypt.hash('admin123', salt);
  const passwordKepsekHash = await bcrypt.hash('kepsek123', salt);
  const passwordGuruHash = await bcrypt.hash('guru123', salt);

  // Akun Admin
  await prisma.user.create({
    data: {
      nama: 'M. Hidad Abdillah, S.Pd.',
      username: 'admin',
      password: passwordAdminHash,
      roleId: roleAdmin.id,
      status: true,
    },
  });

  // Akun Kepala Sekolah
  await prisma.user.create({
    data: {
      nama: 'Dr. H. Mulyadi, M.Pd. (Kepala Sekolah)',
      username: 'kepsek',
      password: passwordKepsekHash,
      roleId: roleKepsek.id,
      status: true,
    },
  });

  // Akun untuk masing-masing Guru (guru1 s/d guru18)
  for (let i = 0; i < createdGurus.length; i++) {
    const guru = createdGurus[i];
    await prisma.user.create({
      data: {
        nama: guru.nama,
        username: `guru${i + 1}`,
        password: passwordGuruHash,
        roleId: roleGuru.id,
        guruId: guru.id,
        status: true,
      },
    });
  }

  // 6. Data Periode
  // A. Periode Riwayat: Mei 2026 (SELESAI)
  const periodeMei = await prisma.periodePenilaian.create({
    data: {
      bulan: 'Mei',
      tahun: 2026,
      namaPeriode: 'Mei 2026',
      status: 'SELESAI',
    },
  });

  // B. Periode Berjalan: Juni 2026 (AKTIF)
  const periodeJuni = await prisma.periodePenilaian.create({
    data: {
      bulan: 'Juni',
      tahun: 2026,
      namaPeriode: 'Juni 2026',
      status: 'AKTIF',
    },
  });

  // 7. Nilai Simulasi Periode Mei 2026 (Lengkap 18 guru dengan perhitungan MOORA)
  // Bobot: C1=0.35, C2=0.25, C3=0.25, C4=0.15
  const rawScoresMei: Array<{ guruIndex: number; c1: number; c2: number; c3: number; c4: number }> = [
    { guruIndex: 0, c1: 5, c2: 5, c3: 5, c4: 4 }, // Ahmad Fauzi
    { guruIndex: 1, c1: 5, c2: 4, c3: 5, c4: 5 }, // Siti Nurhaliza
    { guruIndex: 2, c1: 4, c2: 5, c3: 4, c4: 4 }, // Budi Santoso
    { guruIndex: 3, c1: 4, c2: 4, c3: 5, c4: 4 }, // Ratna Dewi
    { guruIndex: 4, c1: 5, c2: 5, c3: 4, c4: 5 }, // Hendra Gunawan
    { guruIndex: 5, c1: 4, c2: 4, c3: 4, c4: 4 }, // Dewi Sartika
    { guruIndex: 6, c1: 5, c2: 5, c3: 5, c4: 5 }, // Muhammad Rizky
    { guruIndex: 7, c1: 4, c2: 4, c3: 4, c4: 3 }, // Nurul Hidayah
    { guruIndex: 8, c1: 4, c2: 4, c3: 4, c4: 4 }, // Agus Setiawan
    { guruIndex: 9, c1: 4, c2: 3, c3: 4, c4: 4 }, // Eka Putri Rahayu
    { guruIndex: 10, c1: 4, c2: 4, c3: 3, c4: 4 }, // Dedi Supriyadi
    { guruIndex: 11, c1: 3, c2: 4, c3: 4, c4: 3 }, // Rina Marlina
    { guruIndex: 12, c1: 5, c2: 4, c3: 4, c4: 4 }, // Fajar Nugroho
    { guruIndex: 13, c1: 4, c2: 4, c3: 4, c4: 4 }, // Maya Anggraini
    { guruIndex: 14, c1: 4, c2: 5, c3: 4, c4: 4 }, // Yusuf Habibi
    { guruIndex: 15, c1: 5, c2: 4, c3: 5, c4: 4 }, // Fitriani
    { guruIndex: 16, c1: 4, c2: 4, c3: 4, c4: 5 }, // Bambang Hermanto
    { guruIndex: 17, c1: 5, c2: 4, c3: 4, c4: 4 }, // Dian Kusuma
  ];

  // Simpan Penilaian Mei 2026
  for (const s of rawScoresMei) {
    const guru = createdGurus[s.guruIndex];
    const pen = await prisma.penilaian.create({
      data: {
        guruId: guru.id,
        periodeId: periodeMei.id,
        dinilaiOleh: 'Dr. H. Mulyadi, M.Pd.',
        status: 'SELESAI',
        catatan: 'Penilaian Kinerja Berkala Mei 2026',
        details: {
          create: [
            { kriteriaId: kriteriaC1.id, nilai: s.c1 },
            { kriteriaId: kriteriaC2.id, nilai: s.c2 },
            { kriteriaId: kriteriaC3.id, nilai: s.c3 },
            { kriteriaId: kriteriaC4.id, nilai: s.c4 },
          ],
        },
      },
    });
  }

  // Hitung MOORA untuk Mei 2026
  // Hitung pembagi normalisasi: sqrt(sum(x^2)) untuk setiap kriteria
  let sumSqC1 = 0, sumSqC2 = 0, sumSqC3 = 0, sumSqC4 = 0;
  for (const s of rawScoresMei) {
    sumSqC1 += s.c1 * s.c1;
    sumSqC2 += s.c2 * s.c2;
    sumSqC3 += s.c3 * s.c3;
    sumSqC4 += s.c4 * s.c4;
  }
  const normDivC1 = Math.sqrt(sumSqC1);
  const normDivC2 = Math.sqrt(sumSqC2);
  const normDivC3 = Math.sqrt(sumSqC3);
  const normDivC4 = Math.sqrt(sumSqC4);

  const mooraCalculationsMei = rawScoresMei.map((s) => {
    const guru = createdGurus[s.guruIndex];
    const rC1 = s.c1 / normDivC1;
    const rC2 = s.c2 / normDivC2;
    const rC3 = s.c3 / normDivC3;
    const rC4 = s.c4 / normDivC4;

    const wC1 = rC1 * 0.35;
    const wC2 = rC2 * 0.25;
    const wC3 = rC3 * 0.25;
    const wC4 = rC4 * 0.15;

    const yi = wC1 + wC2 + wC3 + wC4;

    return {
      guruId: guru.id,
      yi,
      details: [
        { kriteriaId: kriteriaC1.id, nilaiAwal: s.c1, nilaiNormalisasi: rC1, bobot: 0.35, nilaiTerbobot: wC1 },
        { kriteriaId: kriteriaC2.id, nilaiAwal: s.c2, nilaiNormalisasi: rC2, bobot: 0.25, nilaiTerbobot: wC2 },
        { kriteriaId: kriteriaC3.id, nilaiAwal: s.c3, nilaiNormalisasi: rC3, bobot: 0.25, nilaiTerbobot: wC3 },
        { kriteriaId: kriteriaC4.id, nilaiAwal: s.c4, nilaiNormalisasi: rC4, bobot: 0.15, nilaiTerbobot: wC4 },
      ],
    };
  });

  // Sort descending by Yi for ranking
  mooraCalculationsMei.sort((a, b) => b.yi - a.yi);

  // Simpan Hasil MOORA Mei 2026
  for (let rank = 0; rank < mooraCalculationsMei.length; rank++) {
    const item = mooraCalculationsMei[rank];
    await prisma.hasilMoora.create({
      data: {
        guruId: item.guruId,
        periodeId: periodeMei.id,
        nilaiPreferensi: parseFloat(item.yi.toFixed(4)),
        ranking: rank + 1,
        details: {
          create: item.details.map((d) => ({
            kriteriaId: d.kriteriaId,
            nilaiAwal: d.nilaiAwal,
            nilaiNormalisasi: parseFloat(d.nilaiNormalisasi.toFixed(4)),
            bobot: d.bobot,
            nilaiTerbobot: parseFloat(d.nilaiTerbobot.toFixed(4)),
          })),
        },
      },
    });
  }

  // 8. Periode Juni 2026 (AKTIF) - Berikan penilaian awal untuk 18 guru sesuai Tabel 4.34 Skripsi
  const rawScoresJuniSkripsi = [
    { nip: '198406142009031007', c1: 5, c2: 5, c3: 5, c4: 5 }, // A1 Muhammad Rizky, S.Pd.I.
    { nip: '198501152010011001', c1: 5, c2: 5, c3: 5, c4: 5 }, // A2 Ahmad Fauzi, S.Pd.
    { nip: '198509172010021017', c1: 4, c2: 5, c3: 4, c4: 4 }, // A3 Bambang Hermanto, S.Pd.
    { nip: '198612192010011011', c1: 4, c2: 4, c3: 4, c4: 4 }, // A4 Dedi Supriyadi, S.Pd.
    { nip: '198703222011012002', c1: 5, c2: 5, c3: 5, c4: 5 }, // A5 Siti Nurhaliza, M.Pd.
    { nip: '198708232011021013', c1: 5, c2: 4, c3: 5, c4: 4 }, // A6 Fajar Nugroho, S.Pd.
    { nip: '198811112012011009', c1: 4, c2: 5, c3: 4, c4: 4 }, // A7 Agus Setiawan, S.Pd.
    { nip: '198904102014021003', c1: 5, c2: 4, c3: 5, c4: 4 }, // A8 Budi Santoso, S.Si.
    { nip: '198906202014012016', c1: 5, c2: 5, c3: 4, c4: 5 }, // A9 Fitriani, S.Pd.
    { nip: '199005122015032004', c1: 4, c2: 5, c3: 4, c4: 5 }, // A10 Ratna Dewi, S.Pd.
    { nip: '199009092015022010', c1: 4, c2: 4, c3: 4, c4: 4 }, // A11 Eka Putri Rahayu, S.E.
    { nip: '199103052016021015', c1: 5, c2: 4, c3: 4, c4: 5 }, // A12 Yusuf Habibi, S.Pd.
    { nip: '199108182016011005', c1: 5, c2: 5, c3: 5, c4: 4 }, // A13 Hendra Gunawan, S.Kom.
    { nip: '199202022017042006', c1: 4, c2: 5, c3: 4, c4: 4 }, // A14 Dewi Sartika, M.Pd.
    { nip: '199204152017032012', c1: 4, c2: 4, c3: 4, c4: 3 }, // A15 Rina Marlina, S.Sos.
    { nip: '199307252018022008', c1: 5, c2: 4, c3: 4, c4: 4 }, // A16 Nurul Hidayah, S.Pd.
    { nip: '199310082018032018', c1: 5, c2: 5, c3: 4, c4: 5 }, // A17 Dian Kusuma, S.Pd.
    { nip: '199401302019012014', c1: 4, c2: 4, c3: 5, c4: 4 }, // A18 Maya Anggraini, S.Sn.
  ];

  for (const s of rawScoresJuniSkripsi) {
    const guru = createdGurus.find(g => g.nip === s.nip)!;
    await prisma.penilaian.create({
      data: {
        guruId: guru.id,
        periodeId: periodeJuni.id,
        dinilaiOleh: 'Dr. H. Mulyadi, M.Pd.',
        status: 'SELESAI',
        catatan: 'Penilaian Kinerja Periode Juni 2026',
        details: {
          create: [
            { kriteriaId: kriteriaC1.id, nilai: s.c1 },
            { kriteriaId: kriteriaC2.id, nilai: s.c2 },
            { kriteriaId: kriteriaC3.id, nilai: s.c3 },
            { kriteriaId: kriteriaC4.id, nilai: s.c4 },
          ],
        },
      },
    });
  }

  // Hitung MOORA untuk Juni 2026 juga agar siap pakai
  let sumSqC1_j = 0, sumSqC2_j = 0, sumSqC3_j = 0, sumSqC4_j = 0;
  for (const s of rawScoresJuni) {
    sumSqC1_j += s.c1 * s.c1;
    sumSqC2_j += s.c2 * s.c2;
    sumSqC3_j += s.c3 * s.c3;
    sumSqC4_j += s.c4 * s.c4;
  }
  const normDivC1_j = Math.sqrt(sumSqC1_j);
  const normDivC2_j = Math.sqrt(sumSqC2_j);
  const normDivC3_j = Math.sqrt(sumSqC3_j);
  const normDivC4_j = Math.sqrt(sumSqC4_j);

  const mooraCalculationsJuni = rawScoresJuni.map((s) => {
    const guru = createdGurus[s.guruIndex];
    const rC1 = s.c1 / normDivC1_j;
    const rC2 = s.c2 / normDivC2_j;
    const rC3 = s.c3 / normDivC3_j;
    const rC4 = s.c4 / normDivC4_j;

    const wC1 = rC1 * 0.35;
    const wC2 = rC2 * 0.25;
    const wC3 = rC3 * 0.25;
    const wC4 = rC4 * 0.15;

    const yi = wC1 + wC2 + wC3 + wC4;

    return {
      guruId: guru.id,
      yi,
      details: [
        { kriteriaId: kriteriaC1.id, nilaiAwal: s.c1, nilaiNormalisasi: rC1, bobot: 0.35, nilaiTerbobot: wC1 },
        { kriteriaId: kriteriaC2.id, nilaiAwal: s.c2, nilaiNormalisasi: rC2, bobot: 0.25, nilaiTerbobot: wC2 },
        { kriteriaId: kriteriaC3.id, nilaiAwal: s.c3, nilaiNormalisasi: rC3, bobot: 0.25, nilaiTerbobot: wC3 },
        { kriteriaId: kriteriaC4.id, nilaiAwal: s.c4, nilaiNormalisasi: rC4, bobot: 0.15, nilaiTerbobot: wC4 },
      ],
    };
  });

  mooraCalculationsJuni.sort((a, b) => b.yi - a.yi);

  for (let rank = 0; rank < mooraCalculationsJuni.length; rank++) {
    const item = mooraCalculationsJuni[rank];
    await prisma.hasilMoora.create({
      data: {
        guruId: item.guruId,
        periodeId: periodeJuni.id,
        nilaiPreferensi: parseFloat(item.yi.toFixed(4)),
        ranking: rank + 1,
        details: {
          create: item.details.map((d) => ({
            kriteriaId: d.kriteriaId,
            nilaiAwal: d.nilaiAwal,
            nilaiNormalisasi: parseFloat(d.nilaiNormalisasi.toFixed(4)),
            bobot: d.bobot,
            nilaiTerbobot: parseFloat(d.nilaiTerbobot.toFixed(4)),
          })),
        },
      },
    });
  }

  // 9. Log Aktivitas Awal
  await prisma.logAktivitas.create({
    data: {
      aktivitas: 'Inisialisasi sistem, master data 18 guru, kriteria, dan simulasi periode Mei-Juni 2026',
      modul: 'SISTEM',
    },
  });

  console.log('✓ Seeding selesai: 3 Role, 4 Kriteria, 5 Skala, 18 Guru, 20 Akun User, 2 Periode, dan Penilaian MOORA berhasil disimpan.');
}

main()
  .catch((e) => {
    console.error('Error saat seeding:', e);
    process.exit(1);
  })
  .finally(async () => {
    await prisma.$disconnect();
  });
