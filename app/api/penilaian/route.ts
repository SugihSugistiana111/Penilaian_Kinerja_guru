import { NextRequest, NextResponse } from 'next/server';
import { getSession } from '@/lib/auth';
import { simpanPenilaianGuru, getStatusPenilaianPeriode } from '@/services/layanan-penilaian';

export async function GET(request: NextRequest) {
  const session = await getSession();
  if (!session) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }

  const { searchParams } = new URL(request.url);
  const periodeId = searchParams.get('periodeId');

  if (!periodeId) {
    return NextResponse.json({ error: 'Parameter periodeId wajib disertakan' }, { status: 400 });
  }

  const statusData = await getStatusPenilaianPeriode(periodeId);
  return NextResponse.json(statusData);
}

export async function POST(request: NextRequest) {
  const session = await getSession();
  if (!session) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }

  // Hanya Kepala Sekolah dan Admin yang dapat mengisi penilaian
  if (session.role !== 'ADMIN' && session.role !== 'KEPALA_SEKOLAH') {
    return NextResponse.json({ error: 'Akses ditolak' }, { status: 403 });
  }

  try {
    const body = await request.json();
    if (!body.guruId || !body.periodeId || !Array.isArray(body.skor)) {
      return NextResponse.json({ error: 'Data penilaian tidak lengkap' }, { status: 400 });
    }

    const penilaianId = await simpanPenilaianGuru(
      {
        guruId: body.guruId,
        periodeId: body.periodeId,
        dinilaiOleh: session.role === 'KEPALA_SEKOLAH' ? session.nama : (body.dinilaiOleh || 'Administrator'),
        catatan: body.catatan,
        skor: body.skor,
      },
      session.userId
    );

    return NextResponse.json({ success: true, penilaianId });
  } catch (error: any) {
    return NextResponse.json({ error: error.message || 'Gagal menyimpan penilaian' }, { status: 500 });
  }
}
