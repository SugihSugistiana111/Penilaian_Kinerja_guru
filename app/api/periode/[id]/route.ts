import { NextRequest, NextResponse } from 'next/server';
import { getSession } from '@/lib/auth';
import { getPeriodeById, updateStatusPeriode } from '@/services/layanan-periode';

export async function GET(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  const session = await getSession();
  if (!session) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }

  const periode = await getPeriodeById(params.id);
  if (!periode) {
    return NextResponse.json({ error: 'Periode tidak ditemukan' }, { status: 404 });
  }

  return NextResponse.json(periode);
}

export async function PATCH(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  const session = await getSession();
  if (!session || session.role !== 'ADMIN') {
    return NextResponse.json({ error: 'Hanya Admin yang dapat mengubah status periode' }, { status: 403 });
  }

  try {
    const { status } = await request.json();
    if (!['DRAFT', 'AKTIF', 'SELESAI'].includes(status)) {
      return NextResponse.json({ error: 'Status tidak valid' }, { status: 400 });
    }

    const updated = await updateStatusPeriode(params.id, status);
    return NextResponse.json({ success: true, data: updated });
  } catch (error: any) {
    return NextResponse.json({ error: error.message || 'Gagal mengubah status periode' }, { status: 500 });
  }
}
