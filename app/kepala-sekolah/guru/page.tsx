'use client';

import React, { useState, useEffect } from 'react';
import AppLayout from '@/components/dashboard/AppLayout';
import {
  Search,
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

export default function KepsekDataGuruPage() {
  const [daftarGuru, setDaftarGuru] = useState<GuruData[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [filterKelas, setFilterKelas] = useState('all');
  const [selectedGuru, setSelectedGuru] = useState<GuruData | null>(null);

  useEffect(() => {
    const fetchGuru = async () => {
      setLoading(true);
      try {
        const res = await fetch('/api/guru?statusAktif=true');
        const data = await res.json();
        setDaftarGuru(data);
      } catch (e) {
        console.error(e);
      } finally {
        setLoading(false);
      }
    };
    fetchGuru();
  }, []);

  const filteredData = daftarGuru.filter((g) => {
    if (filterKelas === '10' && !g.mengajarKelas10) return false;
    if (filterKelas === '11' && !g.mengajarKelas11) return false;
    if (filterKelas === '12' && !g.mengajarKelas12) return false;
    if (
      search &&
      !g.nama.toLowerCase().includes(search.toLowerCase()) &&
      !g.nip.includes(search) &&
      !g.jabatanTugasMengajar.toLowerCase().includes(search.toLowerCase())
    ) {
      return false;
    }
    return true;
  });

  return (
    <AppLayout
      title="Data Guru & Tenaga Pengajar"
      subtitle="Daftar tenaga pendidik aktif di SMA Al-Ihsan Boarding School"
      user={{ nama: 'Dr. H. Mulyadi, M.Pd.', username: 'kepsek', role: 'KEPALA_SEKOLAH' }}
    >
      <div className="space-y-6">
        {/* Search & Filter Toolbar */}
        <div className="p-4 bg-white rounded-xl border border-hijau-muda flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-3">
          <div className="flex flex-wrap items-center gap-2">
            <div className="relative min-w-[220px]">
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
              <option value="all">Semua Tingkat Kelas</option>
              <option value="10">Kelas 10</option>
              <option value="11">Kelas 11</option>
              <option value="12">Kelas 12</option>
            </select>
          </div>

          <span className="text-xs text-teks-sekunder">Total: {filteredData.length} Guru Aktif</span>
        </div>

        {/* Tabel Data Guru */}
        <div className="bg-white rounded-xl border border-hijau-muda overflow-hidden">
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
                  <th className="py-2.5 px-3 text-center w-20">Aksi</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-hijau-muda/50 text-teks-utama">
                {loading ? (
                  <tr>
                    <td colSpan={9} className="py-8 text-center text-teks-sekunder">
                      Memuat daftar guru...
                    </td>
                  </tr>
                ) : filteredData.length === 0 ? (
                  <tr>
                    <td colSpan={9} className="py-8 text-center text-teks-sekunder">
                      Tidak ada data guru yang cocok.
                    </td>
                  </tr>
                ) : (
                  filteredData.map((g, idx) => (
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
                      <td className="py-2.5 px-3 text-center">
                        <button
                          onClick={() => setSelectedGuru(g)}
                          title="Lihat Detail Profil"
                          className="px-2.5 py-1 text-xs text-teks-utama hover:bg-hijau-soft border border-hijau-muda rounded flex items-center gap-1 mx-auto"
                        >
                          <Eye className="w-3.5 h-3.5 text-hijau-utama" />
                          <span>Detail</span>
                        </button>
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </div>

        {/* Modal Detail Guru */}
        {selectedGuru && (
          <div className="fixed inset-0 z-50 bg-black/40 flex items-center justify-center p-4">
            <div className="bg-white rounded-xl border border-hijau-muda shadow-lg max-w-md w-full p-5 space-y-4 text-xs">
              <div className="flex items-center justify-between border-b border-hijau-muda pb-3">
                <h3 className="font-semibold text-sm text-teks-utama">Detail Profil Guru</h3>
                <button
                  onClick={() => setSelectedGuru(null)}
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
              </div>

              <div className="flex justify-end pt-3 border-t border-hijau-muda">
                <button
                  type="button"
                  onClick={() => setSelectedGuru(null)}
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
