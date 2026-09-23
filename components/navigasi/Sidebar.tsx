'use client';

import React from 'react';
import Link from 'next/link';
import { usePathname, useRouter } from 'next/navigation';
import {
  LayoutDashboard,
  Users,
  GraduationCap,
  Scale,
  Sliders,
  Calendar,
  ClipboardCheck,
  Calculator,
  Trophy,
  LineChart,
  History,
  Printer,
  UserCog,
  LogOut,
  X,
  Layers,
} from 'lucide-react';

interface SidebarProps {
  role: 'ADMIN' | 'KEPALA_SEKOLAH' | 'GURU';
  namaUser: string;
  username: string;
  isMobileOpen: boolean;
  onCloseMobile: () => void;
}

export default function Sidebar({
  role,
  namaUser,
  username,
  isMobileOpen,
  onCloseMobile,
}: SidebarProps) {
  const pathname = usePathname();
  const router = useRouter();

  const handleLogout = async () => {
    try {
      await fetch('/api/auth/logout', { method: 'POST' });
      router.push('/login');
      router.refresh();
    } catch (e) {
      console.error(e);
    }
  };

  const adminNav = [
    {
      group: 'UTAMA',
      items: [
        { label: 'Dashboard', href: '/admin/dashboard', icon: LayoutDashboard },
      ],
    },
    {
      group: 'DATA MASTER',
      items: [
        { label: 'Data Guru', href: '/admin/guru', icon: GraduationCap },
        { label: 'Kriteria & Bobot', href: '/admin/kriteria', icon: Scale },
        { label: 'Skala Penilaian', href: '/admin/skala-penilaian', icon: Sliders },
        { label: 'Periode Penilaian', href: '/admin/periode', icon: Calendar },
      ],
    },
    {
      group: 'PENILAIAN & SPK',
      items: [
        { label: 'Penilaian Kinerja', href: '/admin/penilaian', icon: ClipboardCheck },
        { label: 'Proses SPK MOORA', href: '/admin/moora', icon: Calculator },
        { label: 'Hasil Ranking', href: '/admin/ranking', icon: Trophy },
      ],
    },
    {
      group: 'MONITORING & LAPORAN',
      items: [
        { label: 'Monitoring Kinerja', href: '/admin/monitoring', icon: LineChart },
        { label: 'Laporan Cetak', href: '/admin/laporan', icon: Printer },
        { label: 'Manajemen Pengguna', href: '/admin/pengguna', icon: UserCog },
      ],
    },
  ];

  const kepsekNav = [
    {
      group: 'UTAMA',
      items: [
        { label: 'Dashboard', href: '/kepala-sekolah/dashboard', icon: LayoutDashboard },
      ],
    },
    {
      group: 'PENILAIAN & EVALUASI',
      items: [
        { label: 'Data Guru', href: '/kepala-sekolah/guru', icon: GraduationCap },
        { label: 'Penilaian Kinerja', href: '/kepala-sekolah/penilaian', icon: ClipboardCheck },
      ],
    },
    {
      group: 'HASIL & KEPUTUSAN',
      items: [
        { label: 'Hasil Ranking MOORA', href: '/kepala-sekolah/ranking', icon: Trophy },
        { label: 'Monitoring Kinerja', href: '/kepala-sekolah/monitoring', icon: LineChart },
        { label: 'Riwayat Penilaian', href: '/kepala-sekolah/riwayat', icon: History },
        { label: 'Cetak Laporan', href: '/kepala-sekolah/laporan', icon: Printer },
      ],
    },
  ];

  const guruNav = [
    {
      group: 'MENU GURU',
      items: [
        { label: 'Dashboard Saya', href: '/guru/dashboard', icon: LayoutDashboard },
        { label: 'Hasil Penilaian', href: '/guru/hasil', icon: Trophy },
        { label: 'Grafik Perkembangan', href: '/guru/monitoring', icon: LineChart },
        { label: 'Riwayat Penilaian', href: '/guru/riwayat', icon: History },
        { label: 'Profil Mengajar', href: '/guru/profil', icon: Users },
      ],
    },
  ];

  const navGroups =
    role === 'ADMIN' ? adminNav : role === 'KEPALA_SEKOLAH' ? kepsekNav : guruNav;

  const roleLabel =
    role === 'ADMIN'
      ? 'Administrator'
      : role === 'KEPALA_SEKOLAH'
      ? 'Kepala Sekolah'
      : 'Guru Pengajar';

  return (
    <>
      {/* Mobile Backdrop */}
      {isMobileOpen && (
        <div
          className="fixed inset-0 bg-black/40 z-40 lg:hidden"
          onClick={onCloseMobile}
        />
      )}

      {/* Sidebar Container */}
      <aside
        className={`fixed top-0 bottom-0 left-0 z-50 w-72 bg-white border-r border-hijau-muda flex flex-col transition-transform duration-200 ease-in-out lg:translate-x-0 ${
          isMobileOpen ? 'translate-x-0' : '-translate-x-full'
        }`}
      >
        {/* Brand Header dengan Logo Asli */}
        <div className="p-4 border-b border-hijau-muda bg-hijau-soft flex items-center justify-between">
          <div className="flex items-center gap-3">
            <img
              src="/logo/logo-alihsan.jpg"
              alt="Logo SMA Al-Ihsan"
              className="w-10 h-10 object-contain shrink-0 rounded-lg"
            />
            <div>
              <h1 className="font-bold text-xs text-teks-utama uppercase tracking-wider leading-tight">
                SPK KINERJA GURU
              </h1>
              <p className="text-[11px] text-teks-sekunder font-medium">
                SMA Al-Ihsan Boarding School
              </p>
            </div>
          </div>
          <button
            onClick={onCloseMobile}
            className="p-1 text-teks-sekunder hover:text-teks-utama lg:hidden"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* User Card Tag */}
        <div className="px-4 py-3 bg-latar-soft border-b border-hijau-muda flex items-center gap-3">
          <div className="w-8 h-8 rounded-full bg-hijau-muda flex items-center justify-center text-teks-utama font-bold text-xs">
            {namaUser.charAt(0).toUpperCase()}
          </div>
          <div className="flex-1 min-w-0">
            <p className="text-xs font-semibold text-teks-utama truncate">{namaUser}</p>
            <p className="text-[11px] text-teks-sekunder">{roleLabel}</p>
          </div>
        </div>

        {/* Navigation Items */}
        <div className="flex-1 overflow-y-auto py-3 px-3 space-y-5">
          {navGroups.map((group, idx) => (
            <div key={idx} className="space-y-1">
              <p className="px-3 text-[10px] font-bold text-teks-sekunder tracking-wider uppercase">
                {group.group}
              </p>
              <div className="space-y-0.5">
                {group.items.map((item) => {
                  const Icon = item.icon;
                  const isActive =
                    pathname === item.href ||
                    (item.href !== '/admin/dashboard' &&
                      item.href !== '/kepala-sekolah/dashboard' &&
                      item.href !== '/guru/dashboard' &&
                      pathname.startsWith(item.href));

                  return (
                    <Link
                      key={item.href}
                      href={item.href}
                      onClick={onCloseMobile}
                      className={`flex items-center gap-3 px-3 py-2 rounded-lg text-xs font-medium transition-colors ${
                        isActive
                          ? 'bg-hijau-muda text-teks-utama font-bold border border-hijau-utama/30'
                          : 'text-teks-sekunder hover:bg-hijau-soft hover:text-teks-utama'
                      }`}
                    >
                      <Icon className="w-4 h-4 shrink-0 text-hijau-utama" />
                      <span>{item.label}</span>
                    </Link>
                  );
                })}
              </div>
            </div>
          ))}
        </div>

        {/* Logout Footer */}
        <div className="p-3 border-t border-hijau-muda">
          <button
            onClick={handleLogout}
            className="w-full flex items-center gap-3 px-3 py-2 rounded-lg text-xs font-medium text-red-600 hover:bg-red-50 transition-colors"
          >
            <LogOut className="w-4 h-4 shrink-0 text-red-500" />
            <span>Keluar dari Akun</span>
          </button>
        </div>
      </aside>
    </>
  );
}
