import React from 'react';
import { getSession } from '@/lib/auth';
import { redirect } from 'next/navigation';
import prisma from '@/lib/prisma';
import AppLayout from '@/components/dashboard/AppLayout';
import KartuStatistik from '@/components/dashboard/KartuStatistik';
import { getPeriodeAktif } from '@/services/layanan-periode';
import { validasiKelengkapanPenilaian, getHasilMooraTersimpan } from '@/services/layanan-moora';
import {
  Users,
  CheckCircle,
  Clock,
  Calendar,
  ArrowRight,
  ClipboardCheck,
  Trophy,
} from 'lucide-react';
import Link from 'next/link';

export default async function KepsekDashboardPage() {
  const session = await getSession();
  if (!session || session.role !== 'KEPALA_SEKOLAH') {
    redirect('/login');
  }

  const totalGuru = await prisma.guru.count({ where: { statusAktif: true } });
  const periodeAktif = await getPeriodeAktif();

  let validasi: any = { isLengkap: false, totalGuru: 0, dinilaiCount: 0, belumDinilaiCount: 0 };
  let hasilRanking: any[] = [];

  if (periodeAktif) {
    validasi = await validasiKelengkapanPenilaian(periodeAktif.id);
    hasilRanking = await getHasilMooraTersimpan(periodeAktif.id);
  }

  const totalGuruAktif = validasi?.totalGuru ?? validasi?.totalGuruAktif ?? totalGuru ?? 0;
  const totalSudah = validasi?.dinilaiCount ?? validasi?.totalSudahDinilai ?? 0;
  const totalBelum = validasi?.belumDinilaiCount ?? validasi?.totalBelumDinilai ?? 0;

  const persentase =
    totalGuruAktif > 0
      ? Math.round((totalSudah / totalGuruAktif) * 100)
      : 0;

  return (
    <AppLayout
      title="Dashboard Kepala Sekolah"
      subtitle="Ringkasan evaluasi kinerja guru dan rekomendasi keputusan metode MOORA"
      user={session}
      periodeAktif={periodeAktif?.namaPeriode || 'Tidak Ada Periode Aktif'}
    >
      <div className="space-y-6">
        {/* 4 Kartu Statistik */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <KartuStatistik
            title="Guru Aktif"
            value={`${totalGuruAktif} Guru`}
            subtext="Tenaga pendidik terdaftar"
            icon={Users}
          />
          <KartuStatistik
            title="Sudah Dinilai"
            value={`${totalSudah} Guru`}
            subtext={`Periode ${periodeAktif?.namaPeriode || '-'}`}
            icon={CheckCircle}
          />
          <KartuStatistik
            title="Belum Dinilai"
            value={`${totalBelum} Guru`}
            subtext={totalBelum === 0 ? 'Semua guru telah dinilai' : 'Menunggu input'}
            icon={Clock}
          />
          <KartuStatistik
            title="Periode Aktif"
            value={periodeAktif?.namaPeriode || '-'}
            subtext={`Tahun ${periodeAktif?.tahun || '-'}`}
            icon={Calendar}
          />
        </div>

        {/* Status Penilaian Sekolah */}
        <div className="bg-white p-6 rounded-xl border border-hijau-muda space-y-4">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
            <div>
              <h3 className="font-semibold text-sm text-teks-utama">
                Status Penilaian Guru Periode {periodeAktif?.namaPeriode || 'Aktif'}
              </h3>
              <p className="text-xs text-teks-sekunder mt-0.5">
                {totalSudah} dari {totalGuruAktif} guru telah dinilai ({persentase}%)
              </p>
            </div>

            <Link
              href="/kepala-sekolah/penilaian"
              className="px-3.5 py-1.5 bg-hijau-utama hover:bg-hijau-hover text-white rounded-lg text-xs font-semibold flex items-center gap-1.5 transition-colors self-start sm:self-auto"
            >
              <ClipboardCheck className="w-3.5 h-3.5" />
              <span>Input Penilaian Guru</span>
            </Link>
          </div>

          <div className="w-full h-2.5 bg-hijau-soft rounded-full overflow-hidden">
            <div
              className="h-full bg-hijau-utama rounded-full transition-all duration-300"
              style={{ width: `${persentase}%` }}
            />
          </div>
        </div>

        {/* Tabel Hasil Ranking Terbaru */}
        <div className="bg-white rounded-xl border border-hijau-muda overflow-hidden">
          <div className="p-4 border-b border-hijau-muda flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Trophy className="w-4 h-4 text-hijau-utama" />
              <h3 className="font-semibold text-sm text-teks-utama">
                Hasil Ranking Rekomendasi Kinerja (MOORA)
              </h3>
            </div>
            <Link
              href="/kepala-sekolah/ranking"
              className="text-xs font-semibold text-hijau-utama hover:underline flex items-center gap-1"
            >
              <span>Lihat Semua Ranking</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </Link>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-hijau-soft border-b border-hijau-muda text-teks-utama font-semibold">
                <tr>
                  <th className="py-2.5 px-3 text-center w-12">No</th>
                  <th className="py-2.5 px-3">Nama Guru & NIP</th>
                  <th className="py-2.5 px-3">Mata Pelajaran</th>
                  <th className="py-2.5 px-3 text-center">Nilai MOORA</th>
                  <th className="py-2.5 px-3 text-center">Peringkat</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-hijau-muda/50 text-teks-utama">
                {hasilRanking.length === 0 ? (
                  <tr>
                    <td colSpan={5} className="py-6 text-center text-teks-sekunder">
                      Belum ada hasil ranking pada periode ini.
                    </td>
                  </tr>
                ) : (
                  hasilRanking.slice(0, 5).map((row: any) => (
                    <tr key={row.id} className="hover:bg-hijau-soft/40 transition-colors">
                      <td className="py-2.5 px-3 text-center font-medium">{row.ranking}</td>
                      <td className="py-2.5 px-3">
                        <div className="font-semibold text-teks-utama">{row.guru.nama}</div>
                        <div className="text-[10px] text-teks-sekunder font-mono">{row.guru.nip}</div>
                      </td>
                      <td className="py-2.5 px-3 text-teks-sekunder">{row.guru.jabatanTugasMengajar}</td>
                      <td className="py-2.5 px-3 text-center font-mono font-semibold text-hijau-utama">
                        {row.nilaiPreferensi.toFixed(4)}
                      </td>
                      <td className="py-2.5 px-3 text-center">
                        <span className="inline-block px-2 py-0.5 rounded bg-hijau-soft text-teks-utama font-bold text-[11px]">
                          #{row.ranking}
                        </span>
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </AppLayout>
  );
}
