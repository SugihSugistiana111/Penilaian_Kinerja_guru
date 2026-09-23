'use client';

import React, { useState, useEffect } from 'react';
import AppLayout from '@/components/dashboard/AppLayout';
import {
  CalendarDays,
  Plus,
  CheckCircle,
  AlertCircle,
  X,
} from 'lucide-react';

interface PeriodeItem {
  id: string;
  bulan: string;
  tahun: number;
  namaPeriode: string;
  status: 'DRAFT' | 'AKTIF' | 'SELESAI';
  createdAt: string;
  _count?: {
    penilaian: number;
    hasilMoora: number;
  };
}

export default function AdminPeriodePage() {
  const [periodeList, setPeriodeList] = useState<PeriodeItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [bulanInput, setBulanInput] = useState('Juli');
  const [tahunInput, setTahunInput] = useState(2026);
  const [setAktifInput, setSetAktifInput] = useState(true);
  const [errorMsg, setErrorMsg] = useState('');
  const [successMsg, setSuccessMsg] = useState('');

  const daftarBulan = [
    'Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni',
    'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember'
  ];

  const fetchPeriode = async () => {
    setLoading(true);
    try {
      const res = await fetch('/api/periode');
      const data = await res.json();
      setPeriodeList(data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchPeriode();
  }, []);

  const handleCreatePeriode = async (e: React.FormEvent) => {
    e.preventDefault();
    setErrorMsg('');
    setSuccessMsg('');

    try {
      const res = await fetch('/api/periode', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          bulan: bulanInput,
          tahun: Number(tahunInput),
          setAktif: setAktifInput,
        }),
      });

      const data = await res.json();
      if (!res.ok) throw new Error(data.error || 'Gagal membuat periode');

      setSuccessMsg(`Periode ${data.namaPeriode} berhasil ditambahkan.`);
      setIsModalOpen(false);
      fetchPeriode();
    } catch (err: any) {
      setErrorMsg(err.message || 'Terjadi kesalahan');
    }
  };

  const handleUpdateStatus = async (periode: PeriodeItem, newStatus: 'DRAFT' | 'AKTIF' | 'SELESAI') => {
    const confirm = window.confirm(
      `Ubah status periode ${periode.namaPeriode} menjadi ${newStatus}?`
    );
    if (!confirm) return;

    try {
      const res = await fetch(`/api/periode/${periode.id}`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ status: newStatus }),
      });

      const data = await res.json();
      if (!res.ok) throw new Error(data.error || 'Gagal mengubah status');

      fetchPeriode();
    } catch (err: any) {
      alert(err.message || 'Terjadi kesalahan');
    }
  };

  return (
    <AppLayout
      title="Periode Penilaian"
      subtitle="Manajemen siklus evaluasi berkala guru SMA Al-Ihsan Boarding School"
      user={{ nama: 'Administrator SPK', username: 'admin', role: 'ADMIN' }}
    >
      <div className="space-y-6">
        {/* Toolbar */}
        <div className="p-4 bg-white rounded-xl border border-hijau-muda flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div className="text-xs text-teks-sekunder">
            Aturan Sistem: <strong className="text-teks-utama">Hanya boleh terdapat 1 periode berstatus AKTIF</strong> pada satu waktu.
          </div>

          <button
            onClick={() => {
              setErrorMsg('');
              setIsModalOpen(true);
            }}
            className="px-3.5 py-1.5 bg-hijau-utama hover:bg-hijau-hover text-white rounded-lg text-xs font-semibold flex items-center justify-center gap-1.5 transition-colors self-start sm:self-auto"
          >
            <Plus className="w-3.5 h-3.5" />
            <span>Tambah Periode Baru</span>
          </button>
        </div>

        {successMsg && (
          <div className="p-3 rounded-lg bg-emerald-50 text-emerald-800 border border-emerald-200 text-xs flex items-center gap-2">
            <CheckCircle className="w-4 h-4 shrink-0" />
            <span>{successMsg}</span>
          </div>
        )}

        {/* Tabel Periode */}
        <div className="bg-white rounded-xl border border-hijau-muda overflow-hidden">
          <div className="p-4 border-b border-hijau-muda">
            <h3 className="font-semibold text-sm text-teks-utama">Daftar Siklus Periode Penilaian</h3>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-hijau-soft border-b border-hijau-muda text-teks-utama font-semibold">
                <tr>
                  <th className="py-2.5 px-3 text-center w-12">No</th>
                  <th className="py-2.5 px-3">Nama Periode</th>
                  <th className="py-2.5 px-3">Bulan & Tahun</th>
                  <th className="py-2.5 px-3 text-center">Data Dinilai</th>
                  <th className="py-2.5 px-3 text-center">Status Periode</th>
                  <th className="py-2.5 px-3 text-center w-56">Ubah Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-hijau-muda/50 text-teks-utama">
                {loading ? (
                  <tr>
                    <td colSpan={6} className="py-8 text-center text-teks-sekunder">
                      Memuat data periode...
                    </td>
                  </tr>
                ) : periodeList.length === 0 ? (
                  <tr>
                    <td colSpan={6} className="py-8 text-center text-teks-sekunder">
                      Belum ada periode yang dibuat.
                    </td>
                  </tr>
                ) : (
                  periodeList.map((p, idx) => (
                    <tr key={p.id} className="hover:bg-hijau-soft/40 transition-colors">
                      <td className="py-2.5 px-3 text-center font-medium text-teks-sekunder">{idx + 1}</td>
                      <td className="py-2.5 px-3 font-semibold">{p.namaPeriode}</td>
                      <td className="py-2.5 px-3 text-teks-sekunder">{p.bulan} {p.tahun}</td>
                      <td className="py-2.5 px-3 text-center font-medium">
                        {p._count?.penilaian || 0} Penilaian
                      </td>
                      <td className="py-2.5 px-3 text-center">
                        <span
                          className={`inline-block px-2.5 py-0.5 rounded text-[11px] font-semibold ${
                            p.status === 'AKTIF'
                              ? 'bg-emerald-100 text-emerald-800'
                              : p.status === 'SELESAI'
                              ? 'bg-blue-100 text-blue-800'
                              : 'bg-gray-100 text-gray-800'
                          }`}
                        >
                          {p.status}
                        </span>
                      </td>
                      <td className="py-2.5 px-3 text-center">
                        <div className="flex items-center justify-center gap-1">
                          {p.status !== 'AKTIF' && (
                            <button
                              onClick={() => handleUpdateStatus(p, 'AKTIF')}
                              className="px-2 py-1 bg-emerald-50 hover:bg-emerald-100 text-emerald-800 border border-emerald-200 rounded text-[11px] font-semibold"
                            >
                              Set Aktif
                            </button>
                          )}
                          {p.status !== 'SELESAI' && (
                            <button
                              onClick={() => handleUpdateStatus(p, 'SELESAI')}
                              className="px-2 py-1 bg-blue-50 hover:bg-blue-100 text-blue-800 border border-blue-200 rounded text-[11px] font-semibold"
                            >
                              Set Selesai
                            </button>
                          )}
                          {p.status !== 'DRAFT' && (
                            <button
                              onClick={() => handleUpdateStatus(p, 'DRAFT')}
                              className="px-2 py-1 bg-gray-50 hover:bg-gray-100 text-gray-700 border border-gray-200 rounded text-[11px] font-medium"
                            >
                              Draft
                            </button>
                          )}
                        </div>
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </div>

        {/* Modal Tambah Periode */}
        {isModalOpen && (
          <div className="fixed inset-0 z-50 bg-black/40 flex items-center justify-center p-4">
            <div className="bg-white rounded-xl border border-hijau-muda shadow-lg max-w-md w-full p-5 space-y-4 text-xs">
              <div className="flex items-center justify-between border-b border-hijau-muda pb-3">
                <h3 className="font-semibold text-sm text-teks-utama">Tambah Periode Penilaian</h3>
                <button
                  onClick={() => setIsModalOpen(false)}
                  className="p-1 text-teks-sekunder hover:text-teks-utama rounded"
                >
                  <X className="w-4 h-4" />
                </button>
              </div>

              {errorMsg && (
                <div className="p-2.5 rounded-lg bg-red-50 text-red-700 border border-red-200">
                  {errorMsg}
                </div>
              )}

              <form onSubmit={handleCreatePeriode} className="space-y-3">
                <div>
                  <label className="block font-medium text-teks-utama mb-1">Bulan:</label>
                  <select
                    value={bulanInput}
                    onChange={(e) => setBulanInput(e.target.value)}
                    className="w-full p-2 bg-latar-soft border border-hijau-muda rounded-lg text-xs"
                  >
                    {daftarBulan.map((b) => (
                      <option key={b} value={b}>{b}</option>
                    ))}
                  </select>
                </div>

                <div>
                  <label className="block font-medium text-teks-utama mb-1">Tahun:</label>
                  <input
                    type="number"
                    min={2020}
                    max={2040}
                    value={tahunInput}
                    onChange={(e) => setTahunInput(Number(e.target.value))}
                    className="w-full p-2 bg-latar-soft border border-hijau-muda rounded-lg text-xs"
                    required
                  />
                </div>

                <div className="pt-1">
                  <label className="flex items-center gap-2 cursor-pointer">
                    <input
                      type="checkbox"
                      checked={setAktifInput}
                      onChange={(e) => setSetAktifInput(e.target.checked)}
                      className="rounded text-hijau-utama"
                    />
                    <span>Jadikan periode aktif sekarang (otomatis mengubah periode lain menjadi DRAFT/SELESAI)</span>
                  </label>
                </div>

                <div className="flex justify-end gap-2 pt-3 border-t border-hijau-muda">
                  <button
                    type="button"
                    onClick={() => setIsModalOpen(false)}
                    className="px-4 py-2 bg-latar-soft hover:bg-gray-100 rounded-lg text-xs font-semibold text-teks-sekunder"
                  >
                    Batal
                  </button>
                  <button
                    type="submit"
                    className="px-4 py-2 bg-hijau-utama hover:bg-hijau-hover text-white rounded-lg text-xs font-semibold"
                  >
                    Simpan Periode
                  </button>
                </div>
              </form>
            </div>
          </div>
        )}
      </div>
    </AppLayout>
  );
}
