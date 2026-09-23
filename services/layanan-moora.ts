import prisma from '@/lib/prisma';

export interface DetailKriteriaMoora {
  kriteriaId: string;
  kodeKriteria: string;
  namaKriteria: string;
  bobot: number;
  jenis: string;
  nilaiAwal: number;
  nilaiNormalisasi: number;
  nilaiTerbobot: number;
}

export interface HasilHitungMooraGuru {
  guruId: string;
  nip: string;
  nama: string;
  jabatan: string;
  details: DetailKriteriaMoora[];
  nilaiPreferensi: number; // Yi
  ranking?: number;
}

export interface HasilLengkapMooraPeriode {
  periodeId: string;
  namaPeriode: string;
  kriteriaList: Array<{
    id: string;
    kode: string;
    nama: string;
    bobot: number;
    jenis: string;
    pembagiNormalisasi: number;
  }>;
  matriksKeputusan: Array<{
    guruId: string;
    nama: string;
    nip: string;
    nilai: Record<string, number>;
  }>;
  matriksNormalisasi: Array<{
    guruId: string;
    nama: string;
    nilai: Record<string, number>;
  }>;
  matriksTerbobot: Array<{
    guruId: string;
    nama: string;
    nilai: Record<string, number>;
  }>;
  hasilAkhir: HasilHitungMooraGuru[];
}

/**
 * Memvalidasi apakah data penilaian suatu periode sudah lengkap untuk seluruh guru aktif
 */
export async function validasiKelengkapanPenilaian(periodeId: string) {
  // 1. Ambil seluruh guru aktif
  const totalGuruAktif = await prisma.guru.count({
    where: { statusAktif: true },
  });

  const daftarGuruAktif = await prisma.guru.findMany({
    where: { statusAktif: true },
    select: { id: true, nama: true, nip: true, jabatanTugasMengajar: true },
  });

  // 2. Ambil kriteria aktif
  const kriteriaAktif = await prisma.kriteria.findMany({
    where: { status: true },
  });

  // 3. Ambil penilaian pada periode tersebut
  const penilaianList = await prisma.penilaian.findMany({
    where: {
      periodeId,
      guru: { statusAktif: true },
    },
    include: {
      details: true,
      guru: true,
    },
  });

  const guruSudahDinilaiIds = new Set(
    penilaianList
      .filter((p: any) => p.details.length === kriteriaAktif.length)
      .map((p: any) => p.guruId)
  );

  const guruBelumDinilai = daftarGuruAktif.filter((g: any) => !guruSudahDinilaiIds.has(g.id));
  const isLengkap = totalGuruAktif > 0 && guruBelumDinilai.length === 0;

  return {
    isLengkap,
    totalGuruAktif,
    totalSudahDinilai: guruSudahDinilaiIds.size,
    totalBelumDinilai: guruBelumDinilai.length,
    guruBelumDinilai,
    // Alias kompatibilitas
    totalGuru: totalGuruAktif,
    dinilaiCount: guruSudahDinilaiIds.size,
    belumDinilaiCount: guruBelumDinilai.length,
    totalSudah: guruSudahDinilaiIds.size,
    totalBelum: guruBelumDinilai.length,
  };
}

/**
 * Menghitung MOORA secara murni (Memory computation)
 */
export async function kalkulasiMooraPeriode(periodeId: string): Promise<HasilLengkapMooraPeriode> {
  const periode = await prisma.periodePenilaian.findUnique({
    where: { id: periodeId },
  });

  if (!periode) {
    throw new Error('Periode penilaian tidak ditemukan');
  }

  // 1. Ambil data guru aktif
  const daftarGuru = await prisma.guru.findMany({
    where: { statusAktif: true },
    orderBy: { nip: 'asc' },
  });

  if (daftarGuru.length === 0) {
    throw new Error('Tidak ada data guru aktif');
  }

  // 2. Ambil seluruh kriteria aktif
  const daftarKriteria = await prisma.kriteria.findMany({
    where: { status: true },
    orderBy: { kode: 'asc' },
  });

  if (daftarKriteria.length === 0) {
    throw new Error('Tidak ada kriteria penilaian aktif');
  }

  // 3. Ambil data penilaian
  const penilaianList = await prisma.penilaian.findMany({
    where: {
      periodeId,
      guru: { statusAktif: true },
    },
    include: {
      details: true,
      guru: true,
    },
  });

  // Susun map penilaian per guru & kriteria
  const skorMap = new Map<string, Map<string, number>>();
  for (const pen of penilaianList) {
    const kriteriaMap = new Map<string, number>();
    for (const d of pen.details) {
      kriteriaMap.set(d.kriteriaId, d.nilai);
    }
    skorMap.set(pen.guruId, kriteriaMap);
  }

  // Tahap 1: Matriks Keputusan X & Hitung Pembagi Normalisasi (akar dari jumlah kuadrat)
  const pembagiNormalisasiMap = new Map<string, number>();

  for (const kriteria of daftarKriteria) {
    let sumKuadrat = 0;
    for (const guru of daftarGuru) {
      const nilai = skorMap.get(guru.id)?.get(kriteria.id) || 0;
      sumKuadrat += nilai * nilai;
    }
    const pembagi = sumKuadrat > 0 ? Math.sqrt(sumKuadrat) : 1;
    pembagiNormalisasiMap.set(kriteria.id, pembagi);
  }

  const kriteriaSummary = daftarKriteria.map((k: any) => ({
    id: k.id,
    kode: k.kode,
    nama: k.nama,
    bobot: k.bobot,
    jenis: k.jenis,
    pembagiNormalisasi: pembagiNormalisasiMap.get(k.id) || 1,
  }));

  const matriksKeputusan = [];
  const matriksNormalisasi = [];
  const matriksTerbobot = [];
  const hasilGuruList: HasilHitungMooraGuru[] = [];

  for (const guru of daftarGuru) {
    const rawScores: Record<string, number> = {};
    const normScores: Record<string, number> = {};
    const weightScores: Record<string, number> = {};
    const details: DetailKriteriaMoora[] = [];

    let sumBenefit = 0;
    let sumCost = 0;

    for (const k of daftarKriteria) {
      const raw = skorMap.get(guru.id)?.get(k.id) || 0;
      const pembagi = pembagiNormalisasiMap.get(k.id) || 1;
      const r_ij = raw / pembagi;
      const v_ij = r_ij * k.bobot;

      rawScores[k.kode] = raw;
      normScores[k.kode] = r_ij;
      weightScores[k.kode] = v_ij;

      if (k.jenis.toUpperCase() === 'BENEFIT') {
        sumBenefit += v_ij;
      } else {
        sumCost += v_ij;
      }

      details.push({
        kriteriaId: k.id,
        kodeKriteria: k.kode,
        namaKriteria: k.nama,
        bobot: k.bobot,
        jenis: k.jenis,
        nilaiAwal: raw,
        nilaiNormalisasi: r_ij,
        nilaiTerbobot: v_ij,
      });
    }

    // Nilai Preferensi / Nilai Optimasi Yi
    const yi = sumBenefit - sumCost;

    matriksKeputusan.push({
      guruId: guru.id,
      nama: guru.nama,
      nip: guru.nip,
      nilai: rawScores,
    });

    matriksNormalisasi.push({
      guruId: guru.id,
      nama: guru.nama,
      nilai: normScores,
    });

    matriksTerbobot.push({
      guruId: guru.id,
      nama: guru.nama,
      nilai: weightScores,
    });

    hasilGuruList.push({
      guruId: guru.id,
      nip: guru.nip,
      nama: guru.nama,
      jabatan: guru.jabatanTugasMengajar,
      details,
      nilaiPreferensi: yi,
    });
  }

  // Tahap 5: Perankingan (Sort descending by Yi)
  hasilGuruList.sort((a: HasilHitungMooraGuru, b: HasilHitungMooraGuru) => b.nilaiPreferensi - a.nilaiPreferensi);

  hasilGuruList.forEach((item: HasilHitungMooraGuru, index: number) => {
    item.ranking = index + 1;
  });

  return {
    periodeId: periode.id,
    namaPeriode: periode.namaPeriode,
    kriteriaList: kriteriaSummary,
    matriksKeputusan,
    matriksNormalisasi,
    matriksTerbobot,
    hasilAkhir: hasilGuruList,
  };
}

/**
 * Menjalankan proses MOORA dan menyimpan hasil permanen ke Database
 */
export async function jalankanDanSimpanMoora(periodeId: string, userId?: string) {
  // 1. Validasi kelengkapan data
  const validasi = await validasiKelengkapanPenilaian(periodeId);
  if (!validasi.isLengkap) {
    throw new Error(
      `Data penilaian belum lengkap. Sebanyak ${validasi.totalBelumDinilai} guru belum dinilai pada periode ini.`
    );
  }

  // 2. Kalkulasi MOORA
  const hasil = await kalkulasiMooraPeriode(periodeId);

  // 3. Simpan ke database dengan transaksi
  await prisma.$transaction(async (tx: any) => {
    // Hapus hasil MOORA lama untuk periode ini jika ada (re-calculate)
    const existingHasil = await tx.hasilMoora.findMany({
      where: { periodeId },
      select: { id: true },
    });

    if (existingHasil.length > 0) {
      await tx.detailMoora.deleteMany({
        where: { hasilMooraId: { in: existingHasil.map((h: any) => h.id) } },
      });
      await tx.hasilMoora.deleteMany({
        where: { periodeId },
      });
    }

    // Insert hasil baru
    for (const item of hasil.hasilAkhir) {
      const createdHasil = await tx.hasilMoora.create({
        data: {
          guruId: item.guruId,
          periodeId: periodeId,
          nilaiPreferensi: parseFloat(item.nilaiPreferensi.toFixed(4)),
          ranking: item.ranking || 0,
        },
      });

      // Insert detail per kriteria
      for (const d of item.details) {
        await tx.detailMoora.create({
          data: {
            hasilMooraId: createdHasil.id,
            kriteriaId: d.kriteriaId,
            nilaiAwal: d.nilaiAwal,
            nilaiNormalisasi: parseFloat(d.nilaiNormalisasi.toFixed(4)),
            bobot: d.bobot,
            nilaiTerbobot: parseFloat(d.nilaiTerbobot.toFixed(4)),
          },
        });
      }
    }

    // Catat log aktivitas
    await tx.logAktivitas.create({
      data: {
        userId: userId || null,
        aktivitas: `Menjalankan kalkulasi MOORA periode ${hasil.namaPeriode}`,
        modul: 'SPK_MOORA',
        dataId: periodeId,
      },
    });
  });

  return hasil;
}

/**
 * Mengambil data hasil MOORA yang tersimpan dari database untuk periode tertentu
 */
export async function getHasilMooraTersimpan(periodeId: string) {
  const hasilList = await prisma.hasilMoora.findMany({
    where: { periodeId },
    include: {
      guru: true,
      periode: true,
      details: {
        include: {
          kriteria: true,
        },
        orderBy: {
          kriteria: { kode: 'asc' },
        },
      },
    },
    orderBy: {
      ranking: 'asc',
    },
  });

  return hasilList;
}
