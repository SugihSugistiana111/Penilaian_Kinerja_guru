import prisma from '@/lib/prisma';

export async function getLaporanPeriode(periodeId: string) {
  const periode = await prisma.periodePenilaian.findUnique({
    where: { id: periodeId },
    include: {
      hasilMoora: {
        include: {
          guru: true,
          details: {
            include: { kriteria: true },
            orderBy: { kriteria: { kode: 'asc' } },
          },
        },
        orderBy: { ranking: 'asc' },
      },
    },
  });

  if (!periode) {
    throw new Error('Periode tidak ditemukan');
  }

  const kriteriaList = await prisma.kriteria.findMany({
    where: { status: true },
    orderBy: { kode: 'asc' },
  });

  return {
    identitasSekolah: {
      namaSekolah: 'SMA AL-IHSAN BOARDING SCHOOL',
      npsn: '20271890',
      alamat: 'Jl. Pesantren Al-Ihsan, Kec. Selaawi, Kab. Garut, Jawa Barat',
      telepon: '(0262) 2801234',
      email: 'info@sma-alihsan.sch.id',
      website: 'www.sma-alihsan.sch.id',
      kepalaSekolah: 'Dr. H. Mulyadi, M.Pd.',
      nipKepalaSekolah: '197508122000031002',
      administrator: 'M. Hidad Abdillah, S.Pd.',
    },
    periode,
    kriteriaList,
    dataRanking: periode.hasilMoora,
  };
}
