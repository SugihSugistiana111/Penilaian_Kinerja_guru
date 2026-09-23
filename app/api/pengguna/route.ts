import { NextRequest, NextResponse } from 'next/server';
import { getSession, hashPassword } from '@/lib/auth';
import prisma from '@/lib/prisma';

export async function GET() {
  const session = await getSession();
  if (!session || session.role !== 'ADMIN') {
    return NextResponse.json({ error: 'Akses ditolak' }, { status: 403 });
  }

  const users = await prisma.user.findMany({
    orderBy: { createdAt: 'asc' },
    select: {
      id: true,
      nama: true,
      username: true,
      roleId: true,
      role: true,
      guruId: true,
      guru: {
        select: {
          id: true,
          nama: true,
          nip: true,
          jabatanTugasMengajar: true,
        },
      },
      status: true,
      createdAt: true,
    },
  });

  return NextResponse.json(users);
}

export async function POST(request: NextRequest) {
  const session = await getSession();
  if (!session || session.role !== 'ADMIN') {
    return NextResponse.json({ error: 'Akses ditolak' }, { status: 403 });
  }

  try {
    const { nama, username, password, roleId, guruId } = await request.json();

    if (!nama || !username || !password || !roleId) {
      return NextResponse.json({ error: 'Nama, username, password, dan role wajib diisi' }, { status: 400 });
    }

    const existing = await prisma.user.findUnique({ where: { username } });
    if (existing) {
      return NextResponse.json({ error: 'Username sudah digunakan' }, { status: 400 });
    }

    const hashedPassword = await hashPassword(password);

    const user = await prisma.user.create({
      data: {
        nama,
        username,
        password: hashedPassword,
        roleId,
        guruId: guruId || null,
        status: true,
      },
    });

    return NextResponse.json({ success: true, userId: user.id }, { status: 201 });
  } catch (error: any) {
    return NextResponse.json({ error: error.message || 'Gagal membuat pengguna' }, { status: 500 });
  }
}

export async function PUT(request: NextRequest) {
  const session = await getSession();
  if (!session || session.role !== 'ADMIN') {
    return NextResponse.json({ error: 'Akses ditolak' }, { status: 403 });
  }

  try {
    const { id, nama, password, status, roleId, guruId } = await request.json();

    const dataToUpdate: any = {};
    if (nama) dataToUpdate.nama = nama;
    if (roleId) dataToUpdate.roleId = roleId;
    if (guruId !== undefined) dataToUpdate.guruId = guruId || null;
    if (status !== undefined) dataToUpdate.status = Boolean(status);
    if (password) {
      dataToUpdate.password = await hashPassword(password);
    }

    const updated = await prisma.user.update({
      where: { id },
      data: dataToUpdate,
    });

    return NextResponse.json({ success: true, data: updated });
  } catch (error: any) {
    return NextResponse.json({ error: error.message || 'Gagal memperbarui pengguna' }, { status: 500 });
  }
}
