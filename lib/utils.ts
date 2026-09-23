import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

/**
 * Format angka desimal dengan jumlah digit tertentu
 */
export function formatDesimal(nilai: number | null | undefined, digit: number = 4): string {
  if (nilai === null || nilai === undefined || isNaN(nilai)) return '-';
  return Number(nilai).toFixed(digit);
}

/**
 * Format tanggal dalam bahasa Indonesia
 */
export function formatTanggalIndonesia(date: Date | string | null | undefined): string {
  if (!date) return '-';
  const d = typeof date === 'string' ? new Date(date) : date;
  return new Intl.DateTimeFormat('id-ID', {
    day: 'numeric',
    month: 'long',
    year: 'numeric',
  }).format(d);
}

/**
 * Mendapatkan predikat / label berdasarkan nilai 1-5
 */
export function getPredikatNilai(nilai: number): { label: string; badgeColor: string } {
  if (nilai >= 4.5) {
    return { label: 'Sangat Baik', badgeColor: 'bg-emerald-100 text-emerald-800 border-emerald-300' };
  } else if (nilai >= 3.5) {
    return { label: 'Baik', badgeColor: 'bg-hijau-muda text-teks-utama border-hijau-utama/30' };
  } else if (nilai >= 2.5) {
    return { label: 'Cukup', badgeColor: 'bg-kuning-muda text-amber-900 border-amber-300' };
  } else if (nilai >= 1.5) {
    return { label: 'Kurang', badgeColor: 'bg-orange-100 text-orange-800 border-orange-300' };
  } else {
    return { label: 'Sangat Kurang', badgeColor: 'bg-red-100 text-red-800 border-red-300' };
  }
}
