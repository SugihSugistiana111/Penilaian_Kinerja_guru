import prisma from '@/lib/prisma';

export async function getDaftarPeriode() {
  return await prisma.periodePenilaian.findMany({
    orderBy: [{ tahun: 'desc' }, { createdAt: 'desc' }],
    include: {
      _count: {
        select: {
          penilaian: true,
          hasilMoora: true,
        },
      },
    },
  });
}

export async function getPeriodeAktif() {
  return await prisma.periodePenilaian.findFirst({
    where: { status: 'AKTIF' },
  });
}

export async function getPeriodeById(id: string) {
  return await prisma.periodePenilaian.findUnique({
    where: { id },
    include: {
      penilaian: {
        include: {
          guru: true,
          details: {
            include: { kriteria: true },
          },
        },
      },
      hasilMoora: {
        include: {
          guru: true,
          details: {
            include: { kriteria: true },
          },
        },
        orderBy: { ranking: 'asc' },
      },
    },
  });
}

export async function buatPeriodeBaru(data: { bulan: string; tahun: number; setAktif?: boolean }) {
  const namaPeriode = `${data.bulan} ${data.tahun}`;

  // Cek apakah periode dengan nama yang sama sudah ada
  const existing = await prisma.periodePenilaian.findFirst({
    where: { bulan: data.bulan, tahun: data.tahun },
  });

  if (existing) {
    throw new Error(`Periode penilaian ${namaPeriode} sudah ada.`);
  }

  // Jika setAktif true, nonaktifkan periode aktif lainnya
  if (data.setAktif) {
    await prisma.periodePenilaian.updateMany({
      where: { status: 'AKTIF' },
      data: { status: 'DRAFT' },
    });
  }

  return await prisma.periodePenilaian.create({
    data: {
      bulan: data.bulan,
      tahun: data.tahun,
      namaPeriode,
      status: data.setAktif ? 'AKTIF' : 'DRAFT',
    },
  });
}

export async function updateStatusPeriode(id: string, status: 'DRAFT' | 'AKTIF' | 'SELESAI') {
  if (status === 'AKTIF') {
    // Pastikan hanya 1 periode yang aktif
    await prisma.periodePenilaian.updateMany({
      where: { status: 'AKTIF' },
      data: { status: 'DRAFT' },
    });
  }

  return await prisma.periodePenilaian.update({
    where: { id },
    data: { status },
  });
}
