import prisma from '@/lib/prisma';

/**
 * Mengambil riwayat perkembangan kriteria dan MOORA untuk satu guru spesifik (Multi-periode)
 */
export async function getPerkembanganKinerjaGuru(guruId: string) {
  const guru = await prisma.guru.findUnique({
    where: { id: guruId },
  });

  if (!guru) {
    throw new Error('Guru tidak ditemukan');
  }

  // Ambil seluruh penilaian guru yang diurutkan berdasarkan periode
  const riwayatPenilaian = await prisma.penilaian.findMany({
    where: { guruId },
    include: {
      periode: true,
      details: {
        include: { kriteria: true },
      },
    },
    orderBy: {
      periode: { createdAt: 'asc' },
    },
  });

  // Ambil hasil MOORA guru untuk setiap periode
  const riwayatMoora = await prisma.hasilMoora.findMany({
    where: { guruId },
    include: {
      periode: true,
      details: {
        include: { kriteria: true },
      },
    },
    orderBy: {
      periode: { createdAt: 'asc' },
    },
  });

  const mooraMap = new Map(riwayatMoora.map((m) => [m.periodeId, m]));

  // Susun data grafik per periode
  const dataGrafik = riwayatPenilaian.map((pen) => {
    const moora = mooraMap.get(pen.periodeId);
    const entry: Record<string, any> = {
      periode: pen.periode.namaPeriode,
      bulan: pen.periode.bulan,
      tahun: pen.periode.tahun,
      nilaiMoora: moora ? moora.nilaiPreferensi : null,
      ranking: moora ? moora.ranking : null,
    };

    pen.details.forEach((d) => {
      entry[d.kriteria.kode] = d.nilai;
      entry[`${d.kriteria.kode}_nama`] = d.kriteria.nama;
    });

    return entry;
  });

  return {
    guru,
    riwayatPenilaian,
    riwayatMoora,
    dataGrafik,
  };
}

/**
 * Mengambil riwayat penilaian seluruh guru dengan opsi filter tahun, bulan, guru
 */
export async function getRiwayatPenilaianSemua(options?: {
  tahun?: number;
  bulan?: string;
  guruId?: string;
}) {
  const whereMoora: any = {};

  if (options?.guruId) whereMoora.guruId = options.guruId;

  if (options?.tahun || options?.bulan) {
    whereMoora.periode = {};
    if (options.tahun) whereMoora.periode.tahun = options.tahun;
    if (options.bulan) whereMoora.periode.bulan = options.bulan;
  }

  const hasilList = await prisma.hasilMoora.findMany({
    where: whereMoora,
    include: {
      guru: true,
      periode: true,
      details: {
        include: { kriteria: true },
        orderBy: { kriteria: { kode: 'asc' } },
      },
    },
    orderBy: [
      { periode: { tahun: 'desc' } },
      { periode: { createdAt: 'desc' } },
      { ranking: 'asc' },
    ],
  });

  return hasilList;
}
