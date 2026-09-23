import React from 'react';
import { getSession } from '@/lib/auth';
import { redirect } from 'next/navigation';
import prisma from '@/lib/prisma';
import AppLayout from '@/components/dashboard/AppLayout';
import KartuStatistik from '@/components/dashboard/KartuStatistik';
import { getPeriodeAktif } from '@/services/layanan-periode';
import {
  Award,
  Trophy,
  CheckCircle,
  Star,
  ArrowRight,
  User,
} from 'lucide-react';
import Link from 'next/link';
import { getPredikatNilai } from '@/lib/utils';

export default async function GuruDashboardPage() {
  const session = await getSession();
  if (!session || session.role !== 'GURU' || !session.guruId) {
    redirect('/login');
  }

  const guru = await prisma.guru.findUnique({
    where: { id: session.guruId },
  });

  if (!guru) redirect('/login');

  const periodeAktif = await getPeriodeAktif();

  const penilaianTerbaru = await prisma.penilaian.findFirst({
    where: { guruId: guru.id, ...(periodeAktif ? { periodeId: periodeAktif.id } : {}) },
    include: {
      periode: true,
      details: {
        include: { kriteria: true },
        orderBy: { kriteria: { kode: 'asc' } },
      },
    },
    orderBy: { createdAt: 'desc' },
  });

  const mooraTerbaru = await prisma.hasilMoora.findFirst({
    where: { guruId: guru.id, ...(periodeAktif ? { periodeId: periodeAktif.id } : {}) },
    include: {
      periode: true,
    },
    orderBy: { createdAt: 'desc' },
  });

  const skorList = penilaianTerbaru?.details || [];
  const rataRata =
    skorList.length > 0
      ? skorList.reduce((sum, d) => sum + d.nilai, 0) / skorList.length
      : 0;
  const predikat = getPredikatNilai(rataRata);

  return (
    <AppLayout
      title="Dashboard Guru"
      subtitle={`Informasi penilaian kinerja mandiri: ${guru.nama}`}
      user={session}
      periodeAktif={periodeAktif?.namaPeriode || 'Periode Tidak Aktif'}
    >
      <div className="space-y-6">
        {/* 4 Kartu Statistik */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <KartuStatistik
            title="Nilai MOORA (Yi)"
            value={mooraTerbaru ? mooraTerbaru.nilaiPreferensi.toFixed(4) : '-'}
            subtext={mooraTerbaru ? `Periode ${mooraTerbaru.periode.namaPeriode}` : 'Belum dihitung'}
            icon={Award}
          />
          <KartuStatistik
            title="Peringkat Sekolah"
            value={mooraTerbaru ? `#${mooraTerbaru.ranking}` : '-'}
            subtext="Hasil pemeringkatan"
            icon={Trophy}
          />
          <KartuStatistik
            title="Rata-rata Skor"
            value={rataRata > 0 ? rataRata.toFixed(2) : '-'}
            subtext={`Predikat: ${predikat.label}`}
            icon={Star}
          />
          <KartuStatistik
            title="Status Penilaian"
            value={penilaianTerbaru ? 'Sudah Dinilai' : 'Belum Dinilai'}
            subtext={penilaianTerbaru ? `Penilai: ${penilaianTerbaru.dinilaiOleh || 'Kepala Sekolah'}` : 'Menunggu periode'}
            icon={CheckCircle}
          />
        </div>

        {/* Tabel 4 Kriteria & Catatan Penilai */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Tabel Kriteria */}
          <div className="lg:col-span-2 bg-white rounded-xl border border-hijau-muda overflow-hidden">
            <div className="p-4 border-b border-hijau-muda flex items-center justify-between">
              <h3 className="font-semibold text-sm text-teks-utama">
                Capaian 4 Kriteria Penilaian ({penilaianTerbaru?.periode?.namaPeriode || periodeAktif?.namaPeriode})
              </h3>
              <Link
                href="/guru/hasil"
                className="text-xs font-semibold text-hijau-utama hover:underline flex items-center gap-1"
              >
                <span>Rincian Lengkap</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </Link>
            </div>

            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs">
                <thead className="bg-hijau-soft border-b border-hijau-muda text-teks-utama font-semibold">
                  <tr>
                    <th className="py-2.5 px-3 text-center w-14">Kode</th>
                    <th className="py-2.5 px-3">Kriteria Penilaian</th>
                    <th className="py-2.5 px-3 text-center">Bobot</th>
                    <th className="py-2.5 px-3 text-center">Skor (1-5)</th>
                    <th className="py-2.5 px-3 text-center">Predikat</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-hijau-muda/50 text-teks-utama">
                  {skorList.length === 0 ? (
                    <tr>
                      <td colSpan={5} className="py-6 text-center text-teks-sekunder">
                        Belum ada penilaian pada periode ini.
                      </td>
                    </tr>
                  ) : (
                    skorList.map((item) => {
                      const itemPredikat = getPredikatNilai(item.nilai);
                      return (
                        <tr key={item.id} className="hover:bg-hijau-soft/40 transition-colors">
                          <td className="py-2.5 px-3 text-center font-bold text-hijau-utama">
                            {item.kriteria.kode}
                          </td>
                          <td className="py-2.5 px-3 font-semibold">{item.kriteria.nama}</td>
                          <td className="py-2.5 px-3 text-center text-teks-sekunder">
                            {(item.kriteria.bobot * 100).toFixed(0)}%
                          </td>
                          <td className="py-2.5 px-3 text-center font-bold">{item.nilai}</td>
                          <td className="py-2.5 px-3 text-center">
                            <span className="text-[11px] font-medium text-teks-utama">
                              {itemPredikat.label}
                            </span>
                          </td>
                        </tr>
                      );
                    })
                  )}
                </tbody>
              </table>
            </div>
          </div>

          {/* Catatan Evaluator & Data Guru */}
          <div className="bg-white p-4 rounded-xl border border-hijau-muda space-y-4">
            <div>
              <h3 className="font-semibold text-sm text-teks-utama">Catatan Kepala Sekolah</h3>
              <div className="mt-2 p-3 rounded-lg bg-latar-soft border border-hijau-muda/60 text-xs text-teks-utama">
                {penilaianTerbaru?.catatan ? (
                  <p className="italic leading-relaxed">"{penilaianTerbaru.catatan}"</p>
                ) : (
                  <p className="text-teks-sekunder">Belum ada catatan evaluasi.</p>
                )}
              </div>
            </div>

            <div className="pt-2 border-t border-hijau-muda/50 space-y-2 text-xs">
              <h4 className="font-semibold text-teks-utama">Data Mengajar</h4>
              <p className="text-teks-sekunder">
                <span className="font-medium text-teks-utama">Mapel:</span> {guru.jabatanTugasMengajar}
              </p>
              <p className="text-teks-sekunder">
                <span className="font-medium text-teks-utama">Beban Jam:</span> {guru.jumlahJamAjar} Jam/Minggu
              </p>
              <p className="text-teks-sekunder">
                <span className="font-medium text-teks-utama">Rombel:</span> {guru.jumlahSiswaPerRombel} Siswa
              </p>
              <Link
                href="/guru/profil"
                className="inline-block pt-1 text-xs font-semibold text-hijau-utama hover:underline"
              >
                Lihat Profil Lengkap →
              </Link>
            </div>
          </div>
        </div>
      </div>
    </AppLayout>
  );
}
