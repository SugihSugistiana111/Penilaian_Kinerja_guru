import { NextRequest, NextResponse } from 'next/server';
import prisma from '@/lib/prisma';
import { comparePassword, createSessionToken, COOKIE_NAME } from '@/lib/auth';

export async function POST(request: NextRequest) {
  try {
    const { username, password } = await request.json();

    if (!username || !password) {
      return NextResponse.json(
        { error: 'Username dan password wajib diisi' },
        { status: 400 }
      );
    }

    // Cari user berdasarkan username
    const user = await prisma.user.findUnique({
      where: { username },
      include: {
        role: true,
        guru: true,
      },
    });

    if (!user || !user.status) {
      return NextResponse.json(
        { error: 'Username atau password salah / Akun nonaktif' },
        { status: 401 }
      );
    }

    // Verifikasi password
    const isPasswordValid = await comparePassword(password, user.password);
    if (!isPasswordValid) {
      return NextResponse.json(
        { error: 'Username atau password salah' },
        { status: 401 }
      );
    }

    // Buat JWT token
    const token = await createSessionToken({
      userId: user.id,
      nama: user.nama,
      username: user.username,
      role: user.role.namaRole as 'ADMIN' | 'KEPALA_SEKOLAH' | 'GURU',
      guruId: user.guruId,
    });

    // Catat log aktivitas
    await prisma.logAktivitas.create({
      data: {
        userId: user.id,
        aktivitas: `User ${user.username} (${user.role.namaRole}) berhasil login`,
        modul: 'AUTENTIKASI',
      },
    });

    const response = NextResponse.json({
      success: true,
      user: {
        id: user.id,
        nama: user.nama,
        username: user.username,
        role: user.role.namaRole,
        guruId: user.guruId,
      },
    });

    // Set cookie
    response.cookies.set({
      name: COOKIE_NAME,
      value: token,
      httpOnly: true,
      secure: process.env.NODE_ENV === 'production',
      sameSite: 'lax',
      path: '/',
      maxAge: 60 * 60 * 24 * 7, // 7 hari
    });

    return response;
  } catch (error: any) {
    console.error('Login error:', error);
    return NextResponse.json(
      { error: 'Terjadi kesalahan pada server saat autentikasi' },
      { status: 500 }
    );
  }
}
