'use client';

import React, { useState, useEffect } from 'react';
import AppLayout from '@/components/dashboard/AppLayout';
import { Calendar } from 'lucide-react';
import { getPredikatNilai } from '@/lib/utils';

export default function GuruHasilPage() {
  const [session, setSession] = useState<any>(null);
  const [guruData, setGuruData] = useState<any>(null);
  const [periodeList, setPeriodeList] = useState<any[]>([]);
  const [selectedPeriodeId, setSelectedPeriodeId] = useState<string>('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const init = async () => {
      try {
        const meRes = await fetch('/api/auth/me');
        const meData = await meRes.json();
        setSession(meData.user);

        const pRes = await fetch('/api/periode');
        const pData = await pRes.json();
        setPeriodeList(pData);
        if (pData.length > 0) setSelectedPeriodeId(pData[0].id);

        if (meData.user?.guruId) {
          const gRes = await fetch(`/api/guru/${meData.user.guruId}`);
          const gData = await gRes.json();
          setGuruData(gData);
        }
      } catch (e) {
        console.error(e);
      } finally {
        setLoading(false);
      }
    };
    init();
  }, []);

  const selectedPenilaian = (guruData?.penilaian || []).find(
    (p: any) => p.periodeId === selectedPeriodeId
  );

  const selectedMoora = (guruData?.hasilMoora || []).find(
    (m: any) => m.periodeId === selectedPeriodeId
  );

  const details = selectedPenilaian?.details || [];
  const avg =
    details.length > 0
      ? details.reduce((s: number, d: any) => s + d.nilai, 0) / details.length
      : 0;
  const predikat = getPredikatNilai(avg);

  return (
    <AppLayout
      title="Hasil Penilaian Mandiri"
      subtitle="Rincian perolehan nilai 4 kriteria evaluasi dan preferensi MOORA"
      user={session || { nama: 'Guru Pengajar', username: 'guru', role: 'GURU' }}
    >
      <div className="max-w-4xl space-y-6">
        {/* Selector Periode */}
        <div className="p-4 bg-white rounded-xl border border-hijau-muda flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div className="flex items-center gap-3">
            <Calendar className="w-4 h-4 text-hijau-utama shrink-0" />
            <div>
              <h3 className="font-semibold text-xs text-teks-utama">Pilih Periode Penilaian</h3>
              <p className="text-[11px] text-teks-sekunder">Melihat hasil evaluasi pada periode tertentu</p>
            </div>
          </div>
          <select
            value={selectedPeriodeId}
            onChange={(e) => setSelectedPeriodeId(e.target.value)}
            className="px-3 py-1.5 bg-latar-soft border border-hijau-muda rounded-lg text-xs font-medium text-teks-utama focus:ring-2 focus:ring-hijau-utama min-w-[200px]"
          >
            {periodeList.map((p) => (
              <option key={p.id} value={p.id}>
                {p.namaPeriode} ({p.status})
              </option>
            ))}
          </select>
        </div>

        {/* Ringkasan Skor */}
        {selectedMoora && (
          <div className="p-4 bg-white rounded-xl border border-hijau-muda flex flex-col sm:flex-row sm:items-center justify-between gap-4">
            <div className="space-y-1">
              <span className="text-xs font-medium text-teks-sekunder">Nilai Preferensi MOORA (Yi)</span>
              <p className="text-2xl font-bold font-mono text-hijau-utama">
                {selectedMoora.nilaiPreferensi.toFixed(4)}
              </p>
            </div>

            <div className="flex items-center gap-4 text-xs">
              <div>
                <span className="text-teks-sekunder block">Peringkat Sekolah</span>
                <span className="font-bold text-base text-teks-utama">#{selectedMoora.ranking}</span>
              </div>
              <div className="border-l border-hijau-muda pl-4">
                <span className="text-teks-sekunder block">Predikat Kinerja</span>
                <span className="font-semibold text-sm text-teks-utama">{predikat.label}</span>
              </div>
            </div>
          </div>
        )}

        {/* Tabel 4 Kriteria */}
        <div className="bg-white rounded-xl border border-hijau-muda overflow-hidden">
          <div className="p-4 border-b border-hijau-muda flex items-center justify-between">
            <h3 className="font-semibold text-sm text-teks-utama">
              Rincian Capaian 4 Kriteria Evaluasi
            </h3>
            <span className="text-xs text-teks-sekunder">Skala Likert (1 - 5)</span>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-hijau-soft border-b border-hijau-muda text-teks-utama font-semibold">
                <tr>
                  <th className="py-2.5 px-3 text-center w-14">Kode</th>
                  <th className="py-2.5 px-3">Nama Kriteria Penilaian</th>
                  <th className="py-2.5 px-3 text-center w-28">Bobot</th>
                  <th className="py-2.5 px-3 text-center w-28">Skor Mentah (1-5)</th>
                  <th className="py-2.5 px-3 text-center w-36">Predikat</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-hijau-muda/50 text-teks-utama">
                {loading ? (
                  <tr>
                    <td colSpan={5} className="text-center py-8 text-teks-sekunder">
                      Memuat nilai kriteria...
                    </td>
                  </tr>
                ) : details.length === 0 ? (
                  <tr>
                    <td colSpan={5} className="text-center py-8 text-teks-sekunder">
                      Belum ada penilaian pada periode ini.
                    </td>
                  </tr>
                ) : (
                  details.map((item: any) => {
                    const subPredikat = getPredikatNilai(item.nilai);
                    return (
                      <tr key={item.id} className="hover:bg-hijau-soft/40 transition-colors">
                        <td className="py-2.5 px-3 text-center font-bold text-hijau-utama">
                          {item.kriteria.kode}
                        </td>
                        <td className="py-2.5 px-3 font-semibold text-teks-utama">
                          {item.kriteria.nama}
                        </td>
                        <td className="py-2.5 px-3 text-center text-teks-sekunder font-medium">
                          {(item.kriteria.bobot * 100).toFixed(0)}%
                        </td>
                        <td className="py-2.5 px-3 text-center font-bold text-sm">
                          {item.nilai}
                        </td>
                        <td className="py-2.5 px-3 text-center">
                          <span className="text-[11px] font-medium text-teks-utama">
                            {subPredikat.label}
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
