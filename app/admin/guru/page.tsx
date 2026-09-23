'use client';

import React, { useState, useEffect } from 'react';
import AppLayout from '@/components/dashboard/AppLayout';
import {
  GraduationCap,
  Plus,
  Search,
  Edit2,
  CheckCircle,
  XCircle,
  Eye,
  X,
} from 'lucide-react';

interface GuruData {
  id: string;
  nip: string;
  nama: string;
  jenisKelamin: string;
  jabatanTugasMengajar: string;
  tugasTambahanUtama?: string | null;
  tugasTambahanLain?: string | null;
  jumlahSiswaPerRombel: number;
  jumlahJamAjar: number;
  mengajarKelas10: boolean;
  mengajarKelas11: boolean;
  mengajarKelas12: boolean;
  statusAktif: boolean;
}

export default function AdminDataGuruPage() {
  const [daftarGuru, setDaftarGuru] = useState<GuruData[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [filterKelas, setFilterKelas] = useState<string>('all');
  const [filterStatus, setFilterStatus] = useState<string>('all');

  // Modal State
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isDetailModalOpen, setIsDetailModalOpen] = useState(false);
  const [selectedGuru, setSelectedGuru] = useState<GuruData | null>(null);
  const [isEditing, setIsEditing] = useState(false);
  const [formData, setFormData] = useState<Partial<GuruData>>({
    nip: '',
    nama: '',
    jenisKelamin: 'L',
    jabatanTugasMengajar: '',
    tugasTambahanUtama: '',
    tugasTambahanLain: '',
    jumlahSiswaPerRombel: 30,
    jumlahJamAjar: 24,
    mengajarKelas10: true,
    mengajarKelas11: false,
    mengajarKelas12: false,
    statusAktif: true,
  });

  const [saving, setSaving] = useState(false);
  const [errorMsg, setErrorMsg] = useState('');

  const fetchGuru = async () => {
    setLoading(true);
    try {
      const res = await fetch('/api/guru');
      const data = await res.json();
      setDaftarGuru(data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchGuru();
  }, []);

  const handleOpenCreateModal = () => {
    setIsEditing(false);
    setFormData({
      nip: '',
      nama: '',
      jenisKelamin: 'L',
      jabatanTugasMengajar: '',
      tugasTambahanUtama: '',
      tugasTambahanLain: '',
      jumlahSiswaPerRombel: 30,
      jumlahJamAjar: 24,
      mengajarKelas10: true,
      mengajarKelas11: false,
      mengajarKelas12: false,
      statusAktif: true,
    });
    setErrorMsg('');
    setIsModalOpen(true);
  };

  const handleOpenEditModal = (guru: GuruData) => {
    setIsEditing(true);
    setSelectedGuru(guru);
    setFormData({ ...guru });
    setErrorMsg('');
    setIsModalOpen(true);
  };

  const handleOpenDetailModal = (guru: GuruData) => {
    setSelectedGuru(guru);
    setIsDetailModalOpen(true);
  };

  const handleSave = async (e: React.FormEvent) => {
    e.preventDefault();
    setSaving(true);
    setErrorMsg('');

    try {
      const url = isEditing ? `/api/guru/${selectedGuru?.id}` : '/api/guru';
      const method = isEditing ? 'PUT' : 'POST';

      const res = await fetch(url, {
        method,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData),
      });

      const data = await res.json();
      if (!res.ok) throw new Error(data.error || 'Gagal menyimpan data guru');

      setIsModalOpen(false);
      fetchGuru();
    } catch (err: any) {
      setErrorMsg(err.message || 'Terjadi kesalahan');
    } finally {
      setSaving(false);
    }
  };

  const handleToggleStatus = async (guru: GuruData) => {
    const confirm = window.confirm(
      `Apakah Anda yakin ingin ${guru.statusAktif ? 'menonaktifkan' : 'mengaktifkan'} ${guru.nama}?`
    );
    if (!confirm) return;

    try {
      const res = await fetch(`/api/guru/${guru.id}`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ statusAktif: !guru.statusAktif }),
      });

      if (!res.ok) throw new Error('Gagal memperbarui status guru');
      fetchGuru();
    } catch (e) {
      console.error(e);
      alert('Terjadi kesalahan saat memperbarui status.');
    }
  };

  const filteredList = daftarGuru.filter((g) => {
    const matchSearch =
      g.nama.toLowerCase().includes(search.toLowerCase()) ||
      g.nip.includes(search) ||
      g.jabatanTugasMengajar.toLowerCase().includes(search.toLowerCase());

    const matchKelas =
      filterKelas === 'all'
        ? true
        : filterKelas === '10'
        ? g.mengajarKelas10
        : filterKelas === '11'
        ? g.mengajarKelas11
        : filterKelas === '12'
        ? g.mengajarKelas12
        : true;

    const matchStatus =
      filterStatus === 'all'
        ? true
        : filterStatus === 'aktif'
        ? g.statusAktif
        : !g.statusAktif;

    return matchSearch && matchKelas && matchStatus;
  });

  return (
    <AppLayout
      title="Data Master Guru"
      subtitle="Manajemen data 18 tenaga pendidik SMA Al-Ihsan Boarding School"
      user={{ nama: 'Administrator SPK', username: 'admin', role: 'ADMIN' }}
    >
      <div className="space-y-6">
        {/* Toolbar Pencarian & Filter */}
        <div className="p-4 bg-white rounded-xl border border-hijau-muda flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-3">
          <div className="flex flex-wrap items-center gap-2">
            <div className="relative min-w-[200px]">
              <Search className="w-3.5 h-3.5 absolute left-3 top-1/2 -translate-y-1/2 text-teks-sekunder" />
              <input
                type="text"
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                placeholder="Cari guru, NIP, mapel..."
                className="w-full pl-8 pr-3 py-1.5 bg-latar-soft border border-hijau-muda rounded-lg text-xs text-teks-utama focus:ring-2 focus:ring-hijau-utama"
              />
            </div>

            <select
              value={filterKelas}
              onChange={(e) => setFilterKelas(e.target.value)}
              className="px-3 py-1.5 bg-latar-soft border border-hijau-muda rounded-lg text-xs font-medium text-teks-utama focus:ring-2 focus:ring-hijau-utama"
            >
              <option value="all">Semua Kelas</option>
              <option value="10">Kelas 10</option>
              <option value="11">Kelas 11</option>
              <option value="12">Kelas 12</option>
            </select>

            <select
              value={filterStatus}
              onChange={(e) => setFilterStatus(e.target.value)}
              className="px-3 py-1.5 bg-latar-soft border border-hijau-muda rounded-lg text-xs font-medium text-teks-utama focus:ring-2 focus:ring-hijau-utama"
            >
              <option value="all">Semua Status</option>
              <option value="aktif">Aktif</option>
              <option value="nonaktif">Nonaktif</option>
            </select>
          </div>

          <button
            onClick={handleOpenCreateModal}
            className="px-3.5 py-1.5 bg-hijau-utama hover:bg-hijau-hover text-white rounded-lg text-xs font-semibold flex items-center justify-center gap-1.5 transition-colors"
          >
            <Plus className="w-3.5 h-3.5" />
            <span>Tambah Data Guru</span>
          </button>
        </div>

        {/* Tabel Data Guru (Desktop) */}
        <div className="bg-white rounded-xl border border-hijau-muda overflow-hidden">
          <div className="p-4 border-b border-hijau-muda flex items-center justify-between">
            <h3 className="font-semibold text-sm text-teks-utama">Daftar Guru Terdaftar</h3>
            <span className="text-xs text-teks-sekunder">Total: {filteredList.length} Guru</span>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-hijau-soft border-b border-hijau-muda text-teks-utama font-semibold">
                <tr>
                  <th className="py-2.5 px-3 text-center w-10">No</th>
                  <th className="py-2.5 px-3 min-w-[180px]">Nama Guru & NIP</th>
                  <th className="py-2.5 px-2 text-center w-12">L/P</th>
                  <th className="py-2.5 px-3 min-w-[150px]">Mata Pelajaran</th>
                  <th className="py-2.5 px-3 min-w-[130px]">Tugas Tambahan</th>
                  <th className="py-2.5 px-2 text-center">Beban Jam</th>
                  <th className="py-2.5 px-2 text-center">Rombel</th>
                  <th className="py-2.5 px-2 text-center">Kelas</th>
                  <th className="py-2.5 px-2 text-center">Status</th>
                  <th className="py-2.5 px-3 text-center w-28">Aksi</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-hijau-muda/50 text-teks-utama">
                {loading ? (
                  <tr>
                    <td colSpan={10} className="py-8 text-center text-teks-sekunder">
                      Memuat daftar guru...
                    </td>
                  </tr>
                ) : filteredList.length === 0 ? (
                  <tr>
                    <td colSpan={10} className="py-8 text-center text-teks-sekunder">
                      Tidak ada data guru yang cocok.
                    </td>
                  </tr>
                ) : (
                  filteredList.map((g, idx) => (
                    <tr key={g.id} className="hover:bg-hijau-soft/40 transition-colors">
                      <td className="py-2.5 px-3 text-center font-medium text-teks-sekunder">
                        {idx + 1}
                      </td>
                      <td className="py-2.5 px-3">
                        <div className="font-semibold">{g.nama}</div>
                        <div className="text-[10px] font-mono text-teks-sekunder">{g.nip}</div>
                      </td>
                      <td className="py-2.5 px-2 text-center font-medium">{g.jenisKelamin}</td>
                      <td className="py-2.5 px-3 text-teks-sekunder">{g.jabatanTugasMengajar}</td>
                      <td className="py-2.5 px-3 text-teks-sekunder">
                        {g.tugasTambahanUtama || '-'}
                      </td>
                      <td className="py-2.5 px-2 text-center font-medium">{g.jumlahJamAjar} Jam</td>
                      <td className="py-2.5 px-2 text-center font-medium">{g.jumlahSiswaPerRombel}</td>
                      <td className="py-2.5 px-2 text-center">
                        <div className="flex items-center justify-center gap-1 text-[10px]">
                          <span className={g.mengajarKelas10 ? 'font-bold text-hijau-utama' : 'text-gray-300'}>10</span>
                          <span className={g.mengajarKelas11 ? 'font-bold text-hijau-utama' : 'text-gray-300'}>11</span>
                          <span className={g.mengajarKelas12 ? 'font-bold text-hijau-utama' : 'text-gray-300'}>12</span>
                        </div>
                      </td>
                      <td className="py-2.5 px-2 text-center">
                        <span
                          className={`inline-block px-2 py-0.5 rounded text-[10px] font-semibold ${
                            g.statusAktif
                              ? 'bg-emerald-100 text-emerald-800'
                              : 'bg-red-100 text-red-800'
                          }`}
                        >
                          {g.statusAktif ? 'Aktif' : 'Nonaktif'}
                        </span>
                      </td>
                      <td className="py-2.5 px-3 text-center">
                        <div className="flex items-center justify-center gap-1.5">
                          <button
                            onClick={() => handleOpenDetailModal(g)}
                            title="Lihat Detail"
                            className="p-1 text-teks-sekunder hover:text-hijau-utama hover:bg-hijau-soft rounded"
                          >
                            <Eye className="w-3.5 h-3.5" />
                          </button>
                          <button
                            onClick={() => handleOpenEditModal(g)}
                            title="Edit Guru"
                            className="p-1 text-teks-sekunder hover:text-blue-600 hover:bg-blue-50 rounded"
                          >
                            <Edit2 className="w-3.5 h-3.5" />
                          </button>
                          <button
                            onClick={() => handleToggleStatus(g)}
                            title={g.statusAktif ? 'Nonaktifkan' : 'Aktifkan'}
                            className={`p-1 rounded ${
                              g.statusAktif
                                ? 'text-teks-sekunder hover:text-red-600 hover:bg-red-50'
                                : 'text-teks-sekunder hover:text-emerald-600 hover:bg-emerald-50'
                            }`}
                          >
                            {g.statusAktif ? <XCircle className="w-3.5 h-3.5" /> : <CheckCircle className="w-3.5 h-3.5" />}
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </div>

        {/* Modal Tambah / Edit Guru Sederhana */}
        {isModalOpen && (
          <div className="fixed inset-0 z-50 bg-black/40 flex items-center justify-center p-4">
            <div className="bg-white rounded-xl border border-hijau-muda shadow-lg max-w-2xl w-full max-h-[90vh] overflow-y-auto">
              <div className="p-4 border-b border-hijau-muda flex items-center justify-between">
                <h3 className="font-semibold text-sm text-teks-utama">
                  {isEditing ? 'Edit Data Guru' : 'Tambah Data Guru Baru'}
                </h3>
                <button
                  onClick={() => setIsModalOpen(false)}
                  className="p-1 text-teks-sekunder hover:text-teks-utama rounded"
                >
                  <X className="w-4 h-4" />
                </button>
              </div>

              <form onSubmit={handleSave} className="p-5 space-y-4 text-xs">
                {errorMsg && (
                  <div className="p-3 rounded-lg bg-red-50 text-red-700 border border-red-200">
                    {errorMsg}
                  </div>
                )}

                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                  <div>
                    <label className="block font-medium text-teks-utama mb-1">NIP</label>
                    <input
                      type="text"
                      value={formData.nip || ''}
                      onChange={(e) => setFormData({ ...formData, nip: e.target.value })}
                      placeholder="18 digit NIP"
                      className="w-full p-2 bg-latar-soft border border-hijau-muda rounded-lg text-xs"
                      required
                    />
                  </div>

                  <div>
                    <label className="block font-medium text-teks-utama mb-1">Nama Lengkap & Gelar</label>
                    <input
                      type="text"
                      value={formData.nama || ''}
                      onChange={(e) => setFormData({ ...formData, nama: e.target.value })}
                      placeholder="Nama lengkap..."
                      className="w-full p-2 bg-latar-soft border border-hijau-muda rounded-lg text-xs"
                      required
                    />
                  </div>

                  <div>
                    <label className="block font-medium text-teks-utama mb-1">Jenis Kelamin</label>
                    <select
                      value={formData.jenisKelamin || 'L'}
                      onChange={(e) => setFormData({ ...formData, jenisKelamin: e.target.value })}
                      className="w-full p-2 bg-latar-soft border border-hijau-muda rounded-lg text-xs"
                    >
                      <option value="L">Laki-laki</option>
                      <option value="P">Perempuan</option>
                    </select>
                  </div>

                  <div>
                    <label className="block font-medium text-teks-utama mb-1">Mata Pelajaran / Jabatan</label>
                    <input
                      type="text"
                      value={formData.jabatanTugasMengajar || ''}
                      onChange={(e) => setFormData({ ...formData, jabatanTugasMengajar: e.target.value })}
                      placeholder="Contoh: Guru Matematika"
                      className="w-full p-2 bg-latar-soft border border-hijau-muda rounded-lg text-xs"
                      required
                    />
                  </div>

                  <div>
                    <label className="block font-medium text-teks-utama mb-1">Tugas Tambahan Utama</label>
                    <input
                      type="text"
                      value={formData.tugasTambahanUtama || ''}
                      onChange={(e) => setFormData({ ...formData, tugasTambahanUtama: e.target.value })}
                      placeholder="Contoh: Wali Kelas 10-A / Koordinator"
                      className="w-full p-2 bg-latar-soft border border-hijau-muda rounded-lg text-xs"
                    />
                  </div>

                  <div>
                    <label className="block font-medium text-teks-utama mb-1">Tugas Tambahan Lain</label>
                    <input
                      type="text"
                      value={formData.tugasTambahanLain || ''}
                      onChange={(e) => setFormData({ ...formData, tugasTambahanLain: e.target.value })}
                      placeholder="Contoh: Pembina OSIS / Ekstrakurikuler"
                      className="w-full p-2 bg-latar-soft border border-hijau-muda rounded-lg text-xs"
                    />
                  </div>

                  <div>
                    <label className="block font-medium text-teks-utama mb-1">Beban Jam Mengajar / Minggu</label>
                    <input
                      type="number"
                      value={formData.jumlahJamAjar || 24}
                      onChange={(e) => setFormData({ ...formData, jumlahJamAjar: Number(e.target.value) })}
                      min={1}
                      max={60}
                      className="w-full p-2 bg-latar-soft border border-hijau-muda rounded-lg text-xs"
                      required
                    />
                  </div>

                  <div>
                    <label className="block font-medium text-teks-utama mb-1">Jumlah Siswa per Rombel</label>
                    <input
                      type="number"
                      value={formData.jumlahSiswaPerRombel || 30}
                      onChange={(e) => setFormData({ ...formData, jumlahSiswaPerRombel: Number(e.target.value) })}
                      min={1}
                      max={50}
                      className="w-full p-2 bg-latar-soft border border-hijau-muda rounded-lg text-xs"
                      required
                    />
                  </div>
                </div>

                <div className="pt-2 border-t border-hijau-muda">
                  <label className="block font-medium text-teks-utama mb-2">Tingkat Kelas yang Diajar:</label>
                  <div className="flex gap-4">
                    <label className="flex items-center gap-1.5 cursor-pointer">
                      <input
                        type="checkbox"
                        checked={formData.mengajarKelas10 || false}
                        onChange={(e) => setFormData({ ...formData, mengajarKelas10: e.target.checked })}
                        className="rounded text-hijau-utama"
                      />
                      <span>Kelas 10</span>
                    </label>

                    <label className="flex items-center gap-1.5 cursor-pointer">
                      <input
                        type="checkbox"
                        checked={formData.mengajarKelas11 || false}
                        onChange={(e) => setFormData({ ...formData, mengajarKelas11: e.target.checked })}
                        className="rounded text-hijau-utama"
                      />
                      <span>Kelas 11</span>
                    </label>

                    <label className="flex items-center gap-1.5 cursor-pointer">
                      <input
                        type="checkbox"
                        checked={formData.mengajarKelas12 || false}
                        onChange={(e) => setFormData({ ...formData, mengajarKelas12: e.target.checked })}
                        className="rounded text-hijau-utama"
                      />
                      <span>Kelas 12</span>
                    </label>
                  </div>
                </div>

                <div className="flex justify-end gap-2 pt-4 border-t border-hijau-muda">
                  <button
                    type="button"
                    onClick={() => setIsModalOpen(false)}
                    className="px-4 py-2 bg-latar-soft hover:bg-gray-100 rounded-lg text-xs font-semibold text-teks-sekunder"
                  >
                    Batal
                  </button>
                  <button
                    type="submit"
                    disabled={saving}
                    className="px-4 py-2 bg-hijau-utama hover:bg-hijau-hover text-white rounded-lg text-xs font-semibold"
                  >
                    {saving ? 'Menyimpan...' : 'Simpan Data'}
                  </button>
                </div>
              </form>
            </div>
          </div>
        )}

        {/* Modal Detail Guru */}
        {isDetailModalOpen && selectedGuru && (
          <div className="fixed inset-0 z-50 bg-black/40 flex items-center justify-center p-4">
            <div className="bg-white rounded-xl border border-hijau-muda shadow-lg max-w-md w-full p-5 space-y-4 text-xs">
              <div className="flex items-center justify-between border-b border-hijau-muda pb-3">
                <h3 className="font-semibold text-sm text-teks-utama">Detail Profil Guru</h3>
                <button
                  onClick={() => setIsDetailModalOpen(false)}
                  className="p-1 text-teks-sekunder hover:text-teks-utama rounded"
                >
                  <X className="w-4 h-4" />
                </button>
              </div>

              <div className="space-y-2 text-teks-utama">
                <p><span className="text-teks-sekunder font-medium">Nama:</span> {selectedGuru.nama}</p>
                <p><span className="text-teks-sekunder font-medium">NIP:</span> {selectedGuru.nip}</p>
                <p><span className="text-teks-sekunder font-medium">Jenis Kelamin:</span> {selectedGuru.jenisKelamin === 'L' ? 'Laki-laki' : 'Perempuan'}</p>
                <p><span className="text-teks-sekunder font-medium">Mata Pelajaran:</span> {selectedGuru.jabatanTugasMengajar}</p>
                <p><span className="text-teks-sekunder font-medium">Tugas Tambahan:</span> {selectedGuru.tugasTambahanUtama || '-'}</p>
                <p><span className="text-teks-sekunder font-medium">Tugas Lain:</span> {selectedGuru.tugasTambahanLain || '-'}</p>
                <p><span className="text-teks-sekunder font-medium">Beban Mengajar:</span> {selectedGuru.jumlahJamAjar} Jam/Minggu</p>
                <p><span className="text-teks-sekunder font-medium">Siswa per Rombel:</span> {selectedGuru.jumlahSiswaPerRombel} Siswa</p>
                <p><span className="text-teks-sekunder font-medium">Status:</span> {selectedGuru.statusAktif ? 'Aktif' : 'Nonaktif'}</p>
              </div>

              <div className="flex justify-end pt-3 border-t border-hijau-muda">
                <button
                  type="button"
                  onClick={() => setIsDetailModalOpen(false)}
                  className="px-4 py-1.5 bg-latar-soft hover:bg-gray-100 rounded-lg text-xs font-semibold text-teks-utama"
                >
                  Tutup
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </AppLayout>
  );
}
