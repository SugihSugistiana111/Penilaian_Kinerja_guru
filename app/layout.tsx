import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'SPK Penilaian Kinerja Guru - SMA Al-Ihsan Boarding School',
  description:
    'Sistem Pendukung Keputusan Berbasis Web untuk Penilaian Kinerja Guru Menggunakan Metode MOORA pada SMA Al-Ihsan Boarding School',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="id">
      <body className="antialiased selection:bg-hijau-muda selection:text-teks-utama">
        {children}
      </body>
    </html>
  );
}
