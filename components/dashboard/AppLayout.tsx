'use client';

import React, { useState } from 'react';
import Sidebar from '@/components/navigasi/Sidebar';
import Topbar from '@/components/navigasi/Topbar';

interface AppLayoutProps {
  children: React.ReactNode;
  title: string;
  subtitle?: string;
  user: {
    nama: string;
    username: string;
    role: 'ADMIN' | 'KEPALA_SEKOLAH' | 'GURU';
    guruId?: string | null;
  };
  periodeAktif?: string;
}

export default function AppLayout({
  children,
  title,
  subtitle,
  user,
  periodeAktif = 'Juni 2026',
}: AppLayoutProps) {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  return (
    <div className="min-h-screen bg-latar-soft flex">
      {/* Sidebar */}
      <Sidebar
        role={user.role}
        namaUser={user.nama}
        username={user.username}
        isMobileOpen={mobileMenuOpen}
        onCloseMobile={() => setMobileMenuOpen(false)}
      />

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col min-w-0 lg:pl-72">
        <Topbar
          title={title}
          subtitle={subtitle}
          role={user.role}
          namaUser={user.nama}
          periodeAktif={periodeAktif}
          onOpenMobile={() => setMobileMenuOpen(true)}
        />

        <main className="flex-1 p-4 lg:p-8 max-w-7xl w-full mx-auto space-y-6">
          {children}
        </main>
      </div>
    </div>
  );
}
