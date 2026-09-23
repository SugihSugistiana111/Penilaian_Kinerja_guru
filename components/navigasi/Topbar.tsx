'use client';

import React from 'react';
import { Menu, Calendar, User } from 'lucide-react';

interface TopbarProps {
  title: string;
  subtitle?: string;
  role: 'ADMIN' | 'KEPALA_SEKOLAH' | 'GURU';
  namaUser: string;
  periodeAktif?: string;
  onOpenMobile?: () => void;
}

export default function Topbar({
  title,
  subtitle,
  role,
  namaUser,
  periodeAktif = 'Juni 2026',
  onOpenMobile,
}: TopbarProps) {
  return (
    <header className="sticky top-0 z-30 bg-white border-b border-hijau-muda px-4 lg:px-8 py-3.5 flex items-center justify-between">
      <div className="flex items-center gap-3">
        <button
          onClick={onOpenMobile}
          className="p-1.5 -ml-2 text-teks-utama hover:bg-hijau-soft rounded-lg lg:hidden"
          aria-label="Buka Menu"
        >
          <Menu className="w-5 h-5" />
        </button>
        <div>
          <h2 className="font-semibold text-lg text-teks-utama leading-tight">
            {title}
          </h2>
          {subtitle && (
            <p className="text-xs text-teks-sekunder mt-0.5">{subtitle}</p>
          )}
        </div>
      </div>

      <div className="flex items-center gap-3 text-xs">
        {/* Periode Aktif */}
        <div className="hidden sm:flex items-center gap-2 px-3 py-1.5 rounded-lg bg-hijau-soft border border-hijau-muda text-teks-utama">
          <Calendar className="w-3.5 h-3.5 text-hijau-utama" />
          <span>Periode: <strong>{periodeAktif}</strong></span>
        </div>

        {/* User Info */}
        <div className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-latar-soft border border-hijau-muda text-teks-utama">
          <User className="w-3.5 h-3.5 text-teks-sekunder" />
          <span className="truncate max-w-[140px] sm:max-w-[200px] font-medium">{namaUser}</span>
        </div>
      </div>
    </header>
  );
}
