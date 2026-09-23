import { NextRequest, NextResponse } from 'next/server';
import { getSession } from '@/lib/auth';
import prisma from '@/lib/prisma';

export async function GET() {
  const session = await getSession();
  if (!session) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }

  const skala = await prisma.skalaPenilaian.findMany({
    orderBy: [{ nilai: 'asc' }],
    include: { kriteria: true },
  });

  return NextResponse.json(skala);
}

export async function PUT(request: NextRequest) {
  const session = await getSession();
  if (!session || session.role !== 'ADMIN') {
    return NextResponse.json({ error: 'Hanya Admin yang dapat mengelola skala' }, { status: 403 });
  }

  try {
    const { id, label, keterangan } = await request.json();
    const updated = await prisma.skalaPenilaian.update({
      where: { id },
      data: {
        ...(label && { label }),
        ...(keterangan !== undefined && { keterangan }),
      },
    });

    return NextResponse.json({ success: true, data: updated });
  } catch (error: any) {
    return NextResponse.json({ error: error.message || 'Gagal mengubah skala' }, { status: 500 });
  }
}
