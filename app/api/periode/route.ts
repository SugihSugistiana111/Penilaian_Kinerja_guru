import { NextRequest, NextResponse } from 'next/server';
import { getSession } from '@/lib/auth';
import { getDaftarPeriode, getPeriodeAktif, buatPeriodeBaru } from '@/services/layanan-periode';

export async function GET(request: NextRequest) {
  const session = await getSession();
  if (!session) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }

  const { searchParams } = new URL(request.url);
  const hanyaAktif = searchParams.get('aktif') === 'true';

  if (hanyaAktif) {
    const aktif = await getPeriodeAktif();
    return NextResponse.json(aktif);
  }

  const list = await getDaftarPeriode();
  return NextResponse.json(list);
}

export async function POST(request: NextRequest) {
  const session = await getSession();
  if (!session || session.role !== 'ADMIN') {
    return NextResponse.json({ error: 'Hanya Admin yang dapat membuat periode' }, { status: 403 });
  }

  try {
    const body = await request.json();
    if (!body.bulan || !body.tahun) {
      return NextResponse.json({ error: 'Bulan dan tahun wajib diisi' }, { status: 400 });
    }

    const periode = await buatPeriodeBaru({
      bulan: body.bulan,
      tahun: Number(body.tahun),
      setAktif: Boolean(body.setAktif),
    });

    return NextResponse.json({ success: true, data: periode }, { status: 201 });
  } catch (error: any) {
    return NextResponse.json({ error: error.message || 'Gagal membuat periode' }, { status: 500 });
  }
}
