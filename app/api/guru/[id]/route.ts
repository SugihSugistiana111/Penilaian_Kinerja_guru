import { NextRequest, NextResponse } from 'next/server';
import { getSession } from '@/lib/auth';
import { getGuruById, updateGuru, toggleStatusGuru } from '@/services/layanan-guru';

export async function GET(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  const session = await getSession();
  if (!session) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }

  // Jika guru, pastikan hanya bisa melihat data dirinya sendiri
  if (session.role === 'GURU' && session.guruId !== params.id) {
    return NextResponse.json({ error: 'Akses ditolak' }, { status: 403 });
  }

  const guru = await getGuruById(params.id);
  if (!guru) {
    return NextResponse.json({ error: 'Guru tidak ditemukan' }, { status: 404 });
  }

  return NextResponse.json(guru);
}

export async function PUT(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  const session = await getSession();
  if (!session || session.role !== 'ADMIN') {
    return NextResponse.json({ error: 'Hanya Admin yang dapat mengubah data guru' }, { status: 403 });
  }

  try {
    const body = await request.json();
    const guru = await updateGuru(params.id, body);
    return NextResponse.json({ success: true, data: guru });
  } catch (error: any) {
    return NextResponse.json({ error: error.message || 'Gagal mengubah data guru' }, { status: 500 });
  }
}

export async function PATCH(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  const session = await getSession();
  if (!session || session.role !== 'ADMIN') {
    return NextResponse.json({ error: 'Hanya Admin yang dapat mengubah status guru' }, { status: 403 });
  }

  try {
    const { statusAktif } = await request.json();
    const guru = await toggleStatusGuru(params.id, Boolean(statusAktif));
    return NextResponse.json({ success: true, data: guru });
  } catch (error: any) {
    return NextResponse.json({ error: error.message || 'Gagal mengubah status guru' }, { status: 500 });
  }
}
