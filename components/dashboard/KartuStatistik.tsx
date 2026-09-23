import React from 'react';
import { LucideIcon } from 'lucide-react';

interface KartuStatistikProps {
  title: string;
  value: string | number;
  subtext?: string;
  icon?: LucideIcon;
  variant?: 'putih' | 'hijau' | 'kuning';
}

export default function KartuStatistik({
  title,
  value,
  subtext,
  icon: Icon,
  variant = 'putih',
}: KartuStatistikProps) {
  return (
    <div className="bg-white p-4 rounded-xl border border-hijau-muda/80 flex items-start justify-between">
      <div className="space-y-1">
        <p className="text-xs font-medium text-teks-sekunder">{title}</p>
        <p className="text-2xl font-bold text-teks-utama tracking-tight">{value}</p>
        {subtext && <p className="text-[11px] text-teks-sekunder">{subtext}</p>}
      </div>
      {Icon && (
        <div className="p-2 rounded-lg bg-hijau-soft text-hijau-utama shrink-0">
          <Icon className="w-4 h-4" />
        </div>
      )}
    </div>
  );
}
