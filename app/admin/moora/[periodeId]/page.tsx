'use client';

import React, { useState, useEffect } from 'react';
import AppLayout from '@/components/dashboard/AppLayout';
import Link from 'next/link';
import {
  ArrowLeft,
  Calculator,
  Trophy,
  Table as TableIcon,
  Printer,
} from 'lucide-react';

interface MooraDetailResponse {
  validasi: any;
  detailKalkulasi: {
    periodeId: string;
    namaPeriode: string;
    kriteriaList: Array<{
      id: string;
      kode: string;
      nama: string;
      bobot: number;
      jenis: string;
      pembagiNormalisasi: number;
    }>;
    matriksKeputusan: Array<{
      guruId: string;
      nama: string;
      nip: string;
      nilai: Record<string, number>;
    }>;
    matriksNormalisasi: Array<{
      guruId: string;
      nama: string;
      nilai: Record<string, number>;
    }>;
    matriksTerbobot: Array<{
      guruId: string;
      nama: string;
      nilai: Record<string, number>;
    }>;
    hasilAkhir: Array<{
      guruId: string;
      nip: string;
      nama: string;
      jabatan: string;
      nilaiPreferensi: number;
      ranking: number;
      details: Array<{
        kodeKriteria: string;
        nilaiAwal: number;
        nilaiNormalisasi: number;
        bobot: number;
        nilaiTerbobot: number;
      }>;
    }>;
  } | null;
  hasilTersimpan: any[];
}

export default function MooraDetailPage({ params }: { params: { periodeId: string } }) {
  const [data, setData] = useState<MooraDetailResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<'A' | 'B' | 'C' | 'D' | 'E' | 'F'>('B');

  useEffect(() => {
    const fetchData = async () => {
      try {
        const res = await fetch(`/api/moora/detail?periodeId=${params.periodeId}`);
        const json = await res.json();
        setData(json);
      } catch (e) {
        console.error(e);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, [params.periodeId]);

  if (loading) {
    return (
      <AppLayout
        title="Detail Perhitungan MOORA"
        subtitle="Memuat data matriks komputasi SPK..."
        user={{ nama: 'Administrator SPK', username: 'admin', role: 'ADMIN' }}
      >
        <div className="p-12 text-center text-xs text-teks-sekunder bg-white rounded-xl border border-hijau-muda">
          Memuat tahapan perhitungan matematis MOORA...
        </div>
      </AppLayout>
    );
  }

  const kalkulasi = data?.detailKalkulasi;

  if (!kalkulasi) {
    return (
      <AppLayout
        title="Detail Perhitungan MOORA"
        subtitle="Data perhitungan tidak ditemukan"
        user={{ nama: 'Administrator SPK', username: 'admin', role: 'ADMIN' }}
      >
        <div className="p-8 text-center space-y-4 bg-white rounded-xl border border-hijau-muda">
          <p className="text-xs text-teks-sekunder">
            Data penilaian belum lengkap atau belum diproses untuk periode ini.
          </p>
          <Link
            href="/admin/moora"
            className="inline-flex items-center gap-1.5 px-4 py-2 bg-hijau-utama text-white text-xs font-semibold rounded-lg"
          >
            <ArrowLeft className="w-4 h-4" />
            <span>Kembali ke Halaman MOORA</span>
          </Link>
        </div>
      </AppLayout>
    );
  }

  return (
    <AppLayout
      title={`Detail Perhitungan MOORA: ${kalkulasi.namaPeriode}`}
      subtitle="Transparansi matematis tahapan metode MOORA untuk keperluan validasi"
      user={{ nama: 'Administrator SPK', username: 'admin', role: 'ADMIN' }}
    >
      <div className="space-y-6">
        {/* Navigation Bar */}
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 p-4 bg-white rounded-xl border border-hijau-muda">
          <Link
            href="/admin/moora"
            className="flex items-center gap-1.5 text-xs font-semibold text-teks-sekunder hover:text-teks-utama"
          >
            <ArrowLeft className="w-4 h-4" />
            <span>Kembali ke Panel MOORA</span>
          </Link>

          <div className="flex items-center gap-2">
            <Link
              href="/admin/ranking"
              className="px-3 py-1.5 bg-latar-soft hover:bg-hijau-soft border border-hijau-muda rounded-lg text-xs font-semibold text-teks-utama flex items-center gap-1.5 transition-colors"
            >
              <Trophy className="w-3.5 h-3.5 text-hijau-utama" />
              <span>Lihat Ranking</span>
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

        {/* Tab Navigasi Akademis (A s/d F) */}
        <div className="flex flex-wrap gap-1.5 bg-white p-1.5 rounded-xl border border-hijau-muda">
          {[
            { key: 'A', label: 'A. Kriteria & Pembagi' },
            { key: 'B', label: 'B. Matriks Keputusan (X)' },
            { key: 'C', label: 'C. Normalisasi (rij)' },
            { key: 'D', label: 'D. Terbobot (vij)' },
            { key: 'E', label: 'E. Optimasi (Yi)' },
            { key: 'F', label: 'F. Hasil Ranking' },
          ].map((tab) => (
            <button
              key={tab.key}
              onClick={() => setActiveTab(tab.key as any)}
              className={`px-3 py-2 rounded-lg text-xs font-medium transition-colors ${
                activeTab === tab.key
                  ? 'bg-hijau-utama text-white font-semibold'
                  : 'text-teks-sekunder hover:bg-hijau-soft hover:text-teks-utama'
              }`}
            >
              {tab.label}
            </button>
          ))}
        </div>

        {/* Tab A: Kriteria & Pembagi Normalisasi */}
        {activeTab === 'A' && (
          <div className="bg-white rounded-xl border border-hijau-muda overflow-hidden space-y-4 p-4">
            <h3 className="font-semibold text-sm text-teks-utama">
              A. Kriteria Penilaian, Bobot, dan Pembagi Normalisasi (√∑x²)
            </h3>
            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs">
                <thead className="bg-hijau-soft border-b border-hijau-muda text-teks-utama font-semibold">
                  <tr>
                    <th className="py-2.5 px-3">Kode</th>
                    <th className="py-2.5 px-3">Nama Kriteria</th>
                    <th className="py-2.5 px-3 text-center">Jenis</th>
                    <th className="py-2.5 px-3 text-center">Bobot (wj)</th>
                    <th className="py-2.5 px-3 text-center">Pembagi Normalisasi (√∑x²)</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-hijau-muda/50 text-teks-utama">
                  {kalkulasi.kriteriaList.map((k) => (
                    <tr key={k.id} className="hover:bg-hijau-soft/40">
                      <td className="py-2.5 px-3 font-bold text-hijau-utama">{k.kode}</td>
                      <td className="py-2.5 px-3 font-semibold">{k.nama}</td>
                      <td className="py-2.5 px-3 text-center font-medium">{k.jenis}</td>
                      <td className="py-2.5 px-3 text-center font-mono font-semibold">
                        {(k.bobot * 100).toFixed(0)}% ({k.bobot.toFixed(2)})
                      </td>
                      <td className="py-2.5 px-3 text-center font-mono text-hijau-utama font-semibold">
                        {k.pembagiNormalisasi.toFixed(4)}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {/* Tab B: Matriks Keputusan (X) */}
        {activeTab === 'B' && (
          <div className="bg-white rounded-xl border border-hijau-muda overflow-hidden space-y-4 p-4">
            <div>
              <h3 className="font-semibold text-sm text-teks-utama">
                B. Matriks Keputusan (X)
              </h3>
              <p className="text-xs text-teks-sekunder mt-0.5">
                Nilai mentah skala 1-5 hasil penilaian untuk setiap guru pada 4 kriteria
              </p>
            </div>

            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs">
                <thead className="bg-hijau-soft border-b border-hijau-muda text-teks-utama font-semibold">
                  <tr>
                    <th className="py-2.5 px-3 text-center w-12">No</th>
                    <th className="py-2.5 px-3 min-w-[200px]">Nama Guru & NIP</th>
                    {kalkulasi.kriteriaList.map((k) => (
                      <th key={k.kode} className="py-2.5 px-3 text-center">
                        {k.kode} ({k.nama})
                      </th>
                    ))}
                  </tr>
                </thead>
                <tbody className="divide-y divide-hijau-muda/50 text-teks-utama">
                  {kalkulasi.matriksKeputusan.map((row, idx) => (
                    <tr key={row.guruId} className="hover:bg-hijau-soft/40">
                      <td className="py-2 px-3 text-center font-medium">{idx + 1}</td>
                      <td className="py-2 px-3">
                        <div className="font-semibold">{row.nama}</div>
                        <div className="text-[10px] font-mono text-teks-sekunder">{row.nip}</div>
                      </td>
                      {kalkulasi.kriteriaList.map((k) => (
                        <td key={k.kode} className="py-2 px-3 text-center font-bold">
                          {row.nilai[k.kode] ?? '-'}
                        </td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {/* Tab C: Matriks Normalisasi (rij) */}
        {activeTab === 'C' && (
          <div className="bg-white rounded-xl border border-hijau-muda overflow-hidden space-y-4 p-4">
            <div>
              <h3 className="font-semibold text-sm text-teks-utama">
                C. Matriks Normalisasi (rij = xij / √∑xkj²)
              </h3>
              <p className="text-xs text-teks-sekunder mt-0.5">
                Setiap nilai elemen matriks keputusan dibagi dengan akar jumlah kuadrat kriteria
              </p>
            </div>

            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs">
                <thead className="bg-hijau-soft border-b border-hijau-muda text-teks-utama font-semibold">
                  <tr>
                    <th className="py-2.5 px-3 text-center w-12">No</th>
                    <th className="py-2.5 px-3 min-w-[200px]">Nama Guru</th>
                    {kalkulasi.kriteriaList.map((k) => (
                      <th key={k.kode} className="py-2.5 px-3 text-center">
                        r_{k.kode}
                      </th>
                    ))}
                  </tr>
                </thead>
                <tbody className="divide-y divide-hijau-muda/50 text-teks-utama">
                  {kalkulasi.matriksNormalisasi.map((row, idx) => (
                    <tr key={row.guruId} className="hover:bg-hijau-soft/40">
                      <td className="py-2 px-3 text-center font-medium">{idx + 1}</td>
                      <td className="py-2 px-3 font-semibold">{row.nama}</td>
                      {kalkulasi.kriteriaList.map((k) => (
                        <td key={k.kode} className="py-2 px-3 text-center font-mono font-medium">
                          {row.nilai[k.kode] ? row.nilai[k.kode].toFixed(4) : '-'}
                        </td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {/* Tab D: Matriks Terbobot (vij) */}
        {activeTab === 'D' && (
          <div className="bg-white rounded-xl border border-hijau-muda overflow-hidden space-y-4 p-4">
            <div>
              <h3 className="font-semibold text-sm text-teks-utama">
                D. Matriks Terbobot (vij = wj × rij)
              </h3>
              <p className="text-xs text-teks-sekunder mt-0.5">
                Hasil perkalian nilai normalisasi dengan bobot kriteria masing-masing
              </p>
            </div>

            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs">
                <thead className="bg-hijau-soft border-b border-hijau-muda text-teks-utama font-semibold">
                  <tr>
                    <th className="py-2.5 px-3 text-center w-12">No</th>
                    <th className="py-2.5 px-3 min-w-[200px]">Nama Guru</th>
                    {kalkulasi.kriteriaList.map((k) => (
                      <th key={k.kode} className="py-2.5 px-3 text-center">
                        v_{k.kode} ({k.bobot * 100}%)
                      </th>
                    ))}
                  </tr>
                </thead>
                <tbody className="divide-y divide-hijau-muda/50 text-teks-utama">
                  {kalkulasi.matriksTerbobot.map((row, idx) => (
                    <tr key={row.guruId} className="hover:bg-hijau-soft/40">
                      <td className="py-2 px-3 text-center font-medium">{idx + 1}</td>
                      <td className="py-2 px-3 font-semibold">{row.nama}</td>
                      {kalkulasi.kriteriaList.map((k) => (
                        <td key={k.kode} className="py-2 px-3 text-center font-mono font-medium">
                          {row.nilai[k.kode] ? row.nilai[k.kode].toFixed(4) : '-'}
                        </td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {/* Tab E: Nilai Optimasi (Yi) */}
        {activeTab === 'E' && (
          <div className="bg-white rounded-xl border border-hijau-muda overflow-hidden space-y-4 p-4">
            <div>
              <h3 className="font-semibold text-sm text-teks-utama">
                E. Nilai Optimasi Preferensi (Yi = ∑ Benefit - ∑ Cost)
              </h3>
              <p className="text-xs text-teks-sekunder mt-0.5">
                Penjumlahan seluruh atribut terbobot kriteria benefit
              </p>
            </div>

            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs">
                <thead className="bg-hijau-soft border-b border-hijau-muda text-teks-utama font-semibold">
                  <tr>
                    <th className="py-2.5 px-3 text-center w-12">No</th>
                    <th className="py-2.5 px-3 min-w-[200px]">Nama Guru</th>
                    <th className="py-2.5 px-3 text-center">Total Nilai Terbobot (Yi)</th>
                    <th className="py-2.5 px-3 text-center">Ranking</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-hijau-muda/50 text-teks-utama">
                  {kalkulasi.hasilAkhir.map((row, idx) => (
                    <tr key={row.guruId} className="hover:bg-hijau-soft/40">
                      <td className="py-2 px-3 text-center font-medium">{idx + 1}</td>
                      <td className="py-2 px-3 font-semibold">{row.nama}</td>
                      <td className="py-2 px-3 text-center font-mono font-bold text-hijau-utama">
                        {row.nilaiPreferensi.toFixed(4)}
                      </td>
                      <td className="py-2 px-3 text-center font-bold">#{row.ranking}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {/* Tab F: Hasil Ranking Final */}
        {activeTab === 'F' && (
          <div className="bg-white rounded-xl border border-hijau-muda overflow-hidden space-y-4 p-4">
            <div className="flex items-center justify-between">
              <h3 className="font-semibold text-sm text-teks-utama">
                F. Pemeringkatan Akhir (Ranking 1 - {kalkulasi.hasilAkhir.length})
              </h3>
            </div>

            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs">
                <thead className="bg-hijau-soft border-b border-hijau-muda text-teks-utama font-semibold">
                  <tr>
                    <th className="py-2.5 px-3 text-center w-14">Ranking</th>
                    <th className="py-2.5 px-3">Nama Guru & NIP</th>
                    <th className="py-2.5 px-3">Mata Pelajaran</th>
                    <th className="py-2.5 px-3 text-center">Nilai MOORA (Yi)</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-hijau-muda/50 text-teks-utama">
                  {kalkulasi.hasilAkhir.map((row) => (
                    <tr key={row.guruId} className="hover:bg-hijau-soft/40">
                      <td className="py-2.5 px-3 text-center font-bold text-teks-utama">
                        {row.ranking}
                      </td>
                      <td className="py-2.5 px-3">
                        <div className="font-semibold">{row.nama}</div>
                        <div className="text-[10px] font-mono text-teks-sekunder">{row.nip}</div>
                      </td>
                      <td className="py-2.5 px-3 text-teks-sekunder">{row.jabatan}</td>
                      <td className="py-2.5 px-3 text-center font-mono font-bold text-hijau-utama">
                        {row.nilaiPreferensi.toFixed(4)}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}
      </div>
    </AppLayout>
  );
}
