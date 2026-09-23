import prisma from '@/lib/prisma';

export interface InputSkorKriteria {
  kriteriaId: string;
  nilai: number;
}

export interface InputPenilaianGuru {
  guruId: string;
  periodeId: string;
  dinilaiOleh?: string;
  catatan?: string;
  skor: InputSkorKriteria[];
}

/**
 * Menyimpan atau memperbarui penilaian kinerja guru
 */
export async function simpanPenilaianGuru(data: InputPenilaianGuru, userId?: string) {
  // 1. Cek apakah penilaian sudah ada
  const existing = await prisma.penilaian.findUnique({
    where: {
      guruId_periodeId: {
        guruId: data.guruId,
        periodeId: data.periodeId,
      },
    },
  });

  return await prisma.$transaction(async (tx: any) => {
    let penilaianId: string;

    if (existing) {
      // Update
      const updated = await tx.penilaian.update({
        where: { id: existing.id },
        data: {
          dinilaiOleh: data.dinilaiOleh || 'Kepala Sekolah',
          catatan: data.catatan,
          status: 'SELESAI',
        },
      });
      penilaianId = updated.id;

      // Hapus detail lama dan insert baru
      await tx.detailPenilaian.deleteMany({
        where: { penilaianId },
      });
    } else {
      // Create baru
      const created = await tx.penilaian.create({
        data: {
          guruId: data.guruId,
          periodeId: data.periodeId,
          dinilaiOleh: data.dinilaiOleh || 'Kepala Sekolah',
          catatan: data.catatan,
          status: 'SELESAI',
        },
      });
      penilaianId = created.id;
    }

    // Insert detail nilai kriteria
    for (const item of data.skor) {
      await tx.detailPenilaian.create({
        data: {
          penilaianId,
          kriteriaId: item.kriteriaId,
          nilai: Number(item.nilai),
        },
      });
    }

    // Log aktivitas
    await tx.logAktivitas.create({
      data: {
        userId: userId || null,
        aktivitas: `Menyimpan penilaian kinerja guru (ID: ${data.guruId})`,
        modul: 'PENILAIAN',
        dataId: penilaianId,
      },
    });

    return penilaianId;
  });
}

/**
 * Mengambil daftar status penilaian guru pada satu periode
 */
export async function getStatusPenilaianPeriode(periodeId: string) {
  const daftarGuru = await prisma.guru.findMany({
    where: { statusAktif: true },
    orderBy: { nama: 'asc' },
  });

  const kriteriaList = await prisma.kriteria.findMany({
    where: { status: true },
    orderBy: { kode: 'asc' },
  });

  const penilaianList = await prisma.penilaian.findMany({
    where: { periodeId },
    include: {
      details: {
        include: { kriteria: true },
      },
    },
  });

  const penilaianMap = new Map(penilaianList.map((p: any) => [p.guruId, p]));

  const rekap = daftarGuru.map((guru: any) => {
    const pen: any = penilaianMap.get(guru.id);
    const sudahDinilai = Boolean(pen && pen.details.length === kriteriaList.length);

    const nilaiPerKriteria: Record<string, number> = {};
    if (pen) {
      pen.details.forEach((d: any) => {
        nilaiPerKriteria[d.kriteria.kode] = d.nilai;
      });
    }

    return {
      guruId: guru.id,
      nip: guru.nip,
      nama: guru.nama,
      jabatan: guru.jabatanTugasMengajar,
      jamAjar: guru.jumlahJamAjar,
      sudahDinilai,
      penilaianId: pen?.id,
      catatan: pen?.catatan,
      nilaiPerKriteria,
    };
  });

  const totalGuru = daftarGuru.length;
  const totalSudah = rekap.filter((r: any) => r.sudahDinilai).length;
  const totalBelum = totalGuru - totalSudah;
  const isLengkap = totalGuru > 0 && totalBelum === 0;

  return {
    periodeId,
    kriteriaList,
    rekap,
    totalGuru,
    totalSudah,
    totalBelum,
    isLengkap,
  };
}
