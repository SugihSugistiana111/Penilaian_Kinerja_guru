'use client';

import React, { useState, useEffect } from 'react';
import AppLayout from '@/components/dashboard/AppLayout';
import {
  Key,
  CheckCircle,
  XCircle,
  Search,
  X,
  Edit2,
} from 'lucide-react';

interface UserData {
  id: string;
  nama: string;
  username: string;
  roleId: string;
  role: { namaRole: string };
  guruId?: string | null;
  guru?: { nama: string; nip: string; jabatanTugasMengajar: string } | null;
  status: boolean;
  createdAt: string;
}

export default function AdminPenggunaPage() {
  const [users, setUsers] = useState<UserData[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [filterRole, setFilterRole] = useState('all');

  // Modal Edit / Reset Password
  const [selectedUser, setSelectedUser] = useState<UserData | null>(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [newPassword, setNewPassword] = useState('');
  const [namaInput, setNamaInput] = useState('');
  const [saving, setSaving] = useState(false);
  const [successMsg, setSuccessMsg] = useState('');

  const fetchUsers = async () => {
    setLoading(true);
    try {
      const res = await fetch('/api/pengguna');
      const data = await res.json();
      setUsers(data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchUsers();
  }, []);

  const handleOpenEdit = (user: UserData) => {
    setSelectedUser(user);
    setNamaInput(user.nama);
    setNewPassword('');
    setSuccessMsg('');
    setIsModalOpen(true);
  };

  const handleSaveUser = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedUser) return;

    setSaving(true);
    try {
      const res = await fetch('/api/pengguna', {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          id: selectedUser.id,
          nama: namaInput,
          password: newPassword || undefined,
        }),
      });

      const data = await res.json();
      if (!res.ok) throw new Error(data.error || 'Gagal menyimpan data pengguna');

      setSuccessMsg(`Data akun ${selectedUser.username} berhasil diperbarui.`);
      setIsModalOpen(false);
      fetchUsers();
    } catch (err: any) {
      alert(err.message || 'Terjadi kesalahan');
    } finally {
      setSaving(false);
    }
  };

  const handleToggleStatus = async (user: UserData) => {
    if (user.username === 'admin') {
      alert('Akun Administrator utama tidak dapat dinonaktifkan.');
      return;
    }

    const confirm = window.confirm(
      `Apakah Anda yakin ingin ${user.status ? 'menonaktifkan' : 'mengaktifkan'} akun ${user.username}?`
    );
    if (!confirm) return;

    try {
      const res = await fetch('/api/pengguna', {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          id: user.id,
          status: !user.status,
        }),
      });

      if (!res.ok) throw new Error('Gagal mengubah status');
      fetchUsers();
    } catch (e) {
      alert('Terjadi kesalahan.');
    }
  };

  const filteredUsers = users.filter((u) => {
    const matchSearch =
      u.nama.toLowerCase().includes(search.toLowerCase()) ||
      u.username.toLowerCase().includes(search.toLowerCase()) ||
      (u.guru?.nip && u.guru.nip.includes(search));

    const matchRole =
      filterRole === 'all'
        ? true
        : u.role.namaRole === filterRole;

    return matchSearch && matchRole;
  });

  return (
    <AppLayout
      title="Manajemen Pengguna"
      subtitle="Pengaturan akun login Administrator, Kepala Sekolah, dan 18 Guru"
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
                placeholder="Cari user, nama, username..."
                className="w-full pl-8 pr-3 py-1.5 bg-latar-soft border border-hijau-muda rounded-lg text-xs text-teks-utama focus:ring-2 focus:ring-hijau-utama"
              />
            </div>

            <select
              value={filterRole}
              onChange={(e) => setFilterRole(e.target.value)}
              className="px-3 py-1.5 bg-latar-soft border border-hijau-muda rounded-lg text-xs font-medium text-teks-utama focus:ring-2 focus:ring-hijau-utama"
            >
              <option value="all">Semua Peran (Role)</option>
              <option value="ADMIN">Administrator</option>
              <option value="KEPALA_SEKOLAH">Kepala Sekolah</option>
              <option value="GURU">Guru Pengajar</option>
            </select>
          </div>

          <span className="text-xs text-teks-sekunder">Total: {filteredUsers.length} Pengguna</span>
        </div>

        {successMsg && (
          <div className="p-3 rounded-lg bg-emerald-50 text-emerald-800 border border-emerald-200 text-xs flex items-center gap-2">
            <CheckCircle className="w-4 h-4 shrink-0" />
            <span>{successMsg}</span>
          </div>
        )}

        {/* Tabel Pengguna */}
        <div className="bg-white rounded-xl border border-hijau-muda overflow-hidden">
          <div className="p-4 border-b border-hijau-muda">
            <h3 className="font-semibold text-sm text-teks-utama">Daftar Akun Pengguna</h3>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-hijau-soft border-b border-hijau-muda text-teks-utama font-semibold">
                <tr>
                  <th className="py-2.5 px-3 text-center w-12">No</th>
                  <th className="py-2.5 px-3">Nama Pengguna</th>
                  <th className="py-2.5 px-3">Username</th>
                  <th className="py-2.5 px-3 text-center">Peran (Role)</th>
                  <th className="py-2.5 px-3 text-center">Status Akun</th>
                  <th className="py-2.5 px-3 text-center w-36">Aksi</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-hijau-muda/50 text-teks-utama">
                {loading ? (
                  <tr>
                    <td colSpan={6} className="py-8 text-center text-teks-sekunder">
                      Memuat daftar pengguna...
                    </td>
                  </tr>
                ) : filteredUsers.length === 0 ? (
                  <tr>
                    <td colSpan={6} className="py-8 text-center text-teks-sekunder">
                      Tidak ada akun pengguna yang cocok.
                    </td>
                  </tr>
                ) : (
                  filteredUsers.map((u, idx) => (
                    <tr key={u.id} className="hover:bg-hijau-soft/40 transition-colors">
                      <td className="py-2.5 px-3 text-center font-medium text-teks-sekunder">{idx + 1}</td>
                      <td className="py-2.5 px-3 font-semibold">{u.nama}</td>
                      <td className="py-2.5 px-3 font-mono text-teks-sekunder">{u.username}</td>
                      <td className="py-2.5 px-3 text-center">
                        <span className="inline-block px-2 py-0.5 rounded bg-latar-soft text-teks-utama font-semibold text-[11px] border border-hijau-muda">
                          {u.role.namaRole}
                        </span>
                      </td>
                      <td className="py-2.5 px-3 text-center">
                        <span
                          className={`inline-block px-2 py-0.5 rounded text-[10px] font-semibold ${
                            u.status
                              ? 'bg-emerald-100 text-emerald-800'
                              : 'bg-red-100 text-red-800'
                          }`}
                        >
                          {u.status ? 'Aktif' : 'Nonaktif'}
                        </span>
                      </td>
                      <td className="py-2.5 px-3 text-center">
                        <div className="flex items-center justify-center gap-1.5">
                          <button
                            onClick={() => handleOpenEdit(u)}
                            className="px-2 py-1 text-xs text-teks-utama hover:bg-hijau-soft border border-hijau-muda rounded flex items-center gap-1"
                          >
                            <Edit2 className="w-3 h-3 text-hijau-utama" />
                            <span>Edit / Reset</span>
                          </button>
                          {u.username !== 'admin' && (
                            <button
                              onClick={() => handleToggleStatus(u)}
                              title={u.status ? 'Nonaktifkan' : 'Aktifkan'}
                              className={`p-1 rounded ${
                                u.status
                                  ? 'text-teks-sekunder hover:text-red-600 hover:bg-red-50'
                                  : 'text-teks-sekunder hover:text-emerald-600 hover:bg-emerald-50'
                              }`}
                            >
                              {u.status ? <XCircle className="w-3.5 h-3.5" /> : <CheckCircle className="w-3.5 h-3.5" />}
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

        {/* Modal Edit / Reset Password */}
        {isModalOpen && selectedUser && (
          <div className="fixed inset-0 z-50 bg-black/40 flex items-center justify-center p-4">
            <div className="bg-white rounded-xl border border-hijau-muda shadow-lg max-w-md w-full p-5 space-y-4 text-xs">
              <div className="flex items-center justify-between border-b border-hijau-muda pb-3">
                <h3 className="font-semibold text-sm text-teks-utama">
                  Edit Akun: {selectedUser.username}
                </h3>
                <button
                  onClick={() => setIsModalOpen(false)}
                  className="p-1 text-teks-sekunder hover:text-teks-utama rounded"
                >
                  <X className="w-4 h-4" />
                </button>
              </div>

              <form onSubmit={handleSaveUser} className="space-y-3">
                <div>
                  <label className="block font-medium text-teks-utama mb-1">Nama Tampilan:</label>
                  <input
                    type="text"
                    value={namaInput}
                    onChange={(e) => setNamaInput(e.target.value)}
                    className="w-full p-2 bg-latar-soft border border-hijau-muda rounded-lg text-xs"
                    required
                  />
                </div>

                <div>
                  <label className="block font-medium text-teks-utama mb-1">
                    Password Baru (Kosongkan jika tidak ingin mengubah):
                  </label>
                  <input
                    type="password"
                    value={newPassword}
                    onChange={(e) => setNewPassword(e.target.value)}
                    placeholder="Masukkan password baru..."
                    className="w-full p-2 bg-latar-soft border border-hijau-muda rounded-lg text-xs"
                  />
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
                    disabled={saving}
                    className="px-4 py-2 bg-hijau-utama hover:bg-hijau-hover text-white rounded-lg text-xs font-semibold"
                  >
                    {saving ? 'Menyimpan...' : 'Simpan Perubahan'}
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
