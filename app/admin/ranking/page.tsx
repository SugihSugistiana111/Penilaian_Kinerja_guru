'use client';

import React, { useState, useEffect } from 'react';
import AppLayout from '@/components/dashboard/AppLayout';
import Link from 'next/link';
import {
  Trophy,
  Search,
  Calendar,
  Printer,
  Calculator,
} from 'lucide-react';
import { getPredikatNilai } from '@/lib/utils';

interface PeriodeItem {
  id: string;
  namaPeriode: string;
  status: string;
}

export default function AdminRankingPage() {
  const [periodeList, setPeriodeList] = useState<PeriodeItem[]>([]);
  const [selectedPeriodeId, setSelectedPeriodeId] = useState<string>('');
  const [rankingList, setRankingList] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');

  useEffect(() => {
    const fetchPeriode = async () => {
      try {
        const res = await fetch('/api/periode');
        const data: PeriodeItem[] = await res.json();
        setPeriodeList(data);
        const aktif = data.find((p) => p.status === 'AKTIF') || data[0];
        if (aktif) setSelectedPeriodeId(aktif.id);
      } catch (e) {
        console.error(e);
      }
    };
    fetchPeriode();
  }, []);

  useEffect(() => {
    const fetchRanking = async () => {
      if (!selectedPeriodeId) return;
      setLoading(true);
      try {
        const res = await fetch(`/api/moora/detail?periodeId=${selectedPeriodeId}`);
        const data = await res.json();
        setRankingList(data.hasilTersimpan || []);
      } catch (e) {
        console.error(e);
      } finally {
        setLoading(false);
      }
    };
    fetchRanking();
  }, [selectedPeriodeId]);

  const filteredRanking = rankingList.filter(
    (r) =>
      r.guru.nama.toLowerCase().includes(search.toLowerCase()) ||
      r.guru.nip.includes(search) ||
      r.guru.jabatanTugasMengajar.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <AppLayout
      title="Hasil Ranking Guru (Metode MOORA)"
      subtitle="Daftar pemeringkatan rekomendasi keputusan kinerja guru SMA Al-Ihsan"
      user={{ nama: 'Administrator SPK', username: 'admin', role: 'ADMIN' }}
    >
      <div className="space-y-6">
        {/* Filter Toolbar */}
        <div className="p-4 bg-white rounded-xl border border-hijau-muda flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-3">
          <div className="flex flex-wrap items-center gap-3">
            <div className="flex items-center gap-2 text-xs font-semibold text-teks-utama">
              <Calendar className="w-4 h-4 text-hijau-utama" />
              <span>Periode:</span>
            </div>
            <select
              value={selectedPeriodeId}
              onChange={(e) => setSelectedPeriodeId(e.target.value)}
              className="px-3 py-1.5 bg-latar-soft border border-hijau-muda rounded-lg text-xs font-medium text-teks-utama focus:ring-2 focus:ring-hijau-utama"
            >
              {periodeList.map((p) => (
                <option key={p.id} value={p.id}>
                  {p.namaPeriode} ({p.status})
                </option>
              ))}
            </select>

            <div className="relative min-w-[200px]">
              <Search className="w-3.5 h-3.5 absolute left-3 top-1/2 -translate-y-1/2 text-teks-sekunder" />
              <input
                type="text"
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                placeholder="Cari guru..."
                className="w-full pl-8 pr-3 py-1.5 bg-latar-soft border border-hijau-muda rounded-lg text-xs text-teks-utama focus:ring-2 focus:ring-hijau-utama"
              />
            </div>
          </div>

          <div className="flex items-center gap-2">
            <Link
              href={`/admin/moora/${selectedPeriodeId}`}
              className="px-3 py-1.5 bg-latar-soft hover:bg-hijau-soft border border-hijau-muda rounded-lg text-xs font-semibold text-teks-utama flex items-center gap-1.5 transition-colors"
            >
              <Calculator className="w-3.5 h-3.5" />
              <span>Detail Matriks MOORA</span>
            </Link>
            <Link
              href="/admin/laporan"
              className="px-3 py-1.5 bg-hijau-utama hover:bg-hijau-hover text-white rounded-lg text-xs font-semibold flex items-center gap-1.5 transition-colors"
            >
              <Printer className="w-3.5 h-3.5" />
              <span>Cetak Laporan</span>
            </Link>
          </div>
        </div>

        {/* Tabel Ranking Standar & Bersih */}
        <div className="bg-white rounded-xl border border-hijau-muda overflow-hidden">
          <div className="p-4 border-b border-hijau-muda flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Trophy className="w-4 h-4 text-hijau-utama" />
              <h3 className="font-semibold text-sm text-teks-utama">
                Tabel Hasil Pemeringkatan MOORA
              </h3>
            </div>
            <span className="text-xs text-teks-sekunder">Total: {filteredRanking.length} Guru</span>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-hijau-soft border-b border-hijau-muda text-teks-utama font-semibold">
                <tr>
                  <th className="py-2.5 px-3 text-center w-14">Ranking</th>
                  <th className="py-2.5 px-3 min-w-[200px]">Nama Guru & NIP</th>
                  <th className="py-2.5 px-3 min-w-[160px]">Mata Pelajaran</th>
                  <th className="py-2.5 px-2 text-center w-14">C1</th>
                  <th className="py-2.5 px-2 text-center w-14">C2</th>
                  <th className="py-2.5 px-2 text-center w-14">C3</th>
                  <th className="py-2.5 px-2 text-center w-14">C4</th>
                  <th className="py-2.5 px-3 text-center min-w-[110px]">Nilai MOORA (Yi)</th>
                  <th className="py-2.5 px-3 text-center">Predikat</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-hijau-muda/50 text-teks-utama">
                {loading ? (
                  <tr>
                    <td colSpan={9} className="text-center py-8 text-teks-sekunder">
                      Memuat data ranking...
                    </td>
                  </tr>
                ) : filteredRanking.length === 0 ? (
                  <tr>
                    <td colSpan={9} className="text-center py-8 text-teks-sekunder">
                      Belum ada data ranking untuk periode ini.
                    </td>
                  </tr>
                ) : (
                  filteredRanking.map((row) => {
                    const avg =
                      row.details.reduce((s: any, d: any) => s + d.nilaiAwal, 0) / (row.details.length || 1);
                    const predikat = getPredikatNilai(avg);

                    return (
                      <tr key={row.id} className="hover:bg-hijau-soft/40 transition-colors">
                        <td className="py-2.5 px-3 text-center font-bold text-teks-utama">
                          {row.ranking}
                        </td>
                        <td className="py-2.5 px-3">
                          <div className="font-semibold text-teks-utama">{row.guru.nama}</div>
                          <div className="text-[10px] font-mono text-teks-sekunder">{row.guru.nip}</div>
                        </td>
                        <td className="py-2.5 px-3 text-teks-sekunder">
                          {row.guru.jabatanTugasMengajar}
                        </td>
                        {row.details.map((d: any) => (
                          <td key={d.id} className="py-2.5 px-2 text-center font-semibold">
                            {d.nilaiAwal}
                          </td>
                        ))}
                        <td className="py-2.5 px-3 text-center font-mono font-bold text-hijau-utama">
                          {row.nilaiPreferensi.toFixed(4)}
                        </td>
                        <td className="py-2.5 px-3 text-center">
                          <span className="text-[11px] font-medium text-teks-utama">
                            {predikat.label}
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
      </div>
    </AppLayout>
  );
}
