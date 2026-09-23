'use client';

import React, { useState, useEffect } from 'react';
import AppLayout from '@/components/dashboard/AppLayout';
import {
  ClipboardCheck,
  CheckCircle,
  AlertCircle,
  Save,
  User,
  Calendar,
} from 'lucide-react';

interface GuruStatusItem {
  guruId: string;
  nip: string;
  nama: string;
  jabatan: string;
  jamAjar: number;
  sudahDinilai: boolean;
  penilaianId?: string;
  catatan?: string;
  nilaiPerKriteria: Record<string, number>;
}

interface KriteriaItem {
  id: string;
  kode: string;
  nama: string;
  bobot: number;
}

interface PeriodeItem {
  id: string;
  namaPeriode: string;
  status: string;
}

export default function KepsekPenilaianPage() {
  const [periodeList, setPeriodeList] = useState<PeriodeItem[]>([]);
  const [selectedPeriodeId, setSelectedPeriodeId] = useState<string>('');
  const [kriteriaList, setKriteriaList] = useState<KriteriaItem[]>([]);
  const [rekapGuru, setRekapGuru] = useState<GuruStatusItem[]>([]);
  const [selectedGuru, setSelectedGuru] = useState<GuruStatusItem | null>(null);
  const [skorForm, setSkorForm] = useState<Record<string, number>>({});
  const [catatanForm, setCatatanForm] = useState('');
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
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

  const loadData = async () => {
    if (!selectedPeriodeId) return;
    setLoading(true);
    try {
      const [kritRes, penRes] = await Promise.all([
        fetch('/api/kriteria'),
        fetch(`/api/penilaian?periodeId=${selectedPeriodeId}`),
      ]);

      const kritData: KriteriaItem[] = await kritRes.json();
      const penData = await penRes.json();

      setKriteriaList(kritData);
      setRekapGuru(penData.rekap || []);

      if (penData.rekap?.length > 0 && !selectedGuru) {
        const first = penData.rekap[0];
        setSelectedGuru(first);
        const skorByKode = first.nilaiPerKriteria || {};
        const skorById: Record<string, number> = {};
        kritData.forEach((k: KriteriaItem) => {
          if (skorByKode[k.kode]) skorById[k.id] = skorByKode[k.kode];
        });
        setSkorForm(skorById);
        setCatatanForm(first.catatan || '');
      } else if (selectedGuru) {
        const updated = penData.rekap.find((g: any) => g.guruId === selectedGuru.guruId);
        if (updated) {
          setSelectedGuru(updated);
          const skorByKode = updated.nilaiPerKriteria || {};
          const skorById: Record<string, number> = {};
          kritData.forEach((k: KriteriaItem) => {
            if (skorByKode[k.kode]) skorById[k.id] = skorByKode[k.kode];
          });
          setSkorForm(skorById);
          setCatatanForm(updated.catatan || '');
        }
      }
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, [selectedPeriodeId]);

  const handleSelectGuru = (guru: GuruStatusItem) => {
    setSelectedGuru(guru);
    // Konversi nilaiPerKriteria (by kode) → skorForm (by ID)
    const skorByKode = guru.nilaiPerKriteria || {};
    const skorById: Record<string, number> = {};
    kriteriaList.forEach((k) => {
      if (skorByKode[k.kode]) skorById[k.id] = skorByKode[k.kode];
    });
    setSkorForm(skorById);
    setCatatanForm(guru.catatan || '');
    setFeedback(null);
  };

  const handleSave = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedGuru || !selectedPeriodeId) return;

    for (const k of kriteriaList) {
      if (!skorForm[k.id] || skorForm[k.id] < 1 || skorForm[k.id] > 5) {
        setFeedback({
          type: 'error',
          text: `Skor untuk kriteria ${k.kode} (${k.nama}) wajib diisi skala 1-5.`,
        });
        return;
      }
    }

    setSaving(true);
    setFeedback(null);

    try {
      const payload = {
        periodeId: selectedPeriodeId,
        guruId: selectedGuru.guruId,
        dinilaiOleh: 'Dr. H. Mulyadi, M.Pd. (Kepala Sekolah)',
        catatan: catatanForm,
        skor: kriteriaList.map((k) => ({
          kriteriaId: k.id,
          nilai: Number(skorForm[k.id]),
        })),
      };

      const res = await fetch('/api/penilaian', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });

      const json = await res.json();
      if (!res.ok) throw new Error(json.error || 'Gagal menyimpan penilaian');

      setFeedback({ type: 'success', text: `Penilaian untuk ${selectedGuru.nama} berhasil disimpan.` });
      await loadData();
    } catch (err: any) {
      setFeedback({ type: 'error', text: err.message || 'Terjadi kesalahan' });
    } finally {
      setSaving(false);
    }
  };

  const dinilaiCount = rekapGuru.filter((g) => g.sudahDinilai).length;

  return (
    <AppLayout
      title="Penilaian Kinerja Guru"
      subtitle="Pengisian skor evaluasi 4 kriteria berkala oleh Kepala Sekolah"
      user={{ nama: 'Dr. H. Mulyadi, M.Pd.', username: 'kepsek', role: 'KEPALA_SEKOLAH' }}
    >
      <div className="space-y-6">
        {/* Periode & Status Ringkas */}
        <div className="p-4 bg-white rounded-xl border border-hijau-muda flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div className="flex items-center gap-3">
            <Calendar className="w-4 h-4 text-hijau-utama" />
            <label className="text-xs font-semibold text-teks-utama">Periode Penilaian:</label>
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

          <div className="text-xs text-teks-sekunder">
            Progress: <strong className="text-teks-utama">{dinilaiCount} dari {rekapGuru.length} guru</strong> telah dinilai
          </div>
        </div>

        {/* Form & Daftar Guru (2 Kolom) */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
          {/* Kolom Kiri: Daftar 18 Guru (4 Kolom Grid) */}
          <div className="lg:col-span-4 bg-white rounded-xl border border-hijau-muda overflow-hidden flex flex-col h-[560px]">
            <div className="p-3 border-b border-hijau-muda bg-hijau-soft flex items-center justify-between">
              <h3 className="font-semibold text-xs text-teks-utama uppercase tracking-wider">
                Daftar Guru ({rekapGuru.length})
              </h3>
              <span className="text-[11px] text-teks-sekunder">Pilih guru untuk dinilai</span>
            </div>

            <div className="flex-1 overflow-y-auto divide-y divide-hijau-muda/40">
              {loading ? (
                <div className="p-6 text-center text-xs text-teks-sekunder">Memuat data guru...</div>
              ) : (
                rekapGuru.map((g) => {
                  const isSelected = selectedGuru?.guruId === g.guruId;
                  return (
                    <button
                      key={g.guruId}
                      onClick={() => handleSelectGuru(g)}
                      className={`w-full text-left p-3 transition-colors flex items-center justify-between ${
                        isSelected
                          ? 'bg-hijau-muda/70 border-l-4 border-hijau-utama'
                          : 'hover:bg-hijau-soft/40'
                      }`}
                    >
                      <div className="min-w-0 pr-2">
                        <p className="text-xs font-semibold text-teks-utama truncate">{g.nama}</p>
                        <p className="text-[11px] text-teks-sekunder truncate">{g.jabatan}</p>
                      </div>

                      <span
                        className={`text-[10px] font-semibold px-2 py-0.5 rounded ${
                          g.sudahDinilai
                            ? 'bg-emerald-100 text-emerald-800'
                            : 'bg-gray-100 text-gray-600'
                        }`}
                      >
                        {g.sudahDinilai ? 'Sudah Dinilai' : 'Belum'}
                      </span>
                    </button>
                  );
                })
              )}
            </div>
          </div>

          {/* Kolom Kanan: Form Penilaian Bersih & Terstruktur (8 Kolom Grid) */}
          <div className="lg:col-span-8 bg-white rounded-xl border border-hijau-muda p-6 space-y-6">
            {!selectedGuru ? (
              <div className="p-12 text-center text-xs text-teks-sekunder">
                Silakan pilih guru di panel sebelah kiri untuk memulai penilaian.
              </div>
            ) : (
              <form onSubmit={handleSave} className="space-y-6">
                {/* Header Data Guru */}
                <div className="pb-4 border-b border-hijau-muda">
                  <h3 className="font-semibold text-base text-teks-utama">{selectedGuru.nama}</h3>
                  <div className="grid grid-cols-2 sm:grid-cols-3 gap-2 mt-2 text-xs text-teks-sekunder">
                    <p><span className="text-teks-utama font-medium">NIP:</span> {selectedGuru.nip}</p>
                    <p><span className="text-teks-utama font-medium">Mata Pelajaran:</span> {selectedGuru.jabatan}</p>
                    <p><span className="text-teks-utama font-medium">Beban Ajar:</span> {selectedGuru.jamAjar} Jam/Minggu</p>
                  </div>
                </div>

                {feedback && (
                  <div
                    className={`p-3 rounded-lg text-xs font-medium flex items-center gap-2 ${
                      feedback.type === 'success'
                        ? 'bg-emerald-50 text-emerald-800 border border-emerald-200'
                        : 'bg-red-50 text-red-800 border border-red-200'
                    }`}
                  >
                    {feedback.type === 'success' ? (
                      <CheckCircle className="w-4 h-4 shrink-0" />
                    ) : (
                      <AlertCircle className="w-4 h-4 shrink-0" />
                    )}
                    <span>{feedback.text}</span>
                  </div>
                )}

                {/* 4 Kriteria Penilaian Skala Likert 1-5 */}
                <div className="space-y-4">
                  <h4 className="font-semibold text-xs text-teks-utama uppercase tracking-wider">
                    Nilai 4 Kriteria Evaluasi
                  </h4>

                  {kriteriaList.map((k) => (
                    <div
                      key={k.id}
                      className="p-3.5 bg-latar-soft rounded-lg border border-hijau-muda/60 flex flex-col sm:flex-row sm:items-center justify-between gap-3"
                    >
                      <div>
                        <div className="flex items-center gap-2">
                          <span className="font-bold text-xs text-hijau-utama">{k.kode}</span>
                          <span className="font-semibold text-xs text-teks-utama">{k.nama}</span>
                        </div>
                        <p className="text-[11px] text-teks-sekunder mt-0.5">
                          Bobot: {(k.bobot * 100).toFixed(0)}% (Benefit)
                        </p>
                      </div>

                      {/* Skala Pilihan 1 - 5 */}
                      <div className="flex items-center gap-2">
                        {[1, 2, 3, 4, 5].map((val) => (
                          <label
                            key={val}
                            className={`flex flex-col items-center justify-center w-10 h-10 rounded-lg cursor-pointer text-xs font-bold border transition-colors ${
                              skorForm[k.id] === val
                                ? 'bg-hijau-utama text-white border-hijau-utama shadow-sm'
                                : 'bg-white text-teks-utama border-hijau-muda hover:bg-hijau-soft'
                            }`}
                          >
                            <input
                              type="radio"
                              name={`kriteria-${k.id}`}
                              value={val}
                              checked={skorForm[k.id] === val}
                              onChange={() =>
                                setSkorForm((prev) => ({ ...prev, [k.id]: val }))
                              }
                              className="sr-only"
                            />
                            <span>{val}</span>
                          </label>
                        ))}
                      </div>
                    </div>
                  ))}
                </div>

                {/* Catatan Evaluator */}
                <div className="space-y-1.5">
                  <label className="block text-xs font-semibold text-teks-utama">
                    Catatan & Rekomendasi Evaluator:
                  </label>
                  <textarea
                    value={catatanForm}
                    onChange={(e) => setCatatanForm(e.target.value)}
                    rows={3}
                    placeholder="Tuliskan catatan evaluasi kinerja untuk guru bersangkutan..."
                    className="w-full p-3 bg-latar-soft border border-hijau-muda rounded-lg text-xs text-teks-utama focus:ring-2 focus:ring-hijau-utama focus:bg-white transition-all"
                  />
                </div>

                {/* Tombol Simpan */}
                <div className="flex justify-end pt-2">
                  <button
                    type="submit"
                    disabled={saving}
                    className="px-6 py-2.5 bg-hijau-utama hover:bg-hijau-hover text-white text-xs font-semibold rounded-lg flex items-center gap-2 transition-colors disabled:opacity-50"
                  >
                    <Save className="w-4 h-4" />
                    <span>{saving ? 'Menyimpan Penilaian...' : 'Simpan Penilaian'}</span>
                  </button>
                </div>
              </form>
            )}
          </div>
        </div>
      </div>
    </AppLayout>
  );
}
