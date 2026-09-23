'use client';

import React, { useState, useEffect, useRef } from 'react';
import AppLayout from '@/components/dashboard/AppLayout';
import { Download, Calendar, Loader2, Printer } from 'lucide-react';
import { formatTanggalIndonesia, getPredikatNilai } from '@/lib/utils';
import jsPDF from 'jspdf';
import html2canvas from 'html2canvas';

interface PeriodeItem {
  id: string;
  namaPeriode: string;
  bulan: string;
  tahun: number;
}

export default function KepsekLaporanPage() {
  const [periodeList, setPeriodeList] = useState<PeriodeItem[]>([]);
  const [selectedPeriodeId, setSelectedPeriodeId] = useState<string>('');
  const [laporanData, setLaporanData] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [downloading, setDownloading] = useState(false);
  const reportRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const fetchPeriode = async () => {
      try {
        const res = await fetch('/api/periode');
        const data: PeriodeItem[] = await res.json();
        setPeriodeList(data);
        if (data.length > 0) setSelectedPeriodeId(data[0].id);
      } catch (e) {
        console.error(e);
      }
    };
    fetchPeriode();
  }, []);

  useEffect(() => {
    const fetchLaporan = async () => {
      if (!selectedPeriodeId) return;
      setLoading(true);
      try {
        const res = await fetch(`/api/moora/detail?periodeId=${selectedPeriodeId}`);
        const data = await res.json();
        setLaporanData(data.hasilTersimpan || []);
      } catch (e) {
        console.error(e);
      } finally {
        setLoading(false);
      }
    };
    fetchLaporan();
  }, [selectedPeriodeId]);

  const selectedPeriode = periodeList.find((p) => p.id === selectedPeriodeId);

  const handleDownloadPDF = async () => {
    if (!reportRef.current) return;
    setDownloading(true);

    try {
      const element = reportRef.current;
      const canvas = await html2canvas(element, {
        scale: 2,
        useCORS: true,
        logging: false,
        backgroundColor: '#ffffff',
        windowWidth: 1024,
      });

      const pdf = new jsPDF('p', 'mm', 'a4');
      const pdfWidth = pdf.internal.pageSize.getWidth(); // 210mm
      const pdfHeight = pdf.internal.pageSize.getHeight(); // 297mm
      const margin = 10; // 10mm margin
      const contentWidth = pdfWidth - margin * 2; // 190mm
      const pageContentHeightMM = pdfHeight - margin * 2; // 277mm

      const imgWidth = canvas.width;
      const pageCanvasHeight = Math.floor((canvas.width * pageContentHeightMM) / contentWidth);
      const totalPages = Math.ceil(canvas.height / pageCanvasHeight);

      for (let i = 0; i < totalPages; i++) {
        if (i > 0) {
          pdf.addPage();
        }

        const pageCanvas = document.createElement('canvas');
        pageCanvas.width = imgWidth;
        const currentSliceHeight = Math.min(pageCanvasHeight, canvas.height - i * pageCanvasHeight);
        pageCanvas.height = currentSliceHeight;

        const ctx = pageCanvas.getContext('2d');
        if (ctx) {
          ctx.fillStyle = '#ffffff';
          ctx.fillRect(0, 0, pageCanvas.width, pageCanvas.height);
          ctx.drawImage(
            canvas,
            0,
            i * pageCanvasHeight,
            imgWidth,
            currentSliceHeight,
            0,
            0,
            imgWidth,
            currentSliceHeight
          );
        }

        const pageImgData = pageCanvas.toDataURL('image/jpeg', 0.98);
        const renderedHeightMM = (currentSliceHeight * contentWidth) / imgWidth;

        pdf.addImage(pageImgData, 'JPEG', margin, margin, contentWidth, renderedHeightMM);
      }

      const cleanPeriodeName = (selectedPeriode?.namaPeriode || 'Periode').replace(/\s+/g, '-');
      pdf.save(`Laporan-Kinerja-Guru-${cleanPeriodeName}.pdf`);
    } catch (err) {
      console.error('Gagal mengunduh PDF:', err);
      alert('Terjadi kesalahan saat mengunduh PDF.');
    } finally {
      setDownloading(false);
    }
  };

  return (
    <AppLayout
      title="Cetak Laporan Kinerja Guru"
      subtitle="Dokumen resmi laporan penilaian berkala pimpinan SMA Al-Ihsan"
      user={{ nama: 'Dr. H. Mulyadi, M.Pd.', username: 'kepsek', role: 'KEPALA_SEKOLAH' }}
    >
      <div className="space-y-6">
        {/* Toolbar Download PDF */}
        <div className="no-print p-4 bg-white rounded-xl border border-hijau-muda flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-3">
          <div className="flex items-center gap-2">
            <Calendar className="w-4 h-4 text-hijau-utama" />
            <label className="text-xs font-semibold text-teks-utama">Pilih Periode:</label>
            <select
              value={selectedPeriodeId}
              onChange={(e) => setSelectedPeriodeId(e.target.value)}
              className="px-3 py-1.5 bg-latar-soft border border-hijau-muda rounded-lg text-xs font-medium text-teks-utama focus:ring-2 focus:ring-hijau-utama"
            >
              {periodeList.map((p) => (
                <option key={p.id} value={p.id}>
                  {p.namaPeriode}
                </option>
              ))}
            </select>
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={() => window.print()}
              className="px-3.5 py-1.5 bg-latar-soft hover:bg-hijau-soft border border-hijau-muda rounded-lg text-xs font-semibold text-teks-utama flex items-center gap-1.5 transition-colors"
            >
              <Printer className="w-3.5 h-3.5 text-teks-sekunder" />
              <span>Cetak</span>
            </button>
            <button
              onClick={handleDownloadPDF}
              disabled={downloading || loading || !laporanData || laporanData.length === 0}
              className="px-4 py-1.5 bg-hijau-utama hover:bg-hijau-hover text-white rounded-lg text-xs font-semibold flex items-center justify-center gap-1.5 transition-colors disabled:opacity-50"
            >
              {downloading ? (
                <>
                  <Loader2 className="w-3.5 h-3.5 animate-spin" />
                  <span>Menyiapkan PDF...</span>
                </>
              ) : (
                <>
                  <Download className="w-3.5 h-3.5" />
                  <span>Download PDF</span>
                </>
              )}
            </button>
          </div>
        </div>

        {/* Lembar Dokumen Kop Surat yang diexport */}
        <div
          ref={reportRef}
          className="bg-white p-8 sm:p-10 rounded-xl border border-hijau-muda max-w-4xl mx-auto space-y-6 print:shadow-none print:border-none print:p-0"
        >
          {/* Kop Surat */}
          <div className="border-b-4 border-double border-teks-utama pb-4 text-center space-y-1">
            <div className="flex items-center justify-center gap-4">
              <div className="w-16 h-16 shrink-0 flex items-center justify-center">
                <img
                  src="/logo/logo-alihsan.jpg"
                  alt="Logo SMA Al-Ihsan"
                  className="w-full h-full object-contain"
                />
              </div>
              <div className="text-center">
                <h2 className="text-sm font-bold text-teks-utama tracking-wider uppercase">
                  YAYASAN AL-IHSAN
                </h2>
                <h1 className="text-xl font-extrabold text-teks-utama tracking-tight">
                  SMA AL-IHSAN BOARDING SCHOOL
                </h1>
                <p className="text-[11px] text-teks-sekunder">
                  NPSN: 20271890 | Jl. Pesantren Al-Ihsan, Selaawi - Garut
                </p>
                <p className="text-[11px] text-teks-sekunder font-mono">
                  Email: info@sma-alihsan.sch.id | Website: www.sma-alihsan.sch.id
                </p>
              </div>
            </div>
          </div>

          {/* Judul Laporan */}
          <div className="text-center space-y-1 pt-2">
            <h3 className="font-bold text-base text-teks-utama uppercase tracking-wider underline">
              LAPORAN HASIL PENILAIAN KINERJA GURU (METODE MOORA)
            </h3>
            <p className="text-xs font-semibold text-teks-utama">
              PERIODE: {selectedPeriode?.namaPeriode?.toUpperCase()}
            </p>
          </div>

          {/* Keterangan Kriteria */}
          <div className="p-3.5 rounded-xl bg-latar-soft border border-hijau-muda/60 text-[11px] space-y-1 print:bg-transparent">
            <p className="font-bold text-teks-utama">Ketentuan Bobot & Kriteria Penilaian:</p>
            <p className="text-teks-sekunder">
              C1: Kehadiran (35%, Benefit) | C2: Ketepatan Waktu (25%, Benefit) | C3: Kelengkapan Perangkat Pembelajaran (25%, Benefit) | C4: Kelengkapan Administrasi Penilaian (15%, Benefit)
            </p>
          </div>

          {/* Tabel Hasil Penilaian Laporan */}
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs border border-gray-300">
              <thead className="bg-gray-100 border-b border-gray-300 font-bold uppercase text-[11px]">
                <tr>
                  <th className="py-2.5 px-2 text-center border-r border-gray-300 w-10">No</th>
                  <th className="py-2.5 px-3 border-r border-gray-300">Nama Guru & NIP</th>
                  <th className="py-2.5 px-3 border-r border-gray-300">Mata Pelajaran</th>
                  <th className="py-2.5 px-2 text-center border-r border-gray-300">C1</th>
                  <th className="py-2.5 px-2 text-center border-r border-gray-300">C2</th>
                  <th className="py-2.5 px-2 text-center border-r border-gray-300">C3</th>
                  <th className="py-2.5 px-2 text-center border-r border-gray-300">C4</th>
                  <th className="py-2.5 px-3 text-center border-r border-gray-300">Nilai MOORA</th>
                  <th className="py-2.5 px-2 text-center border-r border-gray-300">Rank</th>
                  <th className="py-2.5 px-3 text-center">Predikat</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200">
                {loading ? (
                  <tr>
                    <td colSpan={10} className="text-center py-6 text-teks-sekunder">
                      Memuat laporan...
                    </td>
                  </tr>
                ) : !laporanData || laporanData.length === 0 ? (
                  <tr>
                    <td colSpan={10} className="text-center py-6 text-teks-sekunder">
                      Belum ada data nilai tersimpan pada periode ini.
                    </td>
                  </tr>
                ) : (
                  laporanData.map((row: any) => {
                    const mapSkor: Record<string, number> = {};
                    row.details.forEach((d: any) => {
                      mapSkor[d.kriteria.kode] = d.nilaiAwal;
                    });

                    const rataRata = (mapSkor['C1'] + mapSkor['C2'] + mapSkor['C3'] + mapSkor['C4']) / 4;
                    const predikat = getPredikatNilai(rataRata);

                    return (
                      <tr key={row.id} className="hover:bg-gray-50">
                        <td className="py-2 px-2 text-center border-r border-gray-200">{row.ranking}</td>
                        <td className="py-2 px-3 border-r border-gray-200">
                          <div className="font-bold">{row.guru.nama}</div>
                          <div className="text-[10px] font-mono text-gray-500">{row.guru.nip}</div>
                        </td>
                        <td className="py-2 px-3 border-r border-gray-200 text-gray-700">
                          {row.guru.jabatanTugasMengajar}
                        </td>
                        <td className="py-2 px-2 text-center border-r border-gray-200 font-semibold">{mapSkor['C1']}</td>
                        <td className="py-2 px-2 text-center border-r border-gray-200 font-semibold">{mapSkor['C2']}</td>
                        <td className="py-2 px-2 text-center border-r border-gray-200 font-semibold">{mapSkor['C3']}</td>
                        <td className="py-2 px-2 text-center border-r border-gray-200 font-semibold">{mapSkor['C4']}</td>
                        <td className="py-2 px-3 text-center border-r border-gray-200 font-mono font-bold">
                          {row.nilaiPreferensi.toFixed(4)}
                        </td>
                        <td className="py-2 px-2 text-center border-r border-gray-200 font-bold">
                          #{row.ranking}
                        </td>
                        <td className="py-2 px-3 text-center font-semibold">{predikat.label}</td>
                      </tr>
                    );
                  })
                )}
              </tbody>
            </table>
          </div>

          {/* Tanda Tangan */}
          <div className="pt-8 flex justify-between items-start text-xs text-teks-utama break-inside-avoid">
            <div className="text-center space-y-16">
              <p>
                Mengetahui,<br />
                <strong>Administrator SPK</strong>
              </p>
              <div>
                <p className="font-bold underline">M. Hidad Abdillah, S.Pd.</p>
                <p className="text-[11px] text-teks-sekunder">SMA Al-Ihsan Boarding School</p>
              </div>
            </div>

            <div className="text-center space-y-16">
              <p>
                Bandung, {formatTanggalIndonesia(new Date())}<br />
                <strong>Kepala SMA Al-Ihsan Boarding School</strong>
              </p>
              <div>
                <p className="font-bold underline">Dr. H. Mulyadi, M.Pd.</p>
                <p className="text-[11px] font-mono text-teks-sekunder">NIP. 197508122000031002</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </AppLayout>
  );
}
