'use client';

import React, { useState, useEffect } from 'react';
import AppLayout from '@/components/dashboard/AppLayout';
import Link from 'next/link';
import {
  Calculator,
  CheckCircle2,
  AlertTriangle,
  ArrowRight,
  Trophy,
  Calendar,
} from 'lucide-react';

interface PeriodeItem {
  id: string;
  namaPeriode: string;
  status: string;
}

export default function AdminMooraPage() {
  const [periodeList, setPeriodeList] = useState<PeriodeItem[]>([]);
  const [selectedPeriodeId, setSelectedPeriodeId] = useState<string>('');
  const [validasiData, setValidasiData] = useState<any>(null);
  const [hasilTersimpan, setHasilTersimpan] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [executing, setExecuting] = useState(false);
  const [feedback, setFeedback] = useState<{ type: 'success' | 'error'; text: string } | null>(null);

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

  const fetchDetailMoora = async (periodeId: string) => {
    if (!periodeId) return;
    setLoading(true);
    try {
      const res = await fetch(`/api/moora/detail?periodeId=${periodeId}`);
      const data = await res.json();
      setValidasiData(data.validasi);
      setHasilTersimpan(data.hasilTersimpan || []);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (selectedPeriodeId) {
      fetchDetailMoora(selectedPeriodeId);
    }
  }, [selectedPeriodeId]);

  const handleHitungMoora = async () => {
    if (!selectedPeriodeId) return;
    setExecuting(true);
    setFeedback(null);

    try {
      const res = await fetch('/api/moora/hitung', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ periodeId: selectedPeriodeId }),
      });

      const data = await res.json();
      if (!res.ok) {
        throw new Error(data.error || 'Gagal mengeksekusi metode MOORA');
      }

      setFeedback({
        type: 'success',
        text: `Perhitungan MOORA berhasil dijalankan. ${data.data.length} guru telah diperingkat.`,
      });

      await fetchDetailMoora(selectedPeriodeId);
    } catch (err: any) {
      setFeedback({ type: 'error', text: err.message || 'Terjadi kesalahan' });
    } finally {
      setExecuting(false);
    }
  };

  const selectedPeriode = periodeList.find((p) => p.id === selectedPeriodeId);
  const persentase =
    validasiData?.totalGuru > 0
      ? Math.round((validasiData.dinilaiCount / validasiData.totalGuru) * 100)
      : 0;

  return (
    <AppLayout
      title="Proses Metode MOORA"
      subtitle="Validasi kelengkapan data evaluasi dan komputasi perankingan kinerja guru"
      user={{ nama: 'Administrator SPK', username: 'admin', role: 'ADMIN' }}
    >
      <div className="space-y-6">
        {/* Selector Periode */}
        <div className="p-4 bg-white rounded-xl border border-hijau-muda flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div className="flex items-center gap-3">
            <Calendar className="w-4 h-4 text-hijau-utama" />
            <label className="text-xs font-semibold text-teks-utama">Pilih Periode Penilaian:</label>
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
          </div>

          <span className="text-xs text-teks-sekunder">
            Status Periode: <strong className="text-teks-utama">{selectedPeriode?.status || '-'}</strong>
          </span>
        </div>

        {/* Feedback Message */}
        {feedback && (
          <div
            className={`p-3.5 rounded-lg text-xs font-medium flex items-center gap-2 ${
              feedback.type === 'success'
                ? 'bg-emerald-50 text-emerald-800 border border-emerald-200'
                : 'bg-red-50 text-red-800 border border-red-200'
            }`}
          >
            {feedback.type === 'success' ? (
              <CheckCircle2 className="w-4 h-4 shrink-0" />
            ) : (
              <AlertTriangle className="w-4 h-4 shrink-0" />
            )}
            <span>{feedback.text}</span>
          </div>
        )}

        {/* Card Validasi Kelengkapan Data */}
        <div className="bg-white p-6 rounded-xl border border-hijau-muda space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="font-semibold text-sm text-teks-utama">
              Status Kelengkapan Penilaian ({selectedPeriode?.namaPeriode})
            </h3>
            <span
              className={`text-xs font-bold px-2.5 py-0.5 rounded ${
                validasiData?.isLengkap
                  ? 'bg-emerald-100 text-emerald-800'
                  : 'bg-amber-100 text-amber-900'
              }`}
            >
              {validasiData?.isLengkap ? 'Lengkap 100%' : 'Belum Lengkap'}
            </span>
          </div>

          <div className="space-y-1.5">
            <div className="flex justify-between text-xs text-teks-sekunder font-medium">
              <span>{validasiData?.dinilaiCount || 0} dari {validasiData?.totalGuru || 0} guru telah dinilai</span>
              <span>{persentase}%</span>
            </div>
            <div className="w-full h-2 bg-hijau-soft rounded-full overflow-hidden">
              <div
                className="h-full bg-hijau-utama rounded-full transition-all duration-300"
                style={{ width: `${persentase}%` }}
              />
            </div>
          </div>

          {/* Kondisi Validasi */}
          {validasiData?.isLengkap ? (
            <div className="p-4 rounded-lg bg-emerald-50/70 border border-emerald-200 text-xs text-emerald-900 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
              <div>
                <p className="font-semibold">Seluruh data penilaian lengkap.</p>
                <p className="text-[11px] text-emerald-700 mt-0.5">
                  Seluruh {validasiData?.totalGuru || 0} guru aktif telah memiliki nilai pada 4 kriteria. Sistem siap mengeksekusi perhitungan MOORA.
                </p>
              </div>

              <button
                onClick={handleHitungMoora}
                disabled={executing}
                className="px-5 py-2 bg-hijau-utama hover:bg-hijau-hover text-white rounded-lg text-xs font-semibold flex items-center justify-center gap-1.5 transition-colors shrink-0 disabled:opacity-50"
              >
                <Calculator className="w-4 h-4" />
                <span>{executing ? 'Menghitung MOORA...' : 'Hitung Nilai MOORA'}</span>
              </button>
            </div>
          ) : (
            <div className="p-4 rounded-lg bg-amber-50/70 border border-amber-200 text-xs text-amber-900 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
              <div>
                <p className="font-semibold">Penilaian belum lengkap.</p>
                <p className="text-[11px] text-amber-800 mt-0.5">
                  Terdapat {validasiData?.belumDinilaiCount || 0} guru yang belum dinilai. Selesaikan penilaian sebelum komputasi MOORA.
                </p>
              </div>

              <Link
                href="/admin/penilaian"
                className="px-4 py-2 bg-latar-soft hover:bg-amber-100 border border-amber-300 text-amber-950 rounded-lg text-xs font-semibold shrink-0 text-center"
              >
                Lengkapi Penilaian →
              </Link>
            </div>
          )}
        </div>

        {/* Tabel Ringkasan Hasil MOORA Terhitung */}
        <div className="bg-white rounded-xl border border-hijau-muda overflow-hidden">
          <div className="p-4 border-b border-hijau-muda flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Trophy className="w-4 h-4 text-hijau-utama" />
              <h3 className="font-semibold text-sm text-teks-utama">
                Hasil Perhitungan MOORA Tersimpan ({hasilTersimpan.length} Guru)
              </h3>
            </div>

            {hasilTersimpan.length > 0 && (
              <div className="flex items-center gap-2">
                <Link
                  href={`/admin/moora/${selectedPeriodeId}`}
                  className="text-xs font-semibold text-hijau-utama hover:underline flex items-center gap-1"
                >
                  <span>Detail Matriks Perhitungan</span>
                  <ArrowRight className="w-3.5 h-3.5" />
                </Link>
              </div>
            )}
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-hijau-soft border-b border-hijau-muda text-teks-utama font-semibold">
                <tr>
                  <th className="py-2.5 px-3 text-center w-14">Ranking</th>
                  <th className="py-2.5 px-3">Nama Guru & NIP</th>
                  <th className="py-2.5 px-3">Mata Pelajaran</th>
                  <th className="py-2.5 px-3 text-center">Nilai MOORA (Yi)</th>
                  <th className="py-2.5 px-3 text-center">Waktu Eksekusi</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-hijau-muda/50 text-teks-utama">
                {loading ? (
                  <tr>
                    <td colSpan={5} className="py-8 text-center text-teks-sekunder">
                      Memeriksa data MOORA...
                    </td>
                  </tr>
                ) : hasilTersimpan.length === 0 ? (
                  <tr>
                    <td colSpan={5} className="py-8 text-center text-teks-sekunder">
                      Belum ada perhitungan MOORA yang tersimpan pada periode ini.
                    </td>
                  </tr>
                ) : (
                  hasilTersimpan.map((row) => (
                    <tr key={row.id} className="hover:bg-hijau-soft/40 transition-colors">
                      <td className="py-2.5 px-3 text-center font-bold text-teks-utama">
                        {row.ranking}
                      </td>
                      <td className="py-2.5 px-3">
                        <div className="font-semibold">{row.guru.nama}</div>
                        <div className="text-[10px] font-mono text-teks-sekunder">{row.guru.nip}</div>
                      </td>
                      <td className="py-2.5 px-3 text-teks-sekunder">{row.guru.jabatanTugasMengajar}</td>
                      <td className="py-2.5 px-3 text-center font-mono font-bold text-hijau-utama">
                        {row.nilaiPreferensi.toFixed(4)}
                      </td>
                      <td className="py-2.5 px-3 text-center text-teks-sekunder text-[11px]">
                        {new Date(row.createdAt).toLocaleDateString('id-ID', {
                          day: '2-digit',
                          month: 'short',
                          year: 'numeric',
                        })}
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
