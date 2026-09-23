import os
import sqlite3
import datetime
from PIL import Image, ImageDraw, ImageFont

os.makedirs("system_screenshots", exist_ok=True)

def get_font(size=14, bold=False):
    font_names = [
        "segoeuib.ttf" if bold else "segoeui.ttf",
        "arialbd.ttf" if bold else "arial.ttf",
        "calibrib.ttf" if bold else "calibri.ttf",
        "tahomabd.ttf" if bold else "tahoma.ttf"
    ]
    for fn in font_names:
        try:
            return ImageFont.truetype(fn, size)
        except Exception:
            continue
    return ImageFont.load_default()

def draw_rounded_rect(draw, box, radius, fill, outline=None, width=1):
    x1, y1, x2, y2 = box
    draw.rounded_rectangle([x1, y1, x2, y2], radius=radius, fill=fill, outline=outline, width=width)

def draw_centered_in_box(draw, box, text, fill, font):
    x1, y1, x2, y2 = box
    cx = (x1 + x2) / 2
    cy = (y1 + y2) / 2
    bbox = draw.textbbox((0, 0), text, font=font)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    draw.text((cx - w / 2, cy - h / 2 - 1), text, fill=fill, font=font)

def draw_browser_chrome(draw, w, scale, url_path="http://localhost:3000/kepala-sekolah/dashboard"):
    def S(v): return int(v * scale)
    
    # Top title bar
    draw.rectangle([(0, 0), (S(w), S(42))], fill="#1E293B")
    draw.ellipse([(S(16), S(15)), (S(26), S(25))], fill="#EF4444")
    draw.ellipse([(S(32), S(15)), (S(42), S(25))], fill="#F59E0B")
    draw.ellipse([(S(48), S(15)), (S(58), S(25))], fill="#10B981")
    
    # Browser Tab
    draw_rounded_rect(draw, (S(75), S(8), S(350), S(42)), radius=S(6), fill="#0F172A", outline="#334155", width=S(1))
    draw.ellipse([(S(88), S(19)), (S(100), S(31))], fill="#059669")
    draw.text((S(108), S(15)), "SPK Penilaian Guru - SMA Al-Ihsan", fill="#F1F5F9", font=get_font(11 * scale, bold=True))
    
    # URL bar
    draw.rectangle([(0, S(42)), (S(w), S(80))], fill="#0F172A", outline="#1E293B", width=S(1))
    draw.text((S(16), S(52)), "<", fill="#94A3B8", font=get_font(14 * scale, bold=True))
    draw.text((S(38), S(52)), ">", fill="#64748B", font=get_font(14 * scale, bold=True))
    draw.text((S(60), S(52)), "⟳", fill="#94A3B8", font=get_font(14 * scale, bold=True))
    
    draw_rounded_rect(draw, (S(90), S(48), S(w - 180), S(74)), radius=S(4), fill="#1E293B", outline="#334155", width=S(1))
    draw.text((S(105), S(53)), "🔒", fill="#10B981", font=get_font(10 * scale))
    draw.text((S(125), S(53)), url_path, fill="#E2E8F0", font=get_font(11 * scale))
    
    draw_rounded_rect(draw, (S(w - 165), S(48), S(w - 16), S(74)), radius=S(4), fill="#064E3B", outline="#059669", width=S(1))
    draw.text((S(w - 150), S(54)), "● Server: Online", fill="#34D399", font=get_font(10 * scale, bold=True))

def draw_app_header(draw, w, h, scale, title="Dashboard Kepala Sekolah", subtitle="Ringkasan evaluasi kinerja guru & rekomendasi keputusan", role="Kepala Sekolah", namaUser="Dr. H. Mulyadi, M.Pd.", periode="Juni 2026"):
    def S(v): return int(v * scale)
    top_y = 80
    
    draw.rectangle([(S(240), S(top_y)), (S(w), S(top_y + 64))], fill="#FFFFFF", outline="#E2E8F0", width=S(1))
    draw.text((S(260), S(top_y + 12)), title, fill="#0F172A", font=get_font(16 * scale, bold=True))
    if subtitle:
        draw.text((S(260), S(top_y + 36)), subtitle, fill="#64748B", font=get_font(11 * scale))
        
    draw_rounded_rect(draw, (S(w - 390), S(top_y + 16), S(w - 220), S(top_y + 48)), radius=S(6), fill="#ECFDF5", outline="#A7F3D0", width=S(1))
    draw.text((S(w - 378), S(top_y + 23)), f"📅 Periode: {periode}", fill="#065F46", font=get_font(11 * scale, bold=True))
    
    draw_rounded_rect(draw, (S(w - 205), S(top_y + 14), S(w - 20), S(top_y + 50)), radius=S(6), fill="#F8FAFC", outline="#CBD5E1", width=S(1))
    draw.ellipse([(S(w - 195), S(top_y + 22)), (S(w - 175), S(top_y + 42))], fill="#059669")
    draw.text((S(w - 190), S(top_y + 23)), role[0], fill="#FFFFFF", font=get_font(11 * scale, bold=True))
    draw.text((S(w - 168), S(top_y + 18)), namaUser[:16], fill="#0F172A", font=get_font(10 * scale, bold=True))
    draw.text((S(w - 168), S(top_y + 32)), f"Role: {role}", fill="#059669", font=get_font(9 * scale))

def draw_app_sidebar(draw, h, scale, active_menu="Dashboard", role="KEPALA_SEKOLAH"):
    def S(v): return int(v * scale)
    top_y = 80
    
    draw.rectangle([(0, S(top_y)), (S(240), S(h))], fill="#064E3B", outline="#047857", width=S(1))
    
    draw.rectangle([(0, S(top_y)), (S(240), S(top_y + 70))], fill="#022C22")
    draw.rectangle([(S(15), S(top_y + 15)), (S(55), S(top_y + 55))], fill="#059669")
    draw_centered_in_box(draw, (S(15), S(top_y + 15), S(55), S(top_y + 55)), "IHSAN", "#FFFFFF", get_font(9 * scale, bold=True))
    draw.text((S(65), S(top_y + 16)), "SMA AL-IHSAN", fill="#FFFFFF", font=get_font(12 * scale, bold=True))
    draw.text((S(65), S(top_y + 34)), "Boarding School", fill="#A7F3D0", font=get_font(10 * scale))
    draw.text((S(65), S(top_y + 48)), "SPK Penilaian Guru", fill="#6EE7B7", font=get_font(9 * scale))
    
    if role == "KEPALA_SEKOLAH":
        nav_sections = [
            ("MENU UTAMA", [
                ("Dashboard", "Dashboard", "📊"),
                ("Penilaian Guru", "Penilaian", "✍️"),
                ("Monitoring Kinerja", "Monitoring", "📈"),
            ]),
            ("LAPORAN & KEPUTUSAN", [
                ("Peringkat & Hasil", "Ranking", "🏆"),
                ("Laporan Resmi", "Laporan", "🖨️"),
                ("Riwayat Evaluasi", "Riwayat", "📜"),
            ])
        ]
    elif role == "GURU":
        nav_sections = [
            ("PORTAL PENDIDIK", [
                ("Dashboard & Profil", "Dashboard", "📊"),
                ("Riwayat Evaluasi", "Riwayat", "📜"),
                ("Detail Nilai & Saran", "Detail", "📑"),
            ])
        ]
    else:
        nav_sections = [
            ("NAVIGASI UTAMA", [
                ("Dashboard", "Dashboard", "📊"),
            ])
        ]
        
    cur_y = top_y + 82
    for sec_title, items in nav_sections:
        draw.text((S(18), S(cur_y)), sec_title, fill="#6EE7B7", font=get_font(9 * scale, bold=True))
        cur_y += 20
        for label, key, icon in items:
            is_active = (key == active_menu or label == active_menu)
            if is_active:
                draw_rounded_rect(draw, (S(12), S(cur_y - 4), S(228), S(cur_y + 24)), radius=S(6), fill="#059669")
                draw.text((S(22), S(cur_y)), f"{icon}  {label}", fill="#FFFFFF", font=get_font(11 * scale, bold=True))
            else:
                draw.text((S(22), S(cur_y)), f"{icon}  {label}", fill="#D1FAE5", font=get_font(11 * scale))
            cur_y += 30
        cur_y += 10

# -------------------------------------------------------------
# KEPALA SEKOLAH: 1. Dashboard Kepala Sekolah
# -------------------------------------------------------------
def generate_sys_kepsek_01_dashboard():
    scale = 2
    w, h = 1300, 720
    img = Image.new("RGB", (w * scale, h * scale), "#F8FAFC")
    draw = ImageDraw.Draw(img)
    def S(v): return int(v * scale)
    
    draw_browser_chrome(draw, w, scale, "http://localhost:3000/kepala-sekolah/dashboard")
    draw_app_header(draw, w, h, scale, "Dashboard Kepala Sekolah", "Pusat monitoring evaluasi kinerja guru & rekomendasi keputusan MOORA", "Kepala Sekolah", "Dr. H. Mulyadi, M.Pd.", "Juni 2026")
    draw_app_sidebar(draw, h, scale, active_menu="Dashboard", role="KEPALA_SEKOLAH")
    
    content_x = 260
    content_w = w - content_x - 20
    
    # 4 Stat Cards
    card_w = (content_w - 36) // 4
    stats = [
        ("TOTAL GURU AKTIF", "18 Guru", "Seluruh Pendidik Terdaftar", "#059669", "#ECFDF5", "👨‍🏫"),
        ("SUDAH DINILAI KEPSEK", "18 Guru", "Penilaian Selesai 100%", "#2563EB", "#EFF6FF", "✅"),
        ("BELUM DINILAI", "0 Guru", "Tidak Ada Antrean Evaluasi", "#D97706", "#FFFBEB", "⏳"),
        ("PERIODE AKTIF", "Juni 2026", "Status: AKTIF", "#7C3AED", "#F5F3FF", "📅"),
    ]
    for i, (stitle, sval, ssub, c_accent, c_bg, icon) in enumerate(stats):
        cx1 = content_x + i * (card_w + 12)
        cx2 = cx1 + card_w
        draw_rounded_rect(draw, (S(cx1), S(158), S(cx2), S(248)), radius=S(8), fill="#FFFFFF", outline="#E2E8F0", width=S(1))
        draw_rounded_rect(draw, (S(cx1), S(158), S(cx2), S(162)), radius=S(2), fill=c_accent)
        draw_rounded_rect(draw, (S(cx2 - 48), S(172), S(cx2 - 14), S(206)), radius=S(6), fill=c_bg)
        draw_centered_in_box(draw, (S(cx2 - 48), S(172), S(cx2 - 14), S(206)), icon, c_accent, get_font(12 * scale))
        draw.text((S(cx1 + 16), S(172)), stitle, fill="#64748B", font=get_font(9 * scale, bold=True))
        draw.text((S(cx1 + 16), S(190)), sval, fill="#0F172A", font=get_font(16 * scale, bold=True))
        draw.text((S(cx1 + 16), S(224)), ssub, fill="#059669" if i < 2 else "#64748B", font=get_font(9 * scale))
        
    # Status Penilaian & Quick Action
    draw_rounded_rect(draw, (S(content_x), S(260), S(w - 20), S(370)), radius=S(8), fill="#FFFFFF", outline="#E2E8F0", width=S(1))
    draw.text((S(content_x + 20), S(275)), "📋 Progres Evaluasi Penilaian Guru Periode Juni 2026", fill="#0F172A", font=get_font(13 * scale, bold=True))
    draw.text((S(content_x + 20), S(298)), "Kepala Sekolah telah menyelesaikan penginputan skor 18 dari 18 guru aktif. Hasil optimasi MOORA telah siap dianalisis dan disahkan.", fill="#475569", font=get_font(10 * scale))
    
    draw_rounded_rect(draw, (S(content_x + 20), S(324), S(content_x + 650), S(340)), radius=S(4), fill="#059669")
    draw.text((S(content_x + 665), S(324)), "100% Selesai Dinilai", fill="#059669", font=get_font(11 * scale, bold=True))
    
    draw_rounded_rect(draw, (S(w - 380), S(314), S(w - 210), S(350)), radius=S(6), fill="#059669")
    draw_centered_in_box(draw, (S(w - 380), S(314), S(w - 210), S(350)), "✍️ Input Penilaian Guru", "#FFFFFF", get_font(10 * scale, bold=True))
    draw_rounded_rect(draw, (S(w - 195), S(314), S(w - 35), S(350)), radius=S(6), fill="#F8FAFC", outline="#CBD5E1", width=S(1))
    draw_centered_in_box(draw, (S(w - 195), S(314), S(w - 35), S(350)), "Lihat Rekomendasi →", "#0F172A", get_font(10 * scale, bold=True))
    
    # 2 Split Cards: Top 3 & Catatan Pengesahan
    split_w = (content_w - 16) // 2
    draw_rounded_rect(draw, (S(content_x), S(385), S(content_x + split_w), S(690)), radius=S(8), fill="#FFFFFF", outline="#E2E8F0", width=S(1))
    draw.rectangle([(S(content_x), S(385)), (S(content_x + split_w), S(425))], fill="#F8FAFC")
    draw.line([(S(content_x), S(425)), (S(content_x + split_w), S(425))], fill="#E2E8F0", width=S(1))
    draw.text((S(content_x + 18), S(397)), "🏆 Rekomendasi 3 Guru Berkinerja Terbaik", fill="#0F172A", font=get_font(12 * scale, bold=True))
    
    top_3 = [
        ("1", "Ahmad Fauzi, S.Pd.", "Guru Matematika", "Yi: 0.2754", "🥇 Juara 1"),
        ("2", "Siti Nurhaliza, M.Pd.", "Guru Bahasa Indonesia", "Yi: 0.2669", "🥈 Juara 2"),
        ("3", "Budi Santoso, S.Si.", "Guru Fisika", "Yi: 0.2616", "🥉 Juara 3"),
    ]
    for idx, (rk, gname, gmapel, gyi, medal) in enumerate(top_3):
        gy = 440 + idx * 76
        draw_rounded_rect(draw, (S(content_x + 16), S(gy), S(content_x + split_w - 16), S(gy + 66)), radius=S(6), fill="#F8FAFC", outline="#E2E8F0", width=S(1))
        draw_rounded_rect(draw, (S(content_x + 26), S(gy + 14), S(content_x + 66), S(gy + 52)), radius=S(6), fill="#FEF3C7" if idx==0 else "#EFF6FF")
        draw_centered_in_box(draw, (S(content_x + 26), S(gy + 14), S(content_x + 66), S(gy + 52)), f"#{rk}", "#D97706" if idx==0 else "#2563EB", get_font(13 * scale, bold=True))
        draw.text((S(content_x + 78), S(gy + 12)), gname, fill="#0F172A", font=get_font(11 * scale, bold=True))
        draw.text((S(content_x + 78), S(gy + 30)), gmapel, fill="#64748B", font=get_font(9 * scale))
        draw.text((S(content_x + 78), S(gy + 46)), f"Nilai Preferensi: {gyi} (Sangat Baik)", fill="#059669", font=get_font(9 * scale, bold=True))
        
    # Right: Petunjuk Pengesahan Kepala Sekolah
    draw_rounded_rect(draw, (S(content_x + split_w + 16), S(385), S(w - 20), S(690)), radius=S(8), fill="#FFFFFF", outline="#E2E8F0", width=S(1))
    draw.rectangle([(S(content_x + split_w + 16), S(385)), (S(w - 20), S(425))], fill="#F8FAFC")
    draw.line([(S(content_x + split_w + 16), S(425)), (S(w - 20), S(425))], fill="#E2E8F0", width=S(1))
    draw.text((S(content_x + split_w + 34), S(397)), "📑 Lembar Kerja & Wewenang Kepala Sekolah", fill="#0F172A", font=get_font(12 * scale, bold=True))
    
    guidelines = [
        ("1. Input Penilaian", "Melakukan penilaian objektif berbasis rubrik 1-5 untuk kriteria C1 s.d. C4.", "#059669"),
        ("2. Monitoring Kinerja", "Memantau grafik fluktuasi kompetensi guru dari bulan ke bulan.", "#2563EB"),
        ("3. Verifikasi & Pengesahan", "Meninjau laporan rekapitulasi penilaian sebelum ditandatangani resmi.", "#D97706"),
        ("4. Umpan Balik Pembinaan", "Memberikan catatan rekomendasi kualitatif kepada masing-masing guru.", "#7C3AED"),
    ]
    for idx, (ghead, gdesc, gcol) in enumerate(guidelines):
        ly = 440 + idx * 58
        draw.ellipse([(S(content_x + split_w + 36), S(ly + 6)), (S(content_x + split_w + 46), S(ly + 16))], fill=gcol)
        draw.text((S(content_x + split_w + 56), S(ly)), ghead, fill=gcol, font=get_font(10 * scale, bold=True))
        draw.text((S(content_x + split_w + 56), S(ly + 18)), gdesc, fill="#475569", font=get_font(9 * scale))
        if idx < 3:
            draw.line([(S(content_x + split_w + 56), S(ly + 48)), (S(w - 40), S(ly + 48))], fill="#F1F5F9", width=S(1))

    out_p = "system_screenshots/img_sys_kepsek_01_dashboard.png"
    img.save(out_p, quality=95)
    return out_p

# -------------------------------------------------------------
# KEPALA SEKOLAH: 2. Monitoring & Grafik Kinerja Guru
# -------------------------------------------------------------
def generate_sys_kepsek_02_monitoring():
    scale = 2
    w, h = 1300, 720
    img = Image.new("RGB", (w * scale, h * scale), "#F8FAFC")
    draw = ImageDraw.Draw(img)
    def S(v): return int(v * scale)
    
    draw_browser_chrome(draw, w, scale, "http://localhost:3000/kepala-sekolah/monitoring")
    draw_app_header(draw, w, h, scale, "Monitoring & Analisis Kinerja Guru", "Grafik tren perkembangan nilai kompetensi & preferensi MOORA", "Kepala Sekolah", "Dr. H. Mulyadi, M.Pd.", "Juni 2026")
    draw_app_sidebar(draw, h, scale, active_menu="Monitoring", role="KEPALA_SEKOLAH")
    
    content_x = 260
    
    # Guru Selector Bar
    draw_rounded_rect(draw, (S(content_x), S(158), S(w - 20), S(215)), radius=S(8), fill="#FFFFFF", outline="#E2E8F0", width=S(1))
    draw.text((S(content_x + 20), S(176)), "Pilih Tenaga Pendidik:", fill="#0F172A", font=get_font(11 * scale, bold=True))
    draw_rounded_rect(draw, (S(content_x + 180), S(168), S(content_x + 480), S(205)), radius=S(6), fill="#F8FAFC", outline="#CBD5E1", width=S(1))
    draw.text((S(content_x + 195), S(178)), "👤 Ahmad Fauzi, S.Pd. (198501152010011001)", fill="#0F172A", font=get_font(10 * scale, bold=True))
    
    draw.text((S(content_x + 520), S(176)), "Mata Pelajaran: Guru Matematika • Tugas Tambahan: Wakasek Kurikulum", fill="#64748B", font=get_font(9 * scale))
    
    # Chart Area Card
    draw_rounded_rect(draw, (S(content_x), S(230), S(w - 20), S(690)), radius=S(8), fill="#FFFFFF", outline="#E2E8F0", width=S(1))
    draw.text((S(content_x + 20), S(248)), "📈 Grafik Perkembangan Skor Kriteria & Nilai Preferensi MOORA (Mei - Juni 2026)", fill="#0F172A", font=get_font(12 * scale, bold=True))
    
    # Draw Mock Line Chart
    chart_x1 = content_x + 60
    chart_y1 = 290
    chart_x2 = w - 60
    chart_y2 = 520
    
    # Grid lines
    for i in range(5):
        gy = chart_y1 + i * 55
        draw.line([(S(chart_x1), S(gy)), (S(chart_x2), S(gy))], fill="#F1F5F9", width=S(1))
        draw.text((S(chart_x1 - 35), S(gy - 8)), f"Skor {5 - i}", fill="#94A3B8", font=get_font(9 * scale))
        
    # Periods on X axis
    draw.text((S(chart_x1 + 180), S(chart_y2 + 15)), "Periode Mei 2026", fill="#0F172A", font=get_font(11 * scale, bold=True))
    draw.text((S(chart_x2 - 280), S(chart_y2 + 15)), "Periode Juni 2026", fill="#0F172A", font=get_font(11 * scale, bold=True))
    
    # Trend Lines (C1: Green, C2: Blue, C3: Orange, C4: Purple, Yi: Emerald Thick)
    # Line 1: C1 Kehadiran (5.0 -> 5.0)
    draw.line([(S(chart_x1 + 220), S(chart_y1)), (S(chart_x2 - 220), S(chart_y1))], fill="#059669", width=S(3))
    draw.ellipse([(S(chart_x1 + 215), S(chart_y1 - 5)), (S(chart_x1 + 225), S(chart_y1 + 5))], fill="#059669")
    draw.ellipse([(S(chart_x2 - 225), S(chart_y1 - 5)), (S(chart_x2 - 215), S(chart_y1 + 5))], fill="#059669")
    
    # Line 2: C2 Ketepatan Waktu (4.5 -> 5.0)
    draw.line([(S(chart_x1 + 220), S(chart_y1 + 28)), (S(chart_x2 - 220), S(chart_y1))], fill="#2563EB", width=S(3))
    draw.ellipse([(S(chart_x1 + 215), S(chart_y1 + 23)), (S(chart_x1 + 225), S(chart_y1 + 33))], fill="#2563EB")
    
    # Line 3: C4 Administrasi (4.0 -> 4.0)
    draw.line([(S(chart_x1 + 220), S(chart_y1 + 55)), (S(chart_x2 - 220), S(chart_y1 + 55))], fill="#7C3AED", width=S(3))
    draw.ellipse([(S(chart_x1 + 215), S(chart_y1 + 50)), (S(chart_x1 + 225), S(chart_y1 + 60))], fill="#7C3AED")
    draw.ellipse([(S(chart_x2 - 225), S(chart_y1 + 50)), (S(chart_x2 - 215), S(chart_y1 + 60))], fill="#7C3AED")
    
    # Legend at bottom
    draw_rounded_rect(draw, (S(content_x + 20), S(575), S(w - 40), S(660)), radius=S(6), fill="#F8FAFC", outline="#E2E8F0", width=S(1))
    legends = [
        ("C1 Kehadiran (35%)", "#059669"),
        ("C2 Ketepatan Waktu (25%)", "#2563EB"),
        ("C3 Perangkat Pembelajaran (25%)", "#D97706"),
        ("C4 Administrasi Penilaian (15%)", "#7C3AED"),
        ("Nilai MOORA Yi: 0.2754 (Rank #1)", "#0F172A"),
    ]
    cur_lx = content_x + 40
    for ltxt, lcol in legends:
        draw.rectangle([(S(cur_lx), S(605)), (S(cur_lx + 16), S(615))], fill=lcol)
        draw.text((S(cur_lx + 24), S(600)), ltxt, fill="#334155", font=get_font(10 * scale, bold=True))
        cur_lx += len(ltxt) * 7 + 55

    out_p = "system_screenshots/img_sys_kepsek_02_monitoring.png"
    img.save(out_p, quality=95)
    return out_p

# -------------------------------------------------------------
# GURU: 1. Riwayat Penilaian Kinerja Mandiri
# -------------------------------------------------------------
def generate_sys_guru_01_riwayat():
    scale = 2
    w, h = 1300, 720
    img = Image.new("RGB", (w * scale, h * scale), "#F8FAFC")
    draw = ImageDraw.Draw(img)
    def S(v): return int(v * scale)
    
    draw_browser_chrome(draw, w, scale, "http://localhost:3000/guru/riwayat")
    draw_app_header(draw, w, h, scale, "Riwayat & Arsip Evaluasi Kinerja Guru", "Arsip historis pencapaian skor penilaian kinerja antar periode", "Guru", "Ahmad Fauzi, S.Pd.", "Juni 2026")
    draw_app_sidebar(draw, h, scale, active_menu="Riwayat", role="GURU")
    
    content_x = 260
    
    # Table Card Container
    draw_rounded_rect(draw, (S(content_x), S(158), S(w - 20), S(690)), radius=S(8), fill="#FFFFFF", outline="#E2E8F0", width=S(1))
    draw.text((S(content_x + 20), S(176)), "Histori Hasil Penilaian Kinerja (Ahmad Fauzi, S.Pd. - NIP: 198501152010011001)", fill="#0F172A", font=get_font(13 * scale, bold=True))
    
    ty = 220
    draw.rectangle([(S(content_x), S(ty)), (S(w - 20), S(ty + 40))], fill="#F8FAFC")
    draw.line([(S(content_x), S(ty + 40)), (S(w - 20), S(ty + 40))], fill="#CBD5E1", width=S(1))
    
    cols = [("PERIODE EVALUASI", 160), ("C1 (35%)", 85), ("C2 (25%)", 85), ("C3 (25%)", 85), ("C4 (15%)", 85), ("NILAI MOORA (Yi)", 150), ("PERINGKAT", 120), ("CATATAN KEPSEK", 230)]
    cur_x = content_x + 15
    for cname, cw in cols:
        draw.text((S(cur_x), S(ty + 12)), cname, fill="#475569", font=get_font(9 * scale, bold=True))
        cur_x += cw
        
    riwayat_rows = [
        ("Juni 2026 (Aktif)", "5.0", "5.0", "5.0", "4.0", "0.2754", "🥇 Rank #1", "Kinerja teladan dan sangat konsisten.", "#FEF3C7", "#D97706"),
        ("Mei 2026", "5.0", "4.8", "5.0", "4.0", "0.2669", "🥈 Rank #2", "Perangkat ajar lengkap dan disiplin mengajar tinggi.", "#EFF6FF", "#1E40AF"),
    ]
    for idx, (prd, c1, c2, c3, c4, yi, rk, ctt, bg_r, txt_r) in enumerate(riwayat_rows):
        ry = ty + 40 + idx * 85
        draw.line([(S(content_x), S(ry + 85)), (S(w - 20), S(ry + 85))], fill="#F1F5F9", width=S(1))
        
        draw.text((S(content_x + 15), S(ry + 24)), prd, fill="#0F172A", font=get_font(12 * scale, bold=True))
        draw.text((S(content_x + 185), S(ry + 26)), c1, fill="#059669", font=get_font(12 * scale, bold=True))
        draw.text((S(content_x + 270), S(ry + 26)), c2, fill="#059669", font=get_font(12 * scale, bold=True))
        draw.text((S(content_x + 355), S(ry + 26)), c3, fill="#059669", font=get_font(12 * scale, bold=True))
        draw.text((S(content_x + 440), S(ry + 26)), c4, fill="#059669", font=get_font(12 * scale, bold=True))
        
        # Nilai MOORA
        draw_rounded_rect(draw, (S(content_x + 515), S(ry + 18), S(content_x + 630), S(ry + 52)), radius=S(4), fill="#ECFDF5", outline="#A7F3D0", width=S(1))
        draw_centered_in_box(draw, (S(content_x + 515), S(ry + 18), S(content_x + 630), S(ry + 52)), yi, "#065F46", get_font(11 * scale, bold=True))
        
        # Rank Badge
        draw_rounded_rect(draw, (S(content_x + 655), S(ry + 18), S(content_x + 750), S(ry + 52)), radius=S(4), fill=bg_r, outline="#CBD5E1", width=S(1))
        draw_centered_in_box(draw, (S(content_x + 655), S(ry + 18), S(content_x + 750), S(ry + 52)), rk, txt_r, get_font(10 * scale, bold=True))
        
        # Catatan
        draw.text((S(content_x + 775), S(ry + 24)), ctt, fill="#334155", font=get_font(10 * scale))

    out_p = "system_screenshots/img_sys_guru_01_riwayat.png"
    img.save(out_p, quality=95)
    return out_p

if __name__ == "__main__":
    p1 = generate_sys_kepsek_01_dashboard()
    p2 = generate_sys_kepsek_02_monitoring()
    p3 = generate_sys_guru_01_riwayat()
    print("Kepala Sekolah & Guru screenshots generated successfully!")
