'use client';

import React, { useState, Suspense } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import { Lock, User, ShieldCheck, ArrowRight, Sparkles, GraduationCap } from 'lucide-react';

function LoginForm() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const callbackUrl = searchParams.get('callbackUrl') || '';

  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!username || !password) {
      setErrorMsg('Username dan password wajib diisi.');
      return;
    }

    setLoading(true);
    setErrorMsg('');

    try {
      const res = await fetch('/api/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password }),
      });

      const data = await res.json();

      if (!res.ok) {
        throw new Error(data.error || 'Gagal login ke dalam sistem');
      }

      // Redirect sesuai role
      if (callbackUrl) {
        router.push(callbackUrl);
      } else if (data.user.role === 'ADMIN') {
        router.push('/admin/dashboard');
      } else if (data.user.role === 'KEPALA_SEKOLAH') {
        router.push('/kepala-sekolah/dashboard');
      } else {
        router.push('/guru/dashboard');
      }
      router.refresh();
    } catch (err: any) {
      setErrorMsg(err.message || 'Terjadi kesalahan');
    } finally {
      setLoading(false);
    }
  };

  const handleQuickDemo = (u: string, p: string) => {
    setUsername(u);
    setPassword(p);
  };

  return (
    <div className="w-full max-w-md bg-white rounded-3xl border border-hijau-muda/80 shadow-xl overflow-hidden">
      {/* Header Branding dengan Logo Asli */}
      <div className="bg-gradient-to-br from-hijau-soft via-white to-kuning-soft/30 p-8 text-center border-b border-hijau-muda/40">
        <div className="w-28 h-28 mx-auto mb-3 flex items-center justify-center">
          <img
            src="/logo/logo-alihsan.jpg"
            alt="Logo Resmi SMA Al-Ihsan Boarding School"
            className="w-full h-full object-contain drop-shadow-md rounded-2xl"
          />
        </div>
        <h1 className="text-lg font-bold text-teks-utama tracking-tight">
          SMA AL-IHSAN BOARDING SCHOOL
        </h1>
        <p className="text-[11px] font-semibold text-teks-sekunder uppercase tracking-widest mt-0.5">
          SPK Penilaian Kinerja Guru (Metode MOORA)
        </p>
      </div>

      {/* Form Container */}
      <div className="p-8 space-y-6">
        {errorMsg && (
          <div className="p-4 rounded-xl bg-red-50 border border-red-200 text-red-700 text-xs font-medium flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-red-500 shrink-0" />
            {errorMsg}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-xs font-bold text-teks-utama uppercase tracking-wider mb-2">
              Username
            </label>
            <div className="relative">
              <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-teks-sekunder">
                <User className="w-4 h-4" />
              </div>
              <input
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                placeholder="Masukkan username anda"
                className="w-full pl-10 pr-4 py-3 bg-hijau-soft/40 border border-hijau-muda rounded-xl text-sm text-teks-utama placeholder:text-teks-sekunder/50 focus:outline-none focus:ring-2 focus:ring-hijau-utama focus:bg-white transition-all"
                required
              />
            </div>
          </div>

          <div>
            <label className="block text-xs font-bold text-teks-utama uppercase tracking-wider mb-2">
              Password
            </label>
            <div className="relative">
              <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-teks-sekunder">
                <Lock className="w-4 h-4" />
              </div>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Masukkan password anda"
                className="w-full pl-10 pr-4 py-3 bg-hijau-soft/40 border border-hijau-muda rounded-xl text-sm text-teks-utama placeholder:text-teks-sekunder/50 focus:outline-none focus:ring-2 focus:ring-hijau-utama focus:bg-white transition-all"
                required
              />
            </div>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full py-3.5 bg-hijau-utama hover:bg-hijau-hover text-white rounded-xl font-bold text-sm shadow-md hover:shadow-lg transition-all flex items-center justify-center gap-2 mt-2 disabled:opacity-70"
          >
            {loading ? (
              <span>Memverifikasi...</span>
            ) : (
              <>
                <span>Masuk ke Sistem</span>
                <ArrowRight className="w-4 h-4" />
              </>
            )}
          </button>
        </form>

        {/* Quick Demo Accounts Selection */}
        <div className="pt-4 border-t border-hijau-muda/40">
          <div className="flex items-center gap-1.5 mb-3 text-xs font-semibold text-teks-sekunder">
            <Sparkles className="w-3.5 h-3.5 text-amber-500" />
            <span>Akun Demo Cepat (1-Klik untuk Uji Coba):</span>
          </div>
          <div className="grid grid-cols-2 gap-2">
            <button
              type="button"
              onClick={() => handleQuickDemo('admin', 'admin123')}
              className="p-2.5 rounded-xl border border-hijau-muda bg-hijau-soft/50 hover:bg-hijau-muda/70 text-left transition-all"
            >
              <div className="flex items-center gap-1.5 text-xs font-bold text-teks-utama">
                <ShieldCheck className="w-3.5 h-3.5 text-hijau-utama" />
                <span>Administrator</span>
              </div>
              <p className="text-[10px] text-teks-sekunder mt-0.5 font-mono">admin / admin123</p>
            </button>

            <button
              type="button"
              onClick={() => handleQuickDemo('kepsek', 'kepsek123')}
              className="p-2.5 rounded-xl border border-kuning-muda bg-kuning-soft/60 hover:bg-kuning-muda/70 text-left transition-all"
            >
              <div className="flex items-center gap-1.5 text-xs font-bold text-amber-950">
                <ShieldCheck className="w-3.5 h-3.5 text-amber-600" />
                <span>Kepala Sekolah</span>
              </div>
              <p className="text-[10px] text-teks-sekunder mt-0.5 font-mono">kepsek / kepsek123</p>
            </button>

            <button
              type="button"
              onClick={() => handleQuickDemo('guru1', 'guru123')}
              className="p-2.5 rounded-xl border border-hijau-muda bg-white hover:bg-hijau-soft text-left transition-all"
            >
              <div className="flex items-center gap-1.5 text-xs font-bold text-teks-utama">
                <GraduationCap className="w-3.5 h-3.5 text-teks-sekunder" />
                <span>Guru: Ahmad F.</span>
              </div>
              <p className="text-[10px] text-teks-sekunder mt-0.5 font-mono">guru1 / guru123</p>
            </button>

            <button
              type="button"
              onClick={() => handleQuickDemo('guru2', 'guru123')}
              className="p-2.5 rounded-xl border border-hijau-muda bg-white hover:bg-hijau-soft text-left transition-all"
            >
              <div className="flex items-center gap-1.5 text-xs font-bold text-teks-utama">
                <GraduationCap className="w-3.5 h-3.5 text-teks-sekunder" />
                <span>Guru: Siti N.</span>
              </div>
              <p className="text-[10px] text-teks-sekunder mt-0.5 font-mono">guru2 / guru123</p>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default function LoginPage() {
  return (
    <div className="min-h-screen bg-latar-soft flex flex-col justify-center items-center p-4 sm:p-6 lg:p-8">
      {/* Background Decorative Circles */}
      <div className="fixed top-0 left-0 w-96 h-96 bg-hijau-muda/40 rounded-full blur-3xl -z-10 -translate-x-1/2 -translate-y-1/2 pointer-events-none" />
      <div className="fixed bottom-0 right-0 w-96 h-96 bg-kuning-muda/50 rounded-full blur-3xl -z-10 translate-x-1/3 translate-y-1/3 pointer-events-none" />

      <Suspense fallback={<div className="text-xs text-teks-sekunder">Memuat halaman login...</div>}>
        <LoginForm />
      </Suspense>

      <div className="mt-8 text-center text-xs text-teks-sekunder/70">
        <p>© 2026 SMA Al-Ihsan Boarding School. Sistem Pendukung Keputusan Kinerja Guru.</p>
      </div>
    </div>
  );
}
