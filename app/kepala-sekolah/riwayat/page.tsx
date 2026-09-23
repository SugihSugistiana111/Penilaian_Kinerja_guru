'use client';

import React, { useState, useEffect } from 'react';
import AppLayout from '@/components/dashboard/AppLayout';
import { History, Search } from 'lucide-react';
import { getPredikatNilai } from '@/lib/utils';

export default function KepsekRiwayatPage() {
  const [riwayat, setRiwayat] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [filterTahun, setFilterTahun] = useState('all');

  useEffect(() => {
    const fetchRiwayat = async () => {
      setLoading(true);
      try {
        const res = await fetch('/api/periode');
        const periodes = await res.json();
        
        const allHasil: any[] = [];
        for (const p of periodes) {
          const detailRes = await fetch(`/api/moora/detail?periodeId=${p.id}`);
          const detailData = await detailRes.json();
          if (detailData.hasilTersimpan?.length > 0) {
            allHasil.push(...detailData.hasilTersimpan);
          }
        }

        setRiwayat(allHasil);
      } catch (e) {
        console.error(e);
      } finally {
        setLoading(false);
      }
    };
    fetchRiwayat();
  }, []);

  const filtered = riwayat.filter((item) => {
    if (filterTahun !== 'all' && item.periode?.tahun.toString() !== filterTahun) return false;
    if (
      search &&
      !item.guru.nama.toLowerCase().includes(search.toLowerCase()) &&
      !item.guru.nip.includes(search) &&
      !item.periode.namaPeriode.toLowerCase().includes(search.toLowerCase())
    ) {
      return false;
    }
    return true;
  });

  return (
    <AppLayout
      title="Riwayat Evaluasi Kinerja Guru"
      subtitle="Arsip histori penilaian dan pemeringkatan MOORA multi-periode"
      user={{ nama: 'Dr. H. Mulyadi, M.Pd.', username: 'kepsek', role: 'KEPALA_SEKOLAH' }}
    >
      <div className="space-y-6">
        {/* Search & Filter */}
        <div className="p-4 bg-white rounded-xl border border-hijau-muda flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-3">
          <div className="flex flex-wrap items-center gap-2">
            <div className="relative min-w-[220px]">
              <Search className="w-3.5 h-3.5 absolute left-3 top-1/2 -translate-y-1/2 text-teks-sekunder" />
              <input
                type="text"
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                placeholder="Cari guru atau periode..."
                className="w-full pl-8 pr-3 py-1.5 bg-latar-soft border border-hijau-muda rounded-lg text-xs text-teks-utama focus:ring-2 focus:ring-hijau-utama"
              />
            </div>

            <select
              value={filterTahun}
              onChange={(e) => setFilterTahun(e.target.value)}
              className="px-3 py-1.5 bg-latar-soft border border-hijau-muda rounded-lg text-xs font-medium text-teks-utama focus:ring-2 focus:ring-hijau-utama"
            >
              <option value="all">Semua Tahun</option>
              <option value="2026">Tahun 2026</option>
              <option value="2025">Tahun 2025</option>
            </select>
          </div>

          <span className="text-xs text-teks-sekunder">
            Total Arsip: {filtered.length} Data
          </span>
        </div>

        {/* Tabel Riwayat */}
        <div className="bg-white rounded-xl border border-hijau-muda overflow-hidden">
          <div className="p-4 border-b border-hijau-muda flex items-center justify-between">
            <div className="flex items-center gap-2">
              <History className="w-4 h-4 text-hijau-utama" />
              <h3 className="font-semibold text-sm text-teks-utama">Histori Evaluasi Guru</h3>
            </div>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-hijau-soft border-b border-hijau-muda text-teks-utama font-semibold">
                <tr>
                  <th className="py-2.5 px-3">Periode</th>
                  <th className="py-2.5 px-3">Nama Guru & NIP</th>
                  <th className="py-2.5 px-2 text-center w-12">C1</th>
                  <th className="py-2.5 px-2 text-center w-12">C2</th>
                  <th className="py-2.5 px-2 text-center w-12">C3</th>
                  <th className="py-2.5 px-2 text-center w-12">C4</th>
                  <th className="py-2.5 px-3 text-center">Nilai MOORA</th>
                  <th className="py-2.5 px-3 text-center">Peringkat</th>
                  <th className="py-2.5 px-3 text-center">Predikat</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-hijau-muda/50 text-teks-utama">
                {loading ? (
                  <tr>
                    <td colSpan={9} className="py-8 text-center text-teks-sekunder">
                      Memuat riwayat penilaian...
                    </td>
                  </tr>
                ) : filtered.length === 0 ? (
                  <tr>
                    <td colSpan={9} className="py-8 text-center text-teks-sekunder">
                      Tidak ada riwayat penilaian yang cocok.
                    </td>
                  </tr>
                ) : (
                  filtered.map((row) => {
                    const avg =
                      row.details.reduce((s: any, d: any) => s + d.nilaiAwal, 0) / (row.details.length || 1);
                    const predikat = getPredikatNilai(avg);

                    return (
                      <tr key={row.id} className="hover:bg-hijau-soft/40 transition-colors">
                        <td className="py-2.5 px-3 font-semibold text-teks-utama">
                          {row.periode?.namaPeriode}
                        </td>
                        <td className="py-2.5 px-3">
                          <div className="font-semibold">{row.guru.nama}</div>
                          <div className="text-[10px] font-mono text-teks-sekunder">{row.guru.nip}</div>
                        </td>
                        {row.details.map((d: any) => (
                          <td key={d.id} className="py-2.5 px-2 text-center font-semibold">
                            {d.nilaiAwal}
                          </td>
                        ))}
                        <td className="py-2.5 px-3 text-center font-mono font-bold text-hijau-utama">
                          {row.nilaiPreferensi.toFixed(4)}
                        </td>
                        <td className="py-2.5 px-3 text-center font-bold">
                          #{row.ranking}
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
