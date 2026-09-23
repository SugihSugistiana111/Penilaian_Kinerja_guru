import { NextRequest, NextResponse } from 'next/server';
import { getSession } from '@/lib/auth';
import { kalkulasiMooraPeriode, getHasilMooraTersimpan, validasiKelengkapanPenilaian } from '@/services/layanan-moora';

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

  try {
    const validasi = await validasiKelengkapanPenilaian(periodeId);
    let detailKalkulasi = null;

    if (validasi.totalSudahDinilai > 0) {
      try {
        detailKalkulasi = await kalkulasiMooraPeriode(periodeId);
      } catch (e: any) {
        console.error('Kalkulasi error:', e);
      }
    }

    const hasilTersimpan = await getHasilMooraTersimpan(periodeId);

    return NextResponse.json({
      validasi,
      detailKalkulasi,
      hasilTersimpan,
    });
  } catch (error: any) {
    return NextResponse.json({ error: error.message || 'Gagal mengambil detail MOORA' }, { status: 500 });
  }
}
