'use client';

import React, { useState, useEffect } from 'react';
import AppLayout from '@/components/dashboard/AppLayout';
import { Edit2, Save, X, CheckCircle2 } from 'lucide-react';

interface SkalaItem {
  id: string;
  nilai: number;
  label: string;
  keterangan: string | null;
}

export default function AdminSkalaPenilaianPage() {
  const [skalaList, setSkalaList] = useState<SkalaItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [editItem, setEditItem] = useState<SkalaItem | null>(null);
  const [labelInput, setLabelInput] = useState('');
  const [ketInput, setKetInput] = useState('');
  const [saving, setSaving] = useState(false);
  const [successMsg, setSuccessMsg] = useState('');

  const fetchSkala = async () => {
    setLoading(true);
    try {
      const res = await fetch('/api/skala');
      const data = await res.json();
      setSkalaList(data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchSkala();
  }, []);

  const handleOpenEdit = (item: SkalaItem) => {
    setEditItem(item);
    setLabelInput(item.label);
    setKetInput(item.keterangan || '');
    setSuccessMsg('');
  };

  const handleSimpanEdit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!editItem) return;

    setSaving(true);
    try {
      const res = await fetch('/api/skala', {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          id: editItem.id,
          label: labelInput,
          keterangan: ketInput,
        }),
      });

      const data = await res.json();
      if (!res.ok) throw new Error(data.error || 'Gagal menyimpan skala');

      setSuccessMsg(`Skala nilai ${editItem.nilai} berhasil diperbarui.`);
      setEditItem(null);
      fetchSkala();
    } catch (e: any) {
      alert(e.message || 'Terjadi kesalahan');
    } finally {
      setSaving(false);
    }
  };

  return (
    <AppLayout
      title="Skala Penilaian (Likert 1-5)"
      subtitle="Standar tingkatan skor evaluasi kinerja guru SMA Al-Ihsan Boarding School"
      user={{ nama: 'Administrator SPK', username: 'admin', role: 'ADMIN' }}
    >
      <div className="space-y-6">
        {successMsg && (
          <div className="p-3 rounded-lg bg-emerald-50 text-emerald-800 border border-emerald-200 text-xs flex items-center gap-2">
            <CheckCircle2 className="w-4 h-4 shrink-0" />
            <span>{successMsg}</span>
          </div>
        )}

        {/* Tabel Skala Penilaian */}
        <div className="bg-white rounded-xl border border-hijau-muda overflow-hidden">
          <div className="p-4 border-b border-hijau-muda">
            <h3 className="font-semibold text-sm text-teks-utama">Daftar Skala Likert 1 sampai 5</h3>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-hijau-soft border-b border-hijau-muda text-teks-utama font-semibold">
                <tr>
                  <th className="py-2.5 px-3 text-center w-16">Nilai</th>
                  <th className="py-2.5 px-3 w-48">Label Predikat</th>
                  <th className="py-2.5 px-3">Deskripsi / Keterangan</th>
                  <th className="py-2.5 px-3 text-center w-24">Aksi</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-hijau-muda/50 text-teks-utama">
                {loading ? (
                  <tr>
                    <td colSpan={4} className="py-8 text-center text-teks-sekunder">
                      Memuat skala penilaian...
                    </td>
                  </tr>
                ) : (
                  skalaList.map((item) => (
                    <tr key={item.id} className="hover:bg-hijau-soft/40 transition-colors">
                      <td className="py-2.5 px-3 text-center">
                        <span className="inline-flex items-center justify-center w-7 h-7 rounded-lg bg-hijau-soft border border-hijau-muda font-bold text-xs text-hijau-utama">
                          {item.nilai}
                        </span>
                      </td>
                      <td className="py-2.5 px-3 font-semibold">{item.label}</td>
                      <td className="py-2.5 px-3 text-teks-sekunder">{item.keterangan || '-'}</td>
                      <td className="py-2.5 px-3 text-center">
                        <button
                          onClick={() => handleOpenEdit(item)}
                          className="px-2.5 py-1 text-xs text-teks-utama hover:bg-hijau-soft border border-hijau-muda rounded inline-flex items-center gap-1"
                        >
                          <Edit2 className="w-3.5 h-3.5 text-hijau-utama" />
                          <span>Edit</span>
                        </button>
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </div>

        {/* Modal Edit Skala */}
        {editItem && (
          <div className="fixed inset-0 z-50 bg-black/40 flex items-center justify-center p-4">
            <div className="bg-white rounded-xl border border-hijau-muda shadow-lg max-w-md w-full p-5 space-y-4 text-xs">
              <div className="flex items-center justify-between border-b border-hijau-muda pb-3">
                <h3 className="font-semibold text-sm text-teks-utama">
                  Edit Skala Nilai: {editItem.nilai}
                </h3>
                <button
                  onClick={() => setEditItem(null)}
                  className="p-1 text-teks-sekunder hover:text-teks-utama rounded"
                >
                  <X className="w-4 h-4" />
                </button>
              </div>

              <form onSubmit={handleSimpanEdit} className="space-y-3">
                <div>
                  <label className="block font-medium text-teks-utama mb-1">Label Predikat:</label>
                  <input
                    type="text"
                    value={labelInput}
                    onChange={(e) => setLabelInput(e.target.value)}
                    className="w-full p-2 bg-latar-soft border border-hijau-muda rounded-lg text-xs"
                    required
                  />
                </div>

                <div>
                  <label className="block font-medium text-teks-utama mb-1">Deskripsi Keterangan:</label>
                  <textarea
                    rows={3}
                    value={ketInput}
                    onChange={(e) => setKetInput(e.target.value)}
                    className="w-full p-2 bg-latar-soft border border-hijau-muda rounded-lg text-xs"
                  />
                </div>

                <div className="flex justify-end gap-2 pt-3 border-t border-hijau-muda">
                  <button
                    type="button"
                    onClick={() => setEditItem(null)}
                    className="px-4 py-2 bg-latar-soft hover:bg-gray-100 rounded-lg text-xs font-semibold text-teks-sekunder"
                  >
                    Batal
                  </button>
                  <button
                    type="submit"
                    disabled={saving}
                    className="px-4 py-2 bg-hijau-utama hover:bg-hijau-hover text-white rounded-lg text-xs font-semibold flex items-center gap-1.5"
                  >
                    <Save className="w-3.5 h-3.5" />
                    <span>{saving ? 'Menyimpan...' : 'Simpan'}</span>
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
