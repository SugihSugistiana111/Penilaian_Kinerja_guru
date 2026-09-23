'use client';

import React, { useState, useEffect } from 'react';
import AppLayout from '@/components/dashboard/AppLayout';
import { History } from 'lucide-react';

export default function GuruRiwayatPage() {
  const [session, setSession] = useState<any>(null);
  const [guruData, setGuruData] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const meRes = await fetch('/api/auth/me');
        const meData = await meRes.json();
        setSession(meData.user);

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
    fetchData();
  }, []);

  const riwayatList = guruData?.penilaian || [];

  return (
    <AppLayout
      title="Riwayat Evaluasi Kinerja"
      subtitle="Arsip historis penilaian kinerja mandiri dari setiap periode"
      user={session || { nama: 'Guru Pengajar', username: 'guru', role: 'GURU' }}
    >
      <div className="max-w-5xl space-y-6">
        <div className="bg-white rounded-xl border border-hijau-muda overflow-hidden">
          <div className="p-4 border-b border-hijau-muda flex items-center justify-between">
            <div className="flex items-center gap-2">
              <History className="w-4 h-4 text-hijau-utama" />
              <h3 className="font-semibold text-sm text-teks-utama">
                Histori Penilaian ({guruData?.nama})
              </h3>
            </div>
            <span className="text-xs text-teks-sekunder">Total {riwayatList.length} Periode</span>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-hijau-soft border-b border-hijau-muda text-teks-utama font-semibold">
                <tr>
                  <th className="py-2.5 px-3">Periode</th>
                  <th className="py-2.5 px-2 text-center w-14">C1</th>
                  <th className="py-2.5 px-2 text-center w-14">C2</th>
                  <th className="py-2.5 px-2 text-center w-14">C3</th>
                  <th className="py-2.5 px-2 text-center w-14">C4</th>
                  <th className="py-2.5 px-3 text-center">Nilai MOORA</th>
                  <th className="py-2.5 px-3 text-center">Peringkat</th>
                  <th className="py-2.5 px-3">Catatan Evaluator</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-hijau-muda/50 text-teks-utama">
                {loading ? (
                  <tr>
                    <td colSpan={8} className="text-center py-8 text-teks-sekunder">
                      Memuat riwayat...
                    </td>
                  </tr>
                ) : riwayatList.length === 0 ? (
                  <tr>
                    <td colSpan={8} className="text-center py-8 text-teks-sekunder">
                      Belum ada riwayat penilaian.
                    </td>
                  </tr>
                ) : (
                  riwayatList.map((pen: any) => {
                    const moora = guruData.hasilMoora?.find((m: any) => m.periodeId === pen.periodeId);
                    const mapSkor: Record<string, number> = {};
                    pen.details.forEach((d: any) => {
                      mapSkor[d.kriteria.kode] = d.nilai;
                    });

                    return (
                      <tr key={pen.id} className="hover:bg-hijau-soft/40 transition-colors">
                        <td className="py-2.5 px-3 font-semibold text-teks-utama">
                          {pen.periode.namaPeriode}
                        </td>
                        <td className="py-2.5 px-2 text-center font-bold">{mapSkor['C1'] || '-'}</td>
                        <td className="py-2.5 px-2 text-center font-bold">{mapSkor['C2'] || '-'}</td>
                        <td className="py-2.5 px-2 text-center font-bold">{mapSkor['C3'] || '-'}</td>
                        <td className="py-2.5 px-2 text-center font-bold">{mapSkor['C4'] || '-'}</td>
                        <td className="py-2.5 px-3 text-center font-mono font-bold text-hijau-utama">
                          {moora ? moora.nilaiPreferensi.toFixed(4) : '-'}
                        </td>
                        <td className="py-2.5 px-3 text-center font-bold">
                          {moora ? `#${moora.ranking}` : '-'}
                        </td>
                        <td className="py-2.5 px-3 text-teks-sekunder">{pen.catatan || '-'}</td>
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
