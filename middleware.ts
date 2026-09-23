import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';
import { jwtVerify } from 'jose';

const SECRET_KEY = new TextEncoder().encode(
  process.env.AUTH_SECRET || 'spk-kinerja-guru-alihsan-rahasia-super-aman-2026'
);

const COOKIE_NAME = 'spk_auth_token';

export async function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;

  // Lewati file statis, aset logo, favicon, dan API auth
  if (
    pathname.startsWith('/_next') ||
    pathname.startsWith('/api/auth') ||
    pathname.startsWith('/favicon.ico') ||
    pathname.startsWith('/logo') ||
    pathname.includes('.')
  ) {
    return NextResponse.next();
  }

  const token = request.cookies.get(COOKIE_NAME)?.value;
  let userSession: { role: string; userId: string; username: string } | null = null;

  if (token) {
    try {
      const { payload } = await jwtVerify(token, SECRET_KEY);
      userSession = payload as any;
    } catch (e) {
      userSession = null;
    }
  }

  // Jika di root (/) atau /login
  if (pathname === '/' || pathname === '/login') {
    if (userSession) {
      if (userSession.role === 'ADMIN') {
        return NextResponse.redirect(new URL('/admin/dashboard', request.url));
      } else if (userSession.role === 'KEPALA_SEKOLAH') {
        return NextResponse.redirect(new URL('/kepala-sekolah/dashboard', request.url));
      } else if (userSession.role === 'GURU') {
        return NextResponse.redirect(new URL('/guru/dashboard', request.url));
      }
    }
    if (pathname === '/') {
      return NextResponse.redirect(new URL('/login', request.url));
    }
    return NextResponse.next();
  }

  // Proteksi rute Admin
  if (pathname.startsWith('/admin')) {
    if (!userSession) {
      return NextResponse.redirect(new URL('/login?callbackUrl=' + encodeURIComponent(pathname), request.url));
    }
    if (userSession.role !== 'ADMIN') {
      return NextResponse.redirect(new URL('/login?error=unauthorized', request.url));
    }
  }

  // Proteksi rute Kepala Sekolah
  if (pathname.startsWith('/kepala-sekolah')) {
    if (!userSession) {
      return NextResponse.redirect(new URL('/login?callbackUrl=' + encodeURIComponent(pathname), request.url));
    }
    if (userSession.role !== 'KEPALA_SEKOLAH') {
      return NextResponse.redirect(new URL('/login?error=unauthorized', request.url));
    }
  }

  // Proteksi rute Guru
  if (pathname.startsWith('/guru')) {
    if (!userSession) {
      return NextResponse.redirect(new URL('/login?callbackUrl=' + encodeURIComponent(pathname), request.url));
    }
    if (userSession.role !== 'GURU') {
      return NextResponse.redirect(new URL('/login?error=unauthorized', request.url));
    }
  }

  return NextResponse.next();
}

export const config = {
  matcher: ['/((?!_next/static|_next/image|favicon.ico).*)'],
};
