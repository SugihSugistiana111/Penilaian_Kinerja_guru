import prisma from '@/lib/prisma';

export interface DataGuruInput {
  nip: string;
  nama: string;
  jenisKelamin: string;
  jabatanTugasMengajar: string;
  tugasTambahanUtama?: string | null;
  tugasTambahanLain?: string | null;
  jumlahSiswaPerRombel: number;
  jumlahJamAjar: number;
  mengajarKelas10: boolean;
  mengajarKelas11: boolean;
  mengajarKelas12: boolean;
  statusAktif?: boolean;
}

/**
 * Mengambil daftar seluruh guru dengan opsi pencarian dan filter
 */
export async function getDaftarGuru(options?: {
  search?: string;
  statusAktif?: boolean;
  kelas?: 10 | 11 | 12;
}) {
  const where: any = {};

  if (options?.statusAktif !== undefined) {
    where.statusAktif = options.statusAktif;
  }

  if (options?.search) {
    where.OR = [
      { nama: { contains: options.search } },
      { nip: { contains: options.search } },
      { jabatanTugasMengajar: { contains: options.search } },
    ];
  }

  if (options?.kelas === 10) where.mengajarKelas10 = true;
  if (options?.kelas === 11) where.mengajarKelas11 = true;
  if (options?.kelas === 12) where.mengajarKelas12 = true;

  return await prisma.guru.findMany({
    where,
    orderBy: { nama: 'asc' },
    include: {
      user: {
        select: {
          id: true,
          username: true,
        },
      },
    },
  });
}

/**
 * Mengambil detail guru berdasarkan ID
 */
export async function getGuruById(id: string) {
  return await prisma.guru.findUnique({
    where: { id },
    include: {
      user: true,
      penilaian: {
        include: {
          periode: true,
          details: {
            include: { kriteria: true },
          },
        },
        orderBy: { createdAt: 'desc' },
      },
      hasilMoora: {
        include: {
          periode: true,
          details: {
            include: { kriteria: true },
          },
        },
        orderBy: { createdAt: 'desc' },
      },
    },
  });
}

/**
 * Menambahkan data guru baru
 */
export async function tambahGuru(data: DataGuruInput) {
  return await prisma.guru.create({
    data: {
      nip: data.nip,
      nama: data.nama,
      jenisKelamin: data.jenisKelamin,
      jabatanTugasMengajar: data.jabatanTugasMengajar,
      tugasTambahanUtama: data.tugasTambahanUtama || null,
      tugasTambahanLain: data.tugasTambahanLain || null,
      jumlahSiswaPerRombel: Number(data.jumlahSiswaPerRombel) || 0,
      jumlahJamAjar: Number(data.jumlahJamAjar) || 0,
      mengajarKelas10: Boolean(data.mengajarKelas10),
      mengajarKelas11: Boolean(data.mengajarKelas11),
      mengajarKelas12: Boolean(data.mengajarKelas12),
      statusAktif: data.statusAktif ?? true,
    },
  });
}

/**
 * Memperbarui data guru
 */
export async function updateGuru(id: string, data: Partial<DataGuruInput>) {
  return await prisma.guru.update({
    where: { id },
    data: {
      ...(data.nip !== undefined && { nip: data.nip }),
      ...(data.nama !== undefined && { nama: data.nama }),
      ...(data.jenisKelamin !== undefined && { jenisKelamin: data.jenisKelamin }),
      ...(data.jabatanTugasMengajar !== undefined && { jabatanTugasMengajar: data.jabatanTugasMengajar }),
      ...(data.tugasTambahanUtama !== undefined && { tugasTambahanUtama: data.tugasTambahanUtama }),
      ...(data.tugasTambahanLain !== undefined && { tugasTambahanLain: data.tugasTambahanLain }),
      ...(data.jumlahSiswaPerRombel !== undefined && { jumlahSiswaPerRombel: Number(data.jumlahSiswaPerRombel) }),
      ...(data.jumlahJamAjar !== undefined && { jumlahJamAjar: Number(data.jumlahJamAjar) }),
      ...(data.mengajarKelas10 !== undefined && { mengajarKelas10: Boolean(data.mengajarKelas10) }),
      ...(data.mengajarKelas11 !== undefined && { mengajarKelas11: Boolean(data.mengajarKelas11) }),
      ...(data.mengajarKelas12 !== undefined && { mengajarKelas12: Boolean(data.mengajarKelas12) }),
      ...(data.statusAktif !== undefined && { statusAktif: Boolean(data.statusAktif) }),
    },
  });
}

/**
 * Menonaktifkan status aktif guru (Soft delete sesuai aturan RB-02/Bagian 28)
 */
export async function toggleStatusGuru(id: string, statusAktif: boolean) {
  return await prisma.guru.update({
    where: { id },
    data: { statusAktif },
  });
}
