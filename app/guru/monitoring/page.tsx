'use client';

import React, { useState, useEffect } from 'react';
import AppLayout from '@/components/dashboard/AppLayout';
import {
  TrendingUp,
  LineChart as LineChartIcon,
} from 'lucide-react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';

export default function GuruMonitoringPage() {
  const [session, setSession] = useState<any>(null);
  const [chartPoints, setChartPoints] = useState<any[]>([]);
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

          const points = (gData.penilaian || []).map((pen: any) => {
            const moora = (gData.hasilMoora || []).find((m: any) => m.periodeId === pen.periodeId);
            const pt: any = {
              periode: pen.periode.namaPeriode,
              nilaiMoora: moora ? Number(moora.nilaiPreferensi.toFixed(4)) : null,
              ranking: moora ? moora.ranking : null,
            };

            pen.details.forEach((d: any) => {
              pt[d.kriteria.kode] = d.nilai;
            });

            return pt;
          }).reverse();

          setChartPoints(points);
        }
      } catch (e) {
        console.error(e);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  return (
    <AppLayout
      title="Grafik Perkembangan Kinerja"
      subtitle="Analisis tren capaian skor 4 kriteria evaluasi diri sendiri antar periode"
      user={session || { nama: 'Guru Pengajar', username: 'guru', role: 'GURU' }}
    >
      <div className="space-y-6">
        {loading ? (
          <div className="bg-white p-12 rounded-xl border border-hijau-muda text-center text-xs text-teks-sekunder">
            Memuat grafik...
          </div>
        ) : chartPoints.length === 0 ? (
          <div className="bg-white p-12 rounded-xl border border-hijau-muda text-center text-xs text-teks-sekunder">
            Belum ada data perkembangan evaluasi.
          </div>
        ) : (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Chart 4 Kriteria */}
            <div className="bg-white p-5 rounded-xl border border-hijau-muda space-y-3">
              <div>
                <h3 className="font-semibold text-sm text-teks-utama flex items-center gap-2">
                  <TrendingUp className="w-4 h-4 text-hijau-utama" />
                  <span>Tren Capaian 4 Kriteria Evaluasi</span>
                </h3>
                <p className="text-[11px] text-teks-sekunder mt-0.5">
                  C1: Kehadiran (35%), C2: Ketepatan (25%), C3: Perangkat (25%), C4: Administrasi (15%)
                </p>
              </div>

              <div className="h-64 w-full pt-2">
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={chartPoints}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#DCEBDD" />
                    <XAxis dataKey="periode" stroke="#68756C" fontSize={11} />
                    <YAxis domain={[1, 5]} stroke="#68756C" fontSize={11} />
                    <Tooltip />
                    <Legend wrapperStyle={{ fontSize: 11 }} />
                    <Line type="monotone" dataKey="C1" name="C1 Kehadiran" stroke="#86A889" strokeWidth={2.5} dot={{ r: 3 }} />
                    <Line type="monotone" dataKey="C2" name="C2 Ketepatan" stroke="#D97706" strokeWidth={2} dot={{ r: 3 }} />
                    <Line type="monotone" dataKey="C3" name="C3 Perangkat" stroke="#2563EB" strokeWidth={2} dot={{ r: 3 }} />
                    <Line type="monotone" dataKey="C4" name="C4 Administrasi" stroke="#7C3AED" strokeWidth={2} dot={{ r: 3 }} />
                  </LineChart>
                </ResponsiveContainer>
              </div>
            </div>

            {/* Nilai MOORA */}
            <div className="bg-white p-5 rounded-xl border border-hijau-muda space-y-3">
              <div>
                <h3 className="font-semibold text-sm text-teks-utama flex items-center gap-2">
                  <LineChartIcon className="w-4 h-4 text-hijau-utama" />
                  <span>Tren Nilai Preferensi MOORA (Yi)</span>
                </h3>
                <p className="text-[11px] text-teks-sekunder mt-0.5">
                  Perkembangan nilai optimasi akhir pada setiap periode
                </p>
              </div>

              <div className="h-64 w-full pt-2">
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={chartPoints}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#DCEBDD" />
                    <XAxis dataKey="periode" stroke="#68756C" fontSize={11} />
                    <YAxis stroke="#68756C" fontSize={11} />
                    <Tooltip />
                    <Legend wrapperStyle={{ fontSize: 11 }} />
                    <Line
                      type="monotone"
                      dataKey="nilaiMoora"
                      name="Nilai MOORA"
                      stroke="#86A889"
                      strokeWidth={3}
                      dot={{ r: 4, fill: '#86A889' }}
                    />
                  </LineChart>
                </ResponsiveContainer>
              </div>
            </div>
          </div>
        )}
      </div>
    </AppLayout>
  );
}
