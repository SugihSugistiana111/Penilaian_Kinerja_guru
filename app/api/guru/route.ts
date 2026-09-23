import { NextRequest, NextResponse } from 'next/server';
import { getSession } from '@/lib/auth';
import { getDaftarGuru, tambahGuru } from '@/services/layanan-guru';

export async function GET(request: NextRequest) {
  const session = await getSession();
  if (!session) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }

  const { searchParams } = new URL(request.url);
  const search = searchParams.get('search') || undefined;
  const statusParam = searchParams.get('statusAktif');
  const statusAktif = statusParam !== null ? statusParam === 'true' : undefined;

  const data = await getDaftarGuru({ search, statusAktif });
  return NextResponse.json(data);
}

export async function POST(request: NextRequest) {
  const session = await getSession();
  if (!session || session.role !== 'ADMIN') {
    return NextResponse.json({ error: 'Hanya Admin yang dapat menambah data guru' }, { status: 403 });
  }

  try {
    const body = await request.json();
    if (!body.nama || !body.nip || !body.jenisKelamin || !body.jabatanTugasMengajar) {
      return NextResponse.json(
        { error: 'NIP, Nama, Jenis Kelamin, dan Jabatan wajib diisi' },
        { status: 400 }
      );
    }

    const guru = await tambahGuru(body);
    return NextResponse.json({ success: true, data: guru }, { status: 201 });
  } catch (error: any) {
    return NextResponse.json({ error: error.message || 'Gagal menyimpan data guru' }, { status: 500 });
  }
}
