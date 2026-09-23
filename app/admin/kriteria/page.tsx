'use client';

import React, { useState, useEffect } from 'react';
import AppLayout from '@/components/dashboard/AppLayout';
import { Save, CheckCircle2, AlertCircle, Scale } from 'lucide-react';

interface KriteriaData {
  id: string;
  kode: string;
  nama: string;
  bobot: number;
  jenis: string;
  status: boolean;
}

export default function AdminKriteriaPage() {
  const [kriteriaList, setKriteriaList] = useState<KriteriaData[]>([]);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState<{ type: 'success' | 'error'; text: string } | null>(null);

  const fetchKriteria = async () => {
    setLoading(true);
    try {
      const res = await fetch('/api/kriteria');
      const data = await res.json();
      setKriteriaList(data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchKriteria();
  }, []);

  const handleBobotChange = (id: string, newBobotVal: number) => {
    setKriteriaList((prev) =>
      prev.map((k) => (k.id === id ? { ...k, bobot: newBobotVal } : k))
    );
  };

  const handleNamaChange = (id: string, newNama: string) => {
    setKriteriaList((prev) =>
      prev.map((k) => (k.id === id ? { ...k, nama: newNama } : k))
    );
  };

  const totalPersen = kriteriaList.reduce((sum, k) => sum + (k.bobot > 1 ? k.bobot : k.bobot * 100), 0);
  const isValidTotal = Math.abs(totalPersen - 100) < 0.1;

  const handleSimpan = async () => {
    if (!isValidTotal) {
      setMessage({
        type: 'error',
        text: `Total bobot harus tepat 100%. Saat ini total bobot adalah ${totalPersen.toFixed(1)}%.`,
      });
      return;
    }

    setSaving(true);
    setMessage(null);

    try {
      const payload = {
        kriteria: kriteriaList.map((k) => ({
          id: k.id,
          nama: k.nama,
          bobot: k.bobot > 1 ? k.bobot / 100 : k.bobot,
          jenis: k.jenis,
        })),
      };

      const res = await fetch('/api/kriteria', {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });

      const data = await res.json();
      if (!res.ok) throw new Error(data.error || 'Gagal menyimpan bobot kriteria');

      setMessage({ type: 'success', text: 'Bobot kriteria berhasil diperbarui.' });
      fetchKriteria();
    } catch (err: any) {
      setMessage({ type: 'error', text: err.message || 'Terjadi kesalahan' });
    } finally {
      setSaving(false);
    }
  };

  return (
    <AppLayout
      title="Kriteria & Bobot Penilaian"
      subtitle="Pengaturan 4 kriteria evaluasi kinerja guru metode MOORA (Total bobot = 100%)"
      user={{ nama: 'Administrator SPK', username: 'admin', role: 'ADMIN' }}
    >
      <div className="space-y-6">
        {/* Status Total Bobot */}
        <div
          className={`p-4 rounded-xl border flex flex-col sm:flex-row sm:items-center justify-between gap-3 text-xs ${
            isValidTotal
              ? 'bg-emerald-50 text-emerald-900 border-emerald-200'
              : 'bg-amber-50 text-amber-900 border-amber-200'
          }`}
        >
          <div className="flex items-center gap-2">
            <Scale className="w-4 h-4 text-hijau-utama shrink-0" />
            <div>
              <span className="font-semibold">
                Status Total Bobot: {totalPersen.toFixed(0)}% / 100%
              </span>
              <p className="text-[11px] text-teks-sekunder mt-0.5">
                {isValidTotal
                  ? 'Total bobot telah valid (100%) dan siap digunakan untuk komputasi MOORA.'
                  : 'Total bobot belum 100%. Harap sesuaikan kembali bobot masing-masing kriteria.'}
              </p>
            </div>
          </div>

          <button
            onClick={handleSimpan}
            disabled={saving || !isValidTotal}
            className="px-4 py-2 bg-hijau-utama hover:bg-hijau-hover text-white rounded-lg text-xs font-semibold flex items-center justify-center gap-1.5 transition-colors disabled:opacity-50 shrink-0"
          >
            <Save className="w-4 h-4" />
            <span>{saving ? 'Menyimpan...' : 'Simpan Pengaturan Bobot'}</span>
          </button>
        </div>

        {message && (
          <div
            className={`p-3 rounded-lg text-xs font-medium flex items-center gap-2 ${
              message.type === 'success'
                ? 'bg-emerald-50 text-emerald-800 border border-emerald-200'
                : 'bg-red-50 text-red-800 border border-red-200'
            }`}
          >
            {message.type === 'success' ? (
              <CheckCircle2 className="w-4 h-4 shrink-0" />
            ) : (
              <AlertCircle className="w-4 h-4 shrink-0" />
            )}
            <span>{message.text}</span>
          </div>
        )}

        {/* Tabel Kriteria */}
        <div className="bg-white rounded-xl border border-hijau-muda overflow-hidden">
          <div className="p-4 border-b border-hijau-muda">
            <h3 className="font-semibold text-sm text-teks-utama">Daftar Kriteria Evaluasi Kinerja</h3>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-hijau-soft border-b border-hijau-muda text-teks-utama font-semibold">
                <tr>
                  <th className="py-2.5 px-3 text-center w-14">Kode</th>
                  <th className="py-2.5 px-3">Nama Kriteria Penilaian</th>
                  <th className="py-2.5 px-3 text-center w-28">Jenis</th>
                  <th className="py-2.5 px-3 text-center w-36">Bobot (%)</th>
                  <th className="py-2.5 px-3 text-center w-28">Desimal (wj)</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-hijau-muda/50 text-teks-utama">
                {loading ? (
                  <tr>
                    <td colSpan={5} className="py-8 text-center text-teks-sekunder">
                      Memuat kriteria...
                    </td>
                  </tr>
                ) : (
                  kriteriaList.map((k) => {
                    const persenVal = k.bobot > 1 ? k.bobot : k.bobot * 100;
                    return (
                      <tr key={k.id} className="hover:bg-hijau-soft/40 transition-colors">
                        <td className="py-3 px-3 text-center font-bold text-hijau-utama">
                          {k.kode}
                        </td>
                        <td className="py-3 px-3">
                          <input
                            type="text"
                            value={k.nama}
                            onChange={(e) => handleNamaChange(k.id, e.target.value)}
                            className="w-full p-1.5 bg-latar-soft border border-hijau-muda rounded text-xs font-semibold text-teks-utama"
                          />
                        </td>
                        <td className="py-3 px-3 text-center">
                          <span className="font-semibold text-[11px] text-teks-utama">
                            {k.jenis}
                          </span>
                        </td>
                        <td className="py-3 px-3 text-center">
                          <div className="flex items-center justify-center gap-1.5">
                            <input
                              type="number"
                              min={1}
                              max={100}
                              value={persenVal}
                              onChange={(e) => handleBobotChange(k.id, Number(e.target.value))}
                              className="w-20 p-1.5 text-center bg-latar-soft border border-hijau-muda rounded text-xs font-bold text-teks-utama"
                            />
                            <span className="font-semibold text-teks-sekunder">%</span>
                          </div>
                        </td>
                        <td className="py-3 px-3 text-center font-mono font-bold text-hijau-utama">
                          {(persenVal / 100).toFixed(2)}
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
