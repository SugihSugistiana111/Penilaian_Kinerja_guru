import React from 'react';
import Image from 'next/image';

interface LogoProps {
  className?: string;
  size?: number;
  showText?: boolean;
}

export default function Logo({ className = '', size = 44, showText = false }: LogoProps) {
  return (
    <div className={`flex items-center gap-3 ${className}`}>
      <div
        className="relative shrink-0 flex items-center justify-center rounded-2xl overflow-hidden shadow-sm"
        style={{ width: size, height: size }}
      >
        <img
          src="/logo/logo-alihsan.jpg"
          alt="Logo SMA Al-Ihsan Boarding School"
          className="w-full h-full object-contain"
        />
      </div>
      {showText && (
        <div>
          <h1 className="font-bold text-sm text-teks-utama leading-tight tracking-tight">
            SMA AL-IHSAN
          </h1>
          <p className="text-[10px] font-semibold text-teks-sekunder uppercase tracking-wider">
            Boarding School
          </p>
        </div>
      )}
    </div>
  );
}
