import { NextRequest, NextResponse } from 'next/server';
import { getSession } from '@/lib/auth';
import prisma from '@/lib/prisma';

export async function GET() {
  const session = await getSession();
  if (!session) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }

  const kriteria = await prisma.kriteria.findMany({
    orderBy: { kode: 'asc' },
    include: {
      skala: {
        orderBy: { nilai: 'asc' },
      },
    },
  });

  return NextResponse.json(kriteria);
}

export async function PUT(request: NextRequest) {
  const session = await getSession();
  if (!session || session.role !== 'ADMIN') {
    return NextResponse.json({ error: 'Hanya Admin yang dapat mengubah bobot kriteria' }, { status: 403 });
  }

  try {
    const { kriteriaList } = await request.json(); // Array of { id, bobot, nama }

    if (!Array.isArray(kriteriaList)) {
      return NextResponse.json({ error: 'Format data tidak valid' }, { status: 400 });
    }

    // Validasi total bobot = 1.0 (atau 100%)
    const totalBobot = kriteriaList.reduce((sum, item) => sum + Number(item.bobot), 0);
    if (Math.abs(totalBobot - 1.0) > 0.001 && Math.abs(totalBobot - 100) > 0.1) {
      return NextResponse.json(
        { error: `Total bobot kriteria harus 100% atau 1.00 (Total saat ini: ${totalBobot})` },
        { status: 400 }
      );
    }

    // Update setiap kriteria
    await prisma.$transaction(
      kriteriaList.map((item) =>
        prisma.kriteria.update({
          where: { id: item.id },
          data: {
            bobot: item.bobot > 1 ? item.bobot / 100 : item.bobot,
            ...(item.nama && { nama: item.nama }),
          },
        })
      )
    );

    return NextResponse.json({ success: true, message: 'Bobot kriteria berhasil diperbarui' });
  } catch (error: any) {
    return NextResponse.json({ error: error.message || 'Gagal mengubah bobot' }, { status: 500 });
  }
}
