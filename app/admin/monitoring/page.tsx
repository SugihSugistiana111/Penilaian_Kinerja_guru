'use client';

import React, { useState, useEffect } from 'react';
import AppLayout from '@/components/dashboard/AppLayout';
import {
  LineChart as LineChartIcon,
  TrendingUp,
  User,
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

interface GuruItem {
  id: string;
  nama: string;
  nip: string;
  jabatanTugasMengajar: string;
}

export default function AdminMonitoringPage() {
  const [daftarGuru, setDaftarGuru] = useState<GuruItem[]>([]);
  const [selectedGuruId, setSelectedGuruId] = useState<string>('');
  const [monitoringData, setMonitoringData] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchGuru = async () => {
      try {
        const res = await fetch('/api/guru?statusAktif=true');
        const data: GuruItem[] = await res.json();
        setDaftarGuru(data);
        if (data.length > 0) {
          setSelectedGuruId(data[0].id);
        }
      } catch (e) {
        console.error(e);
      }
    };
    fetchGuru();
  }, []);

  const fetchMonitoring = async (guruId: string) => {
    if (!guruId) return;
    setLoading(true);
    try {
      const res = await fetch(`/api/guru/${guruId}`);
      const guru = await res.json();

      const chartPoints = (guru.penilaian || []).map((pen: any) => {
        const moora = (guru.hasilMoora || []).find((m: any) => m.periodeId === pen.periodeId);
        const point: any = {
          periode: pen.periode.namaPeriode,
          nilaiMoora: moora ? Number(moora.nilaiPreferensi.toFixed(4)) : null,
          ranking: moora ? moora.ranking : null,
        };

        pen.details.forEach((d: any) => {
          point[d.kriteria.kode] = d.nilai;
        });

        return point;
      }).reverse();

      setMonitoringData({ guru, chartPoints });
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (selectedGuruId) {
      fetchMonitoring(selectedGuruId);
    }
  }, [selectedGuruId]);

  return (
    <AppLayout
      title="Monitoring Kinerja Guru"
      subtitle="Analisis grafik perkembangan skor 4 kriteria dan nilai preferensi antar periode"
      user={{ nama: 'Administrator SPK', username: 'admin', role: 'ADMIN' }}
    >
      <div className="space-y-6">
        {/* Guru Selector */}
        <div className="p-4 bg-white rounded-xl border border-hijau-muda flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div className="flex items-center gap-3">
            <User className="w-4 h-4 text-hijau-utama" />
            <label className="text-xs font-semibold text-teks-utama">Pilih Guru:</label>
            <select
              value={selectedGuruId}
              onChange={(e) => setSelectedGuruId(e.target.value)}
              className="px-3 py-1.5 bg-latar-soft border border-hijau-muda rounded-lg text-xs font-medium text-teks-utama focus:ring-2 focus:ring-hijau-utama min-w-[240px]"
            >
              {daftarGuru.map((g) => (
                <option key={g.id} value={g.id}>
                  {g.nama} ({g.jabatanTugasMengajar})
                </option>
              ))}
            </select>
          </div>

          <span className="text-xs text-teks-sekunder">
            Total {daftarGuru.length} guru aktif
          </span>
        </div>

        {loading ? (
          <div className="bg-white p-12 rounded-xl border border-hijau-muda text-center text-xs text-teks-sekunder">
            Memuat grafik monitoring...
          </div>
        ) : !monitoringData ? (
          <div className="bg-white p-12 rounded-xl border border-hijau-muda text-center text-xs text-teks-sekunder">
            Data guru tidak ditemukan.
          </div>
        ) : (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Grafik 4 Kriteria Penilaian */}
            <div className="bg-white p-5 rounded-xl border border-hijau-muda space-y-3">
              <div>
                <h3 className="font-semibold text-sm text-teks-utama flex items-center gap-2">
                  <TrendingUp className="w-4 h-4 text-hijau-utama" />
                  <span>Tren Capaian 4 Kriteria ({monitoringData.guru.nama})</span>
                </h3>
                <p className="text-[11px] text-teks-sekunder mt-0.5">
                  C1: Kehadiran (35%), C2: Ketepatan (25%), C3: Perangkat (25%), C4: Administrasi (15%)
                </p>
              </div>

              <div className="h-64 w-full pt-2">
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={monitoringData.chartPoints}>
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

            {/* Grafik Nilai Preferensi MOORA */}
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
                  <LineChart data={monitoringData.chartPoints}>
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
