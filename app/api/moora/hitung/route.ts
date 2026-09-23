import { NextRequest, NextResponse } from 'next/server';
import { getSession } from '@/lib/auth';
import { jalankanDanSimpanMoora, validasiKelengkapanPenilaian } from '@/services/layanan-moora';

export async function POST(request: NextRequest) {
  const session = await getSession();
  if (!session || session.role !== 'ADMIN') {
    return NextResponse.json(
      { error: 'Hanya Administrator yang berwenang menjalankan proses MOORA' },
      { status: 403 }
    );
  }

  try {
    const { periodeId } = await request.json();
    if (!periodeId) {
      return NextResponse.json({ error: 'Parameter periodeId wajib disertakan' }, { status: 400 });
    }

    // Periksa kelengkapan terlebih dahulu
    const validasi = await validasiKelengkapanPenilaian(periodeId);
    if (!validasi.isLengkap) {
      return NextResponse.json(
        {
          error: `Data penilaian belum lengkap. ${validasi.totalBelumDinilai} guru belum dinilai pada periode ini.`,
          detail: validasi,
        },
        { status: 400 }
      );
    }

    const hasil = await jalankanDanSimpanMoora(periodeId, session.userId);
    return NextResponse.json({
      success: true,
      message: 'Perhitungan MOORA berhasil dieksekusi dan disimpan sebagai riwayat.',
      data: hasil,
    });
  } catch (error: any) {
    return NextResponse.json({ error: error.message || 'Gagal menjalankan MOORA' }, { status: 500 });
  }
}
