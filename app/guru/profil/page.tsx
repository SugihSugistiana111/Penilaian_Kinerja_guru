'use client';

import React, { useState, useEffect } from 'react';
import AppLayout from '@/components/dashboard/AppLayout';

export default function GuruProfilPage() {
  const [session, setSession] = useState<any>(null);
  const [guruData, setGuruData] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchProfil = async () => {
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
    fetchProfil();
  }, []);

  return (
    <AppLayout
      title="Profil Guru"
      subtitle="Informasi data kepegawaian dan beban mengajar SMA Al-Ihsan Boarding School"
      user={session || { nama: 'Guru Pengajar', username: 'guru', role: 'GURU' }}
    >
      <div className="max-w-2xl space-y-6">
        {loading ? (
          <div className="bg-white p-12 rounded-xl border border-hijau-muda text-center text-xs text-teks-sekunder">
            Memuat profil...
          </div>
        ) : !guruData ? (
          <div className="bg-white p-12 rounded-xl border border-hijau-muda text-center text-xs text-teks-sekunder">
            Data profil guru tidak ditemukan.
          </div>
        ) : (
          <div className="bg-white rounded-xl border border-hijau-muda p-6 space-y-4">
            <div className="border-b border-hijau-muda pb-4">
              <h3 className="font-semibold text-base text-teks-utama">{guruData.nama}</h3>
              <p className="text-xs font-mono text-teks-sekunder">NIP. {guruData.nip}</p>
            </div>

            <div className="space-y-2.5 text-xs text-teks-utama">
              <div className="grid grid-cols-3 gap-2">
                <span className="text-teks-sekunder font-medium">Jenis Kelamin</span>
                <span className="col-span-2 font-semibold">{guruData.jenisKelamin === 'L' ? 'Laki-laki' : 'Perempuan'}</span>
              </div>

              <div className="grid grid-cols-3 gap-2">
                <span className="text-teks-sekunder font-medium">Mata Pelajaran</span>
                <span className="col-span-2 font-semibold">{guruData.jabatanTugasMengajar}</span>
              </div>

              <div className="grid grid-cols-3 gap-2">
                <span className="text-teks-sekunder font-medium">Tugas Tambahan Utama</span>
                <span className="col-span-2 font-semibold">{guruData.tugasTambahanUtama || '-'}</span>
              </div>

              <div className="grid grid-cols-3 gap-2">
                <span className="text-teks-sekunder font-medium">Tugas Tambahan Lain</span>
                <span className="col-span-2 font-semibold">{guruData.tugasTambahanLain || '-'}</span>
              </div>

              <div className="grid grid-cols-3 gap-2">
                <span className="text-teks-sekunder font-medium">Beban Mengajar</span>
                <span className="col-span-2 font-semibold">{guruData.jumlahJamAjar} Jam / Minggu</span>
              </div>

              <div className="grid grid-cols-3 gap-2">
                <span className="text-teks-sekunder font-medium">Siswa per Rombel</span>
                <span className="col-span-2 font-semibold">{guruData.jumlahSiswaPerRombel} Siswa</span>
              </div>

              <div className="grid grid-cols-3 gap-2">
                <span className="text-teks-sekunder font-medium">Kelas Mengajar</span>
                <span className="col-span-2 font-semibold">
                  {[
                    guruData.mengajarKelas10 ? 'Kelas 10' : null,
                    guruData.mengajarKelas11 ? 'Kelas 11' : null,
                    guruData.mengajarKelas12 ? 'Kelas 12' : null,
                  ].filter(Boolean).join(', ')}
                </span>
              </div>

              <div className="grid grid-cols-3 gap-2">
                <span className="text-teks-sekunder font-medium">Status Kepegawaian</span>
                <span className="col-span-2">
                  <span className="inline-block px-2 py-0.5 rounded text-[10px] font-semibold bg-emerald-100 text-emerald-800">
                    {guruData.statusAktif ? 'Aktif' : 'Nonaktif'}
                  </span>
                </span>
              </div>
            </div>
          </div>
        )}
      </div>
    </AppLayout>
  );
}
