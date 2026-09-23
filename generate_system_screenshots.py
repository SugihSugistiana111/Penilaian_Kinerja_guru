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

def draw_browser_chrome(draw, w, scale, url_path="http://localhost:3000/admin/dashboard"):
    def S(v): return int(v * scale)
    
    # Top title bar
    draw.rectangle([(0, 0), (S(w), S(42))], fill="#1E293B")
    
    # Traffic light buttons
    draw.ellipse([(S(16), S(15)), (S(26), S(25))], fill="#EF4444")
    draw.ellipse([(S(32), S(15)), (S(42), S(25))], fill="#F59E0B")
    draw.ellipse([(S(48), S(15)), (S(58), S(25))], fill="#10B981")
    
    # Browser Tab
    draw_rounded_rect(draw, (S(75), S(8), S(340), S(42)), radius=S(6), fill="#0F172A", outline="#334155", width=S(1))
    draw.ellipse([(S(88), S(19)), (S(100), S(31))], fill="#059669")
    draw.text((S(108), S(15)), "SPK Penilaian Kinerja Guru - SMA Al-Ihsan", fill="#F1F5F9", font=get_font(11 * scale, bold=True))
    
    # URL bar
    draw.rectangle([(0, S(42)), (S(w), S(80))], fill="#0F172A", outline="#1E293B", width=S(1))
    
    # Navigation icons (Back, Forward, Refresh)
    draw.text((S(16), S(52)), "<", fill="#94A3B8", font=get_font(14 * scale, bold=True))
    draw.text((S(38), S(52)), ">", fill="#64748B", font=get_font(14 * scale, bold=True))
    draw.text((S(60), S(52)), "⟳", fill="#94A3B8", font=get_font(14 * scale, bold=True))
    
    # Address bar container
    draw_rounded_rect(draw, (S(90), S(48), S(w - 180), S(74)), radius=S(4), fill="#1E293B", outline="#334155", width=S(1))
    draw.text((S(105), S(53)), "🔒", fill="#10B981", font=get_font(10 * scale))
    draw.text((S(125), S(53)), url_path, fill="#E2E8F0", font=get_font(11 * scale))
    
    # User status badge
    draw_rounded_rect(draw, (S(w - 165), S(48), S(w - 16), S(74)), radius=S(4), fill="#064E3B", outline="#059669", width=S(1))
    draw.text((S(w - 150), S(54)), "● Server: Online", fill="#34D399", font=get_font(10 * scale, bold=True))

def draw_app_header(draw, w, h, scale, title="Dashboard Administrator", subtitle="Ringkasan evaluasi kinerja guru & status MOORA", role="Administrator", namaUser="Administrator Utama", periode="Juni 2026"):
    def S(v): return int(v * scale)
    top_y = 80
    
    # Header bar
    draw.rectangle([(S(240), S(top_y)), (S(w), S(top_y + 64))], fill="#FFFFFF", outline="#E2E8F0", width=S(1))
    
    # Title & subtitle
    draw.text((S(260), S(top_y + 12)), title, fill="#0F172A", font=get_font(16 * scale, bold=True))
    if subtitle:
        draw.text((S(260), S(top_y + 36)), subtitle, fill="#64748B", font=get_font(11 * scale))
        
    # Active Period Badge
    draw_rounded_rect(draw, (S(w - 380), S(top_y + 16), S(w - 210), S(top_y + 48)), radius=S(6), fill="#ECFDF5", outline="#A7F3D0", width=S(1))
    draw.text((S(w - 368), S(top_y + 23)), f"📅 Periode: {periode}", fill="#065F46", font=get_font(11 * scale, bold=True))
    
    # User Badge
    draw_rounded_rect(draw, (S(w - 195), S(top_y + 14), S(w - 20), S(top_y + 50)), radius=S(6), fill="#F8FAFC", outline="#CBD5E1", width=S(1))
    draw.ellipse([(S(w - 185), S(top_y + 22)), (S(w - 165), S(top_y + 42))], fill="#059669")
    draw.text((S(w - 180), S(top_y + 23)), role[0], fill="#FFFFFF", font=get_font(11 * scale, bold=True))
    draw.text((S(w - 158), S(top_y + 18)), namaUser[:14], fill="#0F172A", font=get_font(10 * scale, bold=True))
    draw.text((S(w - 158), S(top_y + 32)), f"Role: {role}", fill="#059669", font=get_font(9 * scale))

def draw_app_sidebar(draw, h, scale, active_menu="Dashboard", role="ADMIN"):
    def S(v): return int(v * scale)
    top_y = 80
    
    # Sidebar Background (Emerald Dark / Navy)
    draw.rectangle([(0, S(top_y)), (S(240), S(h))], fill="#064E3B", outline="#047857", width=S(1))
    
    # School Brand in Sidebar
    draw.rectangle([(0, S(top_y)), (S(240), S(top_y + 70))], fill="#022C22")
    draw.rectangle([(S(15), S(top_y + 15)), (S(55), S(top_y + 55))], fill="#059669")
    draw_centered_in_box(draw, (S(15), S(top_y + 15), S(55), S(top_y + 55)), "IHSAN", "#FFFFFF", get_font(9 * scale, bold=True))
    draw.text((S(65), S(top_y + 16)), "SMA AL-IHSAN", fill="#FFFFFF", font=get_font(12 * scale, bold=True))
    draw.text((S(65), S(top_y + 34)), "Boarding School", fill="#A7F3D0", font=get_font(10 * scale))
    draw.text((S(65), S(top_y + 48)), "SPK Penilaian Guru", fill="#6EE7B7", font=get_font(9 * scale))
    
    # Nav items
    nav_sections = [
        ("NAVIGASI UTAMA", [
            ("Dashboard", "Dashboard", "📊"),
        ]),
        ("DATA MASTER", [
            ("Data Guru", "Guru", "👨‍🏫"),
            ("Kriteria & Bobot", "Kriteria", "⚖️"),
            ("Skala Penilaian", "Skala", "📑"),
            ("Periode Penilaian", "Periode", "📅"),
        ]),
        ("PENILAIAN & SPK", [
            ("Transaksi Penilaian", "Penilaian", "✍️"),
            ("Perhitungan MOORA", "MOORA", "🧮"),
            ("Peringkat & Ranking", "Ranking", "🏆"),
            ("Laporan & Cetak", "Laporan", "🖨️"),
        ]),
        ("PENGATURAN", [
            ("Kelola Pengguna", "Pengguna", "👥"),
            ("Log Aktivitas", "Log", "📜"),
        ])
    ]
    
    if role == "GURU":
        nav_sections = [
            ("PORTAL GURU", [
                ("Dashboard & Profil", "Dashboard", "📊"),
                ("Riwayat Penilaian", "Riwayat", "📜"),
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
# 1. Halaman Login
# -------------------------------------------------------------
def generate_sys_01_login():
    scale = 2
    w, h = 1200, 720
    img = Image.new("RGB", (w * scale, h * scale), "#F0FDF4")
    draw = ImageDraw.Draw(img)
    def S(v): return int(v * scale)
    
    draw_browser_chrome(draw, w, scale, "http://localhost:3000/login")
    
    # Background pattern / banner
    draw.rectangle([(0, S(80)), (S(w), S(h))], fill="#F8FAFC")
    draw.rectangle([(0, S(80)), (S(w), S(340))], fill="#064E3B")
    
    # Central Login Card
    cx, cy = w // 2, (h + 80) // 2
    cw, ch = 480, 480
    x1, y1 = cx - cw // 2, cy - ch // 2
    x2, y2 = cx + cw // 2, cy + ch // 2
    
    draw_rounded_rect(draw, (S(x1), S(y1), S(x2), S(y2)), radius=S(12), fill="#FFFFFF", outline="#E2E8F0", width=S(1))
    
    # Card Header
    draw_rounded_rect(draw, (S(cx - 36), S(y1 + 24), S(cx + 36), S(y1 + 84)), radius=S(10), fill="#059669")
    draw_centered_in_box(draw, (S(cx - 36), S(y1 + 24), S(cx + 36), S(y1 + 84)), "IHSAN", "#FFFFFF", get_font(14 * scale, bold=True))
    
    draw_centered_in_box(draw, (S(x1), S(y1 + 96), S(x2), S(y1 + 120)), "SMA AL-IHSAN BOARDING SCHOOL", "#0F172A", get_font(15 * scale, bold=True))
    draw_centered_in_box(draw, (S(x1), S(y1 + 122), S(x2), S(y1 + 142)), "Sistem Pendukung Keputusan Penilaian Kinerja Guru (MOORA)", "#059669", get_font(10 * scale, bold=True))
    draw_centered_in_box(draw, (S(x1), S(y1 + 144), S(x2), S(y1 + 162)), "Silakan masuk dengan akun terdaftar untuk mengakses sistem", "#64748B", get_font(10 * scale))
    
    # Form input fields
    fy = y1 + 175
    # Username
    draw.text((S(x1 + 40), S(fy)), "Username", fill="#334155", font=get_font(10 * scale, bold=True))
    draw_rounded_rect(draw, (S(x1 + 40), S(fy + 20), S(x2 - 40), S(fy + 58)), radius=S(6), fill="#F8FAFC", outline="#CBD5E1", width=S(1))
    draw.text((S(x1 + 54), S(fy + 30)), "admin", fill="#0F172A", font=get_font(11 * scale))
    
    # Password
    fy += 72
    draw.text((S(x1 + 40), S(fy)), "Password", fill="#334155", font=get_font(10 * scale, bold=True))
    draw_rounded_rect(draw, (S(x1 + 40), S(fy + 20), S(x2 - 40), S(fy + 58)), radius=S(6), fill="#F8FAFC", outline="#CBD5E1", width=S(1))
    draw.text((S(x1 + 54), S(fy + 32)), "••••••••••••••••", fill="#64748B", font=get_font(11 * scale))
    
    # Remember me & Role hints
    fy += 70
    draw_rounded_rect(draw, (S(x1 + 40), S(fy), S(x1 + 54), S(fy + 14)), radius=S(3), fill="#059669")
    draw.text((S(x1 + 62), S(fy)), "Ingat saya pada perangkat ini", fill="#475569", font=get_font(10 * scale))
    
    # Button Submit
    fy += 32
    draw_rounded_rect(draw, (S(x1 + 40), S(fy), S(x2 - 40), S(fy + 44)), radius=S(6), fill="#059669")
    draw_centered_in_box(draw, (S(x1 + 40), S(fy), S(x2 - 40), S(fy + 44)), "Masuk ke Sistem  →", "#FFFFFF", get_font(12 * scale, bold=True))
    
    # Demo credentials pill
    draw_rounded_rect(draw, (S(x1 + 30), S(y2 - 55), S(x2 - 30), S(y2 - 18)), radius=S(6), fill="#ECFDF5", outline="#A7F3D0", width=S(1))
    draw_centered_in_box(draw, (S(x1 + 30), S(y2 - 55), S(x2 - 30), S(y2 - 18)), "Hak Akses Multilevel: Administrator • Kepala Sekolah • Guru", "#065F46", get_font(9 * scale, bold=True))
    
    out_p = "system_screenshots/img_sys_01_login.png"
    img.save(out_p, quality=95)
    return out_p

# -------------------------------------------------------------
# 2. Dashboard Administrator
# -------------------------------------------------------------
def generate_sys_02_dashboard_admin():
    scale = 2
    w, h = 1300, 720
    img = Image.new("RGB", (w * scale, h * scale), "#F8FAFC")
    draw = ImageDraw.Draw(img)
    def S(v): return int(v * scale)
    
    draw_browser_chrome(draw, w, scale, "http://localhost:3000/admin/dashboard")
    draw_app_header(draw, w, h, scale, "Dashboard Administrator", "Ringkasan evaluasi kinerja guru dan status kesiapan MOORA", "Administrator", "Sugih Sugistiana (Admin)", "Juni 2026")
    draw_app_sidebar(draw, h, scale, active_menu="Dashboard")
    
    # Main Content Area
    content_x = 260
    content_w = w - content_x - 20
    
    # 4 Stat Cards
    card_w = (content_w - 36) // 4
    stats = [
        ("TOTAL GURU AKTIF", "18 Guru", "18 Tenaga Pendidik Terdaftar", "#059669", "#ECFDF5", "👨‍🏫"),
        ("SUDAH DINILAI", "18 Guru", "Kelengkapan Nilai 100%", "#2563EB", "#EFF6FF", "✅"),
        ("BELUM DINILAI", "0 Guru", "Semua Data Siap Dihitung", "#D97706", "#FFFBEB", "⏳"),
        ("PERIODE AKTIF", "Juni 2026", "Status Periode: AKTIF", "#7C3AED", "#F5F3FF", "📅"),
    ]
    
    for i, (stitle, sval, ssub, c_accent, c_bg, icon) in enumerate(stats):
        cx1 = content_x + i * (card_w + 12)
        cx2 = cx1 + card_w
        draw_rounded_rect(draw, (S(cx1), S(158), S(cx2), S(248)), radius=S(8), fill="#FFFFFF", outline="#E2E8F0", width=S(1))
        # Top color accent bar
        draw_rounded_rect(draw, (S(cx1), S(158), S(cx2), S(162)), radius=S(2), fill=c_accent)
        
        # Icon box
        draw_rounded_rect(draw, (S(cx2 - 48), S(172), S(cx2 - 14), S(206)), radius=S(6), fill=c_bg)
        draw_centered_in_box(draw, (S(cx2 - 48), S(172), S(cx2 - 14), S(206)), icon, c_accent, get_font(12 * scale))
        
        draw.text((S(cx1 + 16), S(172)), stitle, fill="#64748B", font=get_font(9 * scale, bold=True))
        draw.text((S(cx1 + 16), S(190)), sval, fill="#0F172A", font=get_font(16 * scale, bold=True))
        draw.text((S(cx1 + 16), S(224)), ssub, fill="#059669" if i < 2 else "#64748B", font=get_font(9 * scale))
        
    # Status Banner SPK MOORA
    draw_rounded_rect(draw, (S(content_x), S(260), S(w - 20), S(375)), radius=S(8), fill="#FFFFFF", outline="#E2E8F0", width=S(1))
    draw.text((S(content_x + 20), S(275)), "⚡ Status Kesiapan Perhitungan SPK MOORA (Periode: Juni 2026)", fill="#0F172A", font=get_font(13 * scale, bold=True))
    draw.text((S(content_x + 20), S(298)), "Seluruh 18 guru aktif telah dinilai pada 4 kriteria (C1-Kehadiran, C2-Ketepatan Waktu, C3-Perangkat, C4-Administrasi). Sistem siap melakukan optimasi multiobjektif.", fill="#475569", font=get_font(10 * scale))
    
    # Progress Bar
    draw_rounded_rect(draw, (S(content_x + 20), S(326), S(content_x + 650), S(342)), radius=S(4), fill="#E2E8F0")
    draw_rounded_rect(draw, (S(content_x + 20), S(326), S(content_x + 650), S(342)), radius=S(4), fill="#059669")
    draw.text((S(content_x + 665), S(326)), "100% Siap Dihitung", fill="#059669", font=get_font(11 * scale, bold=True))
    
    # Action buttons
    draw_rounded_rect(draw, (S(w - 380), S(318), S(w - 210), S(354)), radius=S(6), fill="#059669")
    draw_centered_in_box(draw, (S(w - 380), S(318), S(w - 210), S(354)), "⚡ Hitung SPK MOORA", "#FFFFFF", get_font(10 * scale, bold=True))
    
    draw_rounded_rect(draw, (S(w - 195), S(318), S(w - 35), S(354)), radius=S(6), fill="#F8FAFC", outline="#CBD5E1", width=S(1))
    draw_centered_in_box(draw, (S(w - 195), S(318), S(w - 35), S(354)), "Lihat Ranking  →", "#0F172A", get_font(10 * scale, bold=True))
    
    # 2 Cards: Top 3 Guru & Log Aktivitas
    split_w = (content_w - 16) // 2
    # Left: Leaderboard Top 3
    draw_rounded_rect(draw, (S(content_x), S(390), S(content_x + split_w), S(690)), radius=S(8), fill="#FFFFFF", outline="#E2E8F0", width=S(1))
    draw.rectangle([(S(content_x), S(390)), (S(content_x + split_w), S(430))], fill="#F8FAFC")
    draw.line([(S(content_x), S(430)), (S(content_x + split_w), S(430))], fill="#E2E8F0", width=S(1))
    draw.text((S(content_x + 18), S(402)), "🏆 3 Besar Guru Terbaik (Metode MOORA)", fill="#0F172A", font=get_font(12 * scale, bold=True))
    
    top_3 = [
        ("1", "Ahmad Fauzi, S.Pd.", "Guru Matematika", "0.2754", "#FEF3C7", "#D97706", "🥇 Juara 1"),
        ("2", "Siti Nurhaliza, M.Pd.", "Guru Bahasa Indonesia", "0.2669", "#F1F5F9", "#475569", "🥈 Juara 2"),
        ("3", "Budi Santoso, S.Si.", "Guru Fisika", "0.2616", "#FFEDD5", "#C2410C", "🥉 Juara 3"),
    ]
    for idx, (rk, gname, gmapel, gyi, bg_c, txt_c, medal) in enumerate(top_3):
        gy = 445 + idx * 76
        draw_rounded_rect(draw, (S(content_x + 16), S(gy), S(content_x + split_w - 16), S(gy + 66)), radius=S(6), fill="#F8FAFC", outline="#E2E8F0", width=S(1))
        draw_rounded_rect(draw, (S(content_x + 26), S(gy + 14), S(content_x + 66), S(gy + 52)), radius=S(6), fill=bg_c)
        draw_centered_in_box(draw, (S(content_x + 26), S(gy + 14), S(content_x + 66), S(gy + 52)), f"#{rk}", txt_c, get_font(13 * scale, bold=True))
        
        draw.text((S(content_x + 78), S(gy + 12)), gname, fill="#0F172A", font=get_font(11 * scale, bold=True))
        draw.text((S(content_x + 78), S(gy + 30)), gmapel, fill="#64748B", font=get_font(9 * scale))
        draw.text((S(content_x + 78), S(gy + 46)), f"Nilai Yi: {gyi} • Predikat Sangat Baik", fill="#059669", font=get_font(9 * scale, bold=True))
        
        draw_rounded_rect(draw, (S(content_x + split_w - 105), S(gy + 20), S(content_x + split_w - 26), S(gy + 46)), radius=S(4), fill=bg_c)
        draw_centered_in_box(draw, (S(content_x + split_w - 105), S(gy + 20), S(content_x + split_w - 26), S(gy + 46)), medal, txt_c, get_font(9 * scale, bold=True))
        
    # Right: Log Aktivitas
    draw_rounded_rect(draw, (S(content_x + split_w + 16), S(390), S(w - 20), S(690)), radius=S(8), fill="#FFFFFF", outline="#E2E8F0", width=S(1))
    draw.rectangle([(S(content_x + split_w + 16), S(390)), (S(w - 20), S(430))], fill="#F8FAFC")
    draw.line([(S(content_x + split_w + 16), S(430)), (S(w - 20), S(430))], fill="#E2E8F0", width=S(1))
    draw.text((S(content_x + split_w + 34), S(402)), "📜 Riwayat Log Aktivitas Sistem Terbaru", fill="#0F172A", font=get_font(12 * scale, bold=True))
    
    logs = [
        ("AUTENTIKASI", "User admin (ADMIN) berhasil login ke sistem", "Baru saja", "#059669"),
        ("MOORA", "Kalkulasi MOORA periode Mei 2026 berhasil diproses", "10 mnt lalu", "#2563EB"),
        ("PENILAIAN", "Evaluator menyelesaikan input nilai 18 guru", "25 mnt lalu", "#D97706"),
        ("MASTER GURU", "Pembaruan beban jam tatap muka Ahmad Fauzi, S.Pd.", "1 jam lalu", "#7C3AED"),
    ]
    for idx, (lmod, lact, ltime, lcol) in enumerate(logs):
        ly = 445 + idx * 58
        draw.ellipse([(S(content_x + split_w + 36), S(ly + 6)), (S(content_x + split_w + 46), S(ly + 16))], fill=lcol)
        draw.text((S(content_x + split_w + 56), S(ly)), f"[{lmod}]", fill=lcol, font=get_font(9 * scale, bold=True))
        draw.text((S(content_x + split_w + 56), S(ly + 16)), lact, fill="#334155", font=get_font(9 * scale))
        draw.text((S(content_x + split_w + 56), S(ly + 32)), f"Waktu: {ltime}", fill="#94A3B8", font=get_font(8 * scale))
        if idx < 3:
            draw.line([(S(content_x + split_w + 56), S(ly + 48)), (S(w - 40), S(ly + 48))], fill="#F1F5F9", width=S(1))

    out_p = "system_screenshots/img_sys_02_dashboard_admin.png"
    img.save(out_p, quality=95)
    return out_p

# -------------------------------------------------------------
# 3. Kelola Data Guru
# -------------------------------------------------------------
def generate_sys_03_kelola_guru():
    scale = 2
    w, h = 1300, 720
    img = Image.new("RGB", (w * scale, h * scale), "#F8FAFC")
    draw = ImageDraw.Draw(img)
    def S(v): return int(v * scale)
    
    draw_browser_chrome(draw, w, scale, "http://localhost:3000/admin/guru")
    draw_app_header(draw, w, h, scale, "Kelola Master Data Guru", "Manajemen data profil tenaga pendidik & alternatif SPK MOORA", "Administrator", "Sugih Sugistiana (Admin)", "Juni 2026")
    draw_app_sidebar(draw, h, scale, active_menu="Guru")
    
    content_x = 260
    content_w = w - content_x - 20
    
    # Table Card Container
    draw_rounded_rect(draw, (S(content_x), S(158), S(w - 20), S(690)), radius=S(8), fill="#FFFFFF", outline="#E2E8F0", width=S(1))
    
    # Search & Action Bar
    draw_rounded_rect(draw, (S(content_x + 18), S(172), S(content_x + 350), S(206)), radius=S(6), fill="#F8FAFC", outline="#CBD5E1", width=S(1))
    draw.text((S(content_x + 32), S(181)), "🔍 Cari nama guru / NIP...", fill="#94A3B8", font=get_font(10 * scale))
    
    draw_rounded_rect(draw, (S(w - 180), S(172), S(w - 36), S(206)), radius=S(6), fill="#059669")
    draw_centered_in_box(draw, (S(w - 180), S(172), S(w - 36), S(206)), "+ Tambah Guru", "#FFFFFF", get_font(10 * scale, bold=True))
    
    # Table Header
    ty = 220
    draw.rectangle([(S(content_x), S(ty)), (S(w - 20), S(ty + 38))], fill="#F8FAFC")
    draw.line([(S(content_x), S(ty + 38)), (S(w - 20), S(ty + 38))], fill="#CBD5E1", width=S(1))
    
    cols = [
        ("NO", 45), ("NIP", 160), ("NAMA LENGKAP", 230), ("JK", 50),
        ("TUGAS MENGAJAR", 190), ("TUGAS TAMBAHAN", 200), ("JAM", 60), ("STATUS", 80)
    ]
    cur_x = content_x + 15
    for cname, cw in cols:
        draw.text((S(cur_x), S(ty + 11)), cname, fill="#475569", font=get_font(9 * scale, bold=True))
        cur_x += cw
        
    gurus = [
        ("1", "198501152010011001", "Ahmad Fauzi, S.Pd.", "L", "Guru Matematika", "Wakasek Kurikulum", "24 Jam", "AKTIF"),
        ("2", "198703222011012002", "Siti Nurhaliza, M.Pd.", "P", "Guru Bahasa Indonesia", "Kepala Perpustakaan", "26 Jam", "AKTIF"),
        ("3", "198904102014021003", "Budi Santoso, S.Si.", "L", "Guru Fisika", "Kepala Lab IPA", "24 Jam", "AKTIF"),
        ("4", "199005122015032004", "Ratna Dewi, S.Pd.", "P", "Guru Kimia", "Wali Kelas 11 MIPA 1", "24 Jam", "AKTIF"),
        ("5", "199108182016011005", "Hendra Gunawan, S.Kom.", "L", "Guru Informatika", "Kepala Lab Komputer", "24 Jam", "AKTIF"),
        ("6", "199211052017022006", "Dewi Lestari, M.Pd.", "P", "Guru Biologi", "Wali Kelas 10 MIPA 2", "22 Jam", "AKTIF"),
        ("7", "198806202012011007", "Rudi Hermawan, S.Pd.", "L", "Guru Bahasa Inggris", "Pembina English Club", "24 Jam", "AKTIF"),
        ("8", "199302142018032008", "Nurul Hidayah, S.Pd.I.", "P", "Guru PAI", "Koordinator Tahfidz", "26 Jam", "AKTIF"),
        ("9", "198609252011011009", "Agus Setiawan, S.Pd.", "L", "Guru Penjasorkes", "Pembina Olahraga", "24 Jam", "AKTIF"),
        ("10", "199407302019022010", "Rina Marlina, S.Pd.", "P", "Guru Sejarah", "Wali Kelas 12 IPS 1", "20 Jam", "AKTIF"),
    ]
    for idx, (no, nip, name, jk, mapel, tugas, jam, st) in enumerate(gurus):
        ry = ty + 38 + idx * 42
        if idx % 2 == 1:
            draw.rectangle([(S(content_x + 1), S(ry)), (S(w - 21), S(ry + 42))], fill="#F8FAFC")
        draw.line([(S(content_x), S(ry + 42)), (S(w - 20), S(ry + 42))], fill="#F1F5F9", width=S(1))
        
        cur_x = content_x + 15
        row_vals = [(no, 45), (nip, 160), (name, 230), (jk, 50), (mapel, 190), (tugas, 200), (jam, 60)]
        for val, cw in row_vals:
            draw.text((S(cur_x), S(ry + 12)), str(val), fill="#0F172A" if cw > 100 else "#64748B", font=get_font(10 * scale, bold=(cw == 230)))
            cur_x += cw
            
        # Status pill
        draw_rounded_rect(draw, (S(cur_x), S(ry + 10), S(cur_x + 60), S(ry + 32)), radius=S(4), fill="#ECFDF5", outline="#A7F3D0", width=S(1))
        draw_centered_in_box(draw, (S(cur_x), S(ry + 10), S(cur_x + 60), S(ry + 32)), "AKTIF", "#065F46", get_font(8 * scale, bold=True))

    out_p = "system_screenshots/img_sys_03_kelola_guru.png"
    img.save(out_p, quality=95)
    return out_p

# -------------------------------------------------------------
# 4. Kelola Kriteria & Bobot
# -------------------------------------------------------------
def generate_sys_04_kelola_kriteria():
    scale = 2
    w, h = 1300, 720
    img = Image.new("RGB", (w * scale, h * scale), "#F8FAFC")
    draw = ImageDraw.Draw(img)
    def S(v): return int(v * scale)
    
    draw_browser_chrome(draw, w, scale, "http://localhost:3000/admin/kriteria")
    draw_app_header(draw, w, h, scale, "Kelola Kriteria & Bobot", "Konfigurasi kriteria evaluasi kinerja guru dan parameter MOORA", "Administrator", "Sugih Sugistiana (Admin)", "Juni 2026")
    draw_app_sidebar(draw, h, scale, active_menu="Kriteria")
    
    content_x = 260
    
    # Banner Total Bobot Valid
    draw_rounded_rect(draw, (S(content_x), S(158), S(w - 20), S(215)), radius=S(8), fill="#ECFDF5", outline="#A7F3D0", width=S(1))
    draw.text((S(content_x + 20), S(172)), "✅ Total Bobot Kriteria Valid: 1.00 (100%)", fill="#065F46", font=get_font(12 * scale, bold=True))
    draw.text((S(content_x + 20), S(192)), "Akumulasi bobot kriteria telah memenuhi syarat normalisasi MOORA (∑Wj = 1.00). Seluruh kriteria bernilai BENEFIT.", fill="#047857", font=get_font(10 * scale))
    
    # Table Card
    draw_rounded_rect(draw, (S(content_x), S(230), S(w - 20), S(690)), radius=S(8), fill="#FFFFFF", outline="#E2E8F0", width=S(1))
    draw.text((S(content_x + 20), S(248)), "Daftar Kriteria Penilaian Kinerja Guru (Metode MOORA)", fill="#0F172A", font=get_font(13 * scale, bold=True))
    
    ty = 280
    draw.rectangle([(S(content_x), S(ty)), (S(w - 20), S(ty + 40))], fill="#F8FAFC")
    draw.line([(S(content_x), S(ty + 40)), (S(w - 20), S(ty + 40))], fill="#CBD5E1", width=S(1))
    
    cols = [("KODE", 80), ("NAMA KRITERIA", 300), ("BOBOT PREFERENSI", 180), ("PERSENTASE", 130), ("SIFAT KRITERIA", 140), ("STATUS", 100)]
    cur_x = content_x + 20
    for cname, cw in cols:
        draw.text((S(cur_x), S(ty + 12)), cname, fill="#475569", font=get_font(9 * scale, bold=True))
        cur_x += cw
        
    crit_data = [
        ("C1", "Kehadiran", "0.35", "35 %", "BENEFIT", "AKTIF", "#059669"),
        ("C2", "Ketepatan Waktu", "0.25", "25 %", "BENEFIT", "AKTIF", "#2563EB"),
        ("C3", "Kelengkapan Perangkat Pembelajaran", "0.25", "25 %", "BENEFIT", "AKTIF", "#D97706"),
        ("C4", "Kelengkapan Administrasi Penilaian", "0.15", "15 %", "BENEFIT", "AKTIF", "#7C3AED"),
    ]
    for idx, (kd, nm, wgt, pct, sft, st, col) in enumerate(crit_data):
        ry = ty + 40 + idx * 75
        draw.line([(S(content_x), S(ry + 75)), (S(w - 20), S(ry + 75))], fill="#F1F5F9", width=S(1))
        
        # Code badge
        draw_rounded_rect(draw, (S(content_x + 20), S(ry + 18), S(content_x + 70), S(ry + 56)), radius=S(6), fill="#EFF6FF", outline="#BFDBFE", width=S(1))
        draw_centered_in_box(draw, (S(content_x + 20), S(ry + 18), S(content_x + 70), S(ry + 56)), kd, "#2563EB", get_font(13 * scale, bold=True))
        
        draw.text((S(content_x + 100), S(ry + 18)), nm, fill="#0F172A", font=get_font(12 * scale, bold=True))
        draw.text((S(content_x + 100), S(ry + 40)), f"Parameter evaluasi kinerja guru aspek {nm.lower()}", fill="#64748B", font=get_font(9 * scale))
        
        draw.text((S(content_x + 400), S(ry + 26)), wgt, fill="#0F172A", font=get_font(13 * scale, bold=True))
        draw.text((S(content_x + 580), S(ry + 26)), pct, fill="#059669", font=get_font(12 * scale, bold=True))
        
        # Sifat Benefit Pill
        draw_rounded_rect(draw, (S(content_x + 710), S(ry + 22), S(content_x + 810), S(ry + 52)), radius=S(4), fill="#ECFDF5", outline="#A7F3D0", width=S(1))
        draw_centered_in_box(draw, (S(content_x + 710), S(ry + 22), S(content_x + 810), S(ry + 52)), "BENEFIT", "#065F46", get_font(10 * scale, bold=True))
        
        # Status Pill
        draw_rounded_rect(draw, (S(content_x + 850), S(ry + 22), S(content_x + 930), S(ry + 52)), radius=S(4), fill="#F8FAFC", outline="#CBD5E1", width=S(1))
        draw_centered_in_box(draw, (S(content_x + 850), S(ry + 22), S(content_x + 930), S(ry + 52)), "AKTIF", "#334155", get_font(10 * scale, bold=True))

    out_p = "system_screenshots/img_sys_04_kelola_kriteria.png"
    img.save(out_p, quality=95)
    return out_p

# -------------------------------------------------------------
# 5. Kelola Skala Penilaian / Rubrik
# -------------------------------------------------------------
def generate_sys_05_skala_penilaian():
    scale = 2
    w, h = 1300, 720
    img = Image.new("RGB", (w * scale, h * scale), "#F8FAFC")
    draw = ImageDraw.Draw(img)
    def S(v): return int(v * scale)
    
    draw_browser_chrome(draw, w, scale, "http://localhost:3000/admin/skala-penilaian")
    draw_app_header(draw, w, h, scale, "Kelola Skala Penilaian / Rubrik", "Rubrik indikator capaian kompetensi kuantitatif skala 1 - 5", "Administrator", "Sugih Sugistiana (Admin)", "Juni 2026")
    draw_app_sidebar(draw, h, scale, active_menu="Skala")
    
    content_x = 260
    
    # Filter Tabs for Kriteria C1 - C4
    draw.text((S(content_x), S(160)), "Pilih Kriteria Penilaian:", fill="#0F172A", font=get_font(11 * scale, bold=True))
    tab_list = [
        ("C1 - Kehadiran (35%)", True),
        ("C2 - Ketepatan Waktu (25%)", False),
        ("C3 - Perangkat Pembelajaran (25%)", False),
        ("C4 - Administrasi Penilaian (15%)", False),
    ]
    cur_tx = content_x
    for t_label, is_act in tab_list:
        tw = len(t_label) * 8 + 30
        if is_act:
            draw_rounded_rect(draw, (S(cur_tx), S(184), S(cur_tx + tw), S(220)), radius=S(6), fill="#059669")
            draw_centered_in_box(draw, (S(cur_tx), S(184), S(cur_tx + tw), S(220)), t_label, "#FFFFFF", get_font(10 * scale, bold=True))
        else:
            draw_rounded_rect(draw, (S(cur_tx), S(184), S(cur_tx + tw), S(220)), radius=S(6), fill="#FFFFFF", outline="#CBD5E1", width=S(1))
            draw_centered_in_box(draw, (S(cur_tx), S(184), S(cur_tx + tw), S(220)), t_label, "#475569", get_font(10 * scale))
        cur_tx += tw + 12
        
    # Table Rubrik
    draw_rounded_rect(draw, (S(content_x), S(235), S(w - 20), S(690)), radius=S(8), fill="#FFFFFF", outline="#E2E8F0", width=S(1))
    
    ty = 250
    draw.rectangle([(S(content_x), S(ty)), (S(w - 20), S(ty + 40))], fill="#F8FAFC")
    draw.line([(S(content_x), S(ty + 40)), (S(w - 20), S(ty + 40))], fill="#CBD5E1", width=S(1))
    
    draw.text((S(content_x + 20), S(ty + 12)), "SKOR", fill="#475569", font=get_font(9 * scale, bold=True))
    draw.text((S(content_x + 120), S(ty + 12)), "PREDIKAT", fill="#475569", font=get_font(9 * scale, bold=True))
    draw.text((S(content_x + 280), S(ty + 12)), "DESKRIPSI INDIKATOR KETERCAPAIAN KOMPETENSI GURU", fill="#475569", font=get_font(9 * scale, bold=True))
    
    rubriks = [
        ("5", "Sangat Baik", "Tingkat kehadiran guru ≥ 95% dari total hari efektif dinas, tanpa ketidakhadiran tanpa keterangan.", "#ECFDF5", "#065F46"),
        ("4", "Baik", "Tingkat kehadiran guru 85% – 94% dengan bukti surat keterangan izin/sakit yang sah.", "#EFF6FF", "#1E40AF"),
        ("3", "Cukup", "Tingkat kehadiran guru 75% – 84% dengan frekuensi izin dinas wajar.", "#FFFBEB", "#92400E"),
        ("2", "Kurang", "Tingkat kehadiran guru 60% – 74%, terdapat catatan terlambat atau tidak hadir tanpa izin resmi.", "#FEF2F2", "#991B1B"),
        ("1", "Sangat Kurang", "Tingkat kehadiran guru < 60%, memerlukan pembinaan khusus dari Kepala Sekolah.", "#FDF2F8", "#831843"),
    ]
    for idx, (skor, pred, desc, bg_p, txt_p) in enumerate(rubriks):
        ry = ty + 40 + idx * 76
        draw.line([(S(content_x), S(ry + 76)), (S(w - 20), S(ry + 76))], fill="#F1F5F9", width=S(1))
        
        # Skor Badge
        draw_rounded_rect(draw, (S(content_x + 20), S(ry + 16), S(content_x + 65), S(ry + 60)), radius=S(6), fill="#F8FAFC", outline="#CBD5E1", width=S(1))
        draw_centered_in_box(draw, (S(content_x + 20), S(ry + 16), S(content_x + 65), S(ry + 60)), skor, "#0F172A", get_font(16 * scale, bold=True))
        
        # Predikat Badge
        draw_rounded_rect(draw, (S(content_x + 110), S(ry + 22), S(content_x + 240), S(ry + 54)), radius=S(4), fill=bg_p, outline="#CBD5E1", width=S(1))
        draw_centered_in_box(draw, (S(content_x + 110), S(ry + 22), S(content_x + 240), S(ry + 54)), pred, txt_p, get_font(10 * scale, bold=True))
        
        # Deskripsi Indikator
        draw.text((S(content_x + 280), S(ry + 26)), desc, fill="#334155", font=get_font(10 * scale))

    out_p = "system_screenshots/img_sys_05_skala_penilaian.png"
    img.save(out_p, quality=95)
    return out_p

# -------------------------------------------------------------
# 6. Kelola Periode Penilaian
# -------------------------------------------------------------
def generate_sys_06_periode_penilaian():
    scale = 2
    w, h = 1300, 720
    img = Image.new("RGB", (w * scale, h * scale), "#F8FAFC")
    draw = ImageDraw.Draw(img)
    def S(v): return int(v * scale)
    
    draw_browser_chrome(draw, w, scale, "http://localhost:3000/admin/periode")
    draw_app_header(draw, w, h, scale, "Kelola Periode Penilaian", "Manajemen agenda siklus evaluasi berkala kinerja guru", "Administrator", "Sugih Sugistiana (Admin)", "Juni 2026")
    draw_app_sidebar(draw, h, scale, active_menu="Periode")
    
    content_x = 260
    
    # Table Card
    draw_rounded_rect(draw, (S(content_x), S(158), S(w - 20), S(690)), radius=S(8), fill="#FFFFFF", outline="#E2E8F0", width=S(1))
    
    # Top Action Bar
    draw.text((S(content_x + 20), S(176)), "Daftar Gelombang Evaluasi & Periode Penilaian Kinerja", fill="#0F172A", font=get_font(13 * scale, bold=True))
    draw_rounded_rect(draw, (S(w - 200), S(170), S(w - 36), S(206)), radius=S(6), fill="#059669")
    draw_centered_in_box(draw, (S(w - 200), S(170), S(w - 36), S(206)), "+ Buat Periode Baru", "#FFFFFF", get_font(10 * scale, bold=True))
    
    ty = 220
    draw.rectangle([(S(content_x), S(ty)), (S(w - 20), S(ty + 40))], fill="#F8FAFC")
    draw.line([(S(content_x), S(ty + 40)), (S(w - 20), S(ty + 40))], fill="#CBD5E1", width=S(1))
    
    cols = [("NAMA PERIODE", 200), ("BULAN", 130), ("TAHUN", 100), ("STATUS PERIODE", 150), ("PROGRES PENILAIAN", 260), ("AKSI", 120)]
    cur_x = content_x + 20
    for cname, cw in cols:
        draw.text((S(cur_x), S(ty + 12)), cname, fill="#475569", font=get_font(9 * scale, bold=True))
        cur_x += cw
        
    periodes = [
        ("Juni 2026", "Juni", "2026", "AKTIF", "18 dari 18 Guru (100% Selesai)", "#ECFDF5", "#065F46", True),
        ("Mei 2026", "Mei", "2026", "SELESAI", "18 dari 18 Guru (100% Selesai)", "#F1F5F9", "#475569", False),
    ]
    for idx, (pname, bln, thn, st, prg, bg_p, txt_p, is_active) in enumerate(periodes):
        ry = ty + 40 + idx * 85
        draw.line([(S(content_x), S(ry + 85)), (S(w - 20), S(ry + 85))], fill="#F1F5F9", width=S(1))
        
        draw.text((S(content_x + 20), S(ry + 24)), pname, fill="#0F172A", font=get_font(13 * scale, bold=True))
        draw.text((S(content_x + 220), S(ry + 26)), bln, fill="#334155", font=get_font(11 * scale))
        draw.text((S(content_x + 350), S(ry + 26)), thn, fill="#334155", font=get_font(11 * scale))
        
        # Status Badge
        draw_rounded_rect(draw, (S(content_x + 450), S(ry + 20), S(content_x + 550), S(ry + 54)), radius=S(4), fill=bg_p, outline="#A7F3D0" if is_active else "#CBD5E1", width=S(1))
        draw_centered_in_box(draw, (S(content_x + 450), S(ry + 20), S(content_x + 550), S(ry + 54)), f"● {st}", txt_p, get_font(10 * scale, bold=True))
        
        # Progress Bar
        draw.text((S(content_x + 600), S(ry + 14)), prg, fill="#059669", font=get_font(9 * scale, bold=True))
        draw_rounded_rect(draw, (S(content_x + 600), S(ry + 34), S(content_x + 830), S(ry + 46)), radius=S(4), fill="#E2E8F0")
        draw_rounded_rect(draw, (S(content_x + 600), S(ry + 34), S(content_x + 830), S(ry + 46)), radius=S(4), fill="#059669")
        
        # Action button
        draw_rounded_rect(draw, (S(content_x + 860), S(ry + 20), S(content_x + 960), S(ry + 54)), radius=S(4), fill="#F8FAFC", outline="#CBD5E1", width=S(1))
        draw_centered_in_box(draw, (S(content_x + 860), S(ry + 20), S(content_x + 960), S(ry + 54)), "Kelola Data", "#334155", get_font(9 * scale, bold=True))

    out_p = "system_screenshots/img_sys_06_periode_penilaian.png"
    img.save(out_p, quality=95)
    return out_p

# -------------------------------------------------------------
# 7. Form Transaksi Penilaian Kinerja Guru
# -------------------------------------------------------------
def generate_sys_07_form_penilaian():
    scale = 2
    w, h = 1300, 720
    img = Image.new("RGB", (w * scale, h * scale), "#F8FAFC")
    draw = ImageDraw.Draw(img)
    def S(v): return int(v * scale)
    
    draw_browser_chrome(draw, w, scale, "http://localhost:3000/kepala-sekolah/penilaian")
    draw_app_header(draw, w, h, scale, "Form Evaluasi Penilaian Kinerja Guru", "Instrumen penginputan skor kriteria & umpan balik kualitatif", "Kepala Sekolah", "Dr. H. Mulyadi, M.Pd.", "Juni 2026")
    draw_app_sidebar(draw, h, scale, active_menu="Penilaian")
    
    content_x = 260
    
    # Guru Info Header Box
    draw_rounded_rect(draw, (S(content_x), S(158), S(w - 20), S(245)), radius=S(8), fill="#FFFFFF", outline="#E2E8F0", width=S(1))
    draw_rounded_rect(draw, (S(content_x + 18), S(172), S(content_x + 75), S(228)), radius=S(8), fill="#ECFDF5", outline="#A7F3D0", width=S(1))
    draw_centered_in_box(draw, (S(content_x + 18), S(172), S(content_x + 75), S(228)), "AF", "#065F46", get_font(16 * scale, bold=True))
    
    draw.text((S(content_x + 90), S(172)), "Ahmad Fauzi, S.Pd. (NIP: 198501152010011001)", fill="#0F172A", font=get_font(13 * scale, bold=True))
    draw.text((S(content_x + 90), S(194)), "Penugasan: Guru Matematika • Beban Ajar: 24 Jam/Minggu • Tugas Tambahan: Wakasek Kurikulum", fill="#475569", font=get_font(10 * scale))
    draw.text((S(content_x + 90), S(214)), "Evaluator: Dr. H. Mulyadi, M.Pd. (Kepala Sekolah) • Status Penilaian: SELESAI", fill="#059669", font=get_font(9 * scale, bold=True))
    
    # 4 Kriteria Radio Cards
    crits = [
        ("C1. Kehadiran (Bobot: 35%)", "Tingkat kehadiran guru ≥ 95% dari total hari dinas", 5),
        ("C2. Ketepatan Waktu (Bobot: 25%)", "Selalu hadir tepat waktu saat jam pelajaran", 5),
        ("C3. Kelengkapan Perangkat Pembelajaran (Bobot: 25%)", "Modul ajar dan RPP lengkap terverifikasi", 5),
        ("C4. Kelengkapan Administrasi Penilaian (Bobot: 15%)", "Rekap nilai dan rubrik evaluasi siswa rapi", 4),
    ]
    for idx, (ctitle, cdesc, val) in enumerate(crits):
        cy = 260 + idx * 74
        draw_rounded_rect(draw, (S(content_x), S(cy), S(w - 20), S(cy + 64)), radius=S(6), fill="#FFFFFF", outline="#E2E8F0", width=S(1))
        draw.text((S(content_x + 18), S(cy + 12)), ctitle, fill="#0F172A", font=get_font(11 * scale, bold=True))
        draw.text((S(content_x + 18), S(cy + 34)), cdesc, fill="#64748B", font=get_font(9 * scale))
        
        # 5 Radio Buttons for scale 1..5
        for s in range(1, 6):
            rx = w - 380 + (s - 1) * 65
            is_sel = (s == val)
            draw_rounded_rect(draw, (S(rx), S(cy + 14), S(rx + 52), S(cy + 48)), radius=S(4), fill="#059669" if is_sel else "#F8FAFC", outline="#059669" if is_sel else "#CBD5E1", width=S(1))
            draw_centered_in_box(draw, (S(rx), S(cy + 14), S(rx + 52), S(cy + 48)), f"Skor {s}", "#FFFFFF" if is_sel else "#475569", get_font(9 * scale, bold=is_sel))

    # Notes & Save Button
    draw_rounded_rect(draw, (S(content_x), S(570), S(w - 20), S(690)), radius=S(8), fill="#FFFFFF", outline="#E2E8F0", width=S(1))
    draw.text((S(content_x + 18), S(582)), "Catatan Pembinaan & Evaluasi Kepala Sekolah:", fill="#0F172A", font=get_font(10 * scale, bold=True))
    draw_rounded_rect(draw, (S(content_x + 18), S(604), S(w - 240), S(675)), radius=S(4), fill="#F8FAFC", outline="#CBD5E1", width=S(1))
    draw.text((S(content_x + 28), S(616)), "Kinerja Ahmad Fauzi, S.Pd. sangat konsisten dan berdedikasi tinggi baik dalam proses belajar mengajar maupun koordinasi kurikulum sekolah.", fill="#334155", font=get_font(10 * scale))
    
    draw_rounded_rect(draw, (S(w - 210), S(610), S(w - 36), S(660)), radius=S(6), fill="#059669")
    draw_centered_in_box(draw, (S(w - 210), S(610), S(w - 36), S(660)), "💾 Simpan Nilai Selesai", "#FFFFFF", get_font(10 * scale, bold=True))

    out_p = "system_screenshots/img_sys_07_form_penilaian.png"
    img.save(out_p, quality=95)
    return out_p

# -------------------------------------------------------------
# 8. Proses Perhitungan SPK MOORA
# -------------------------------------------------------------
def generate_sys_08_proses_moora():
    scale = 2
    w, h = 1300, 720
    img = Image.new("RGB", (w * scale, h * scale), "#F8FAFC")
    draw = ImageDraw.Draw(img)
    def S(v): return int(v * scale)
    
    draw_browser_chrome(draw, w, scale, "http://localhost:3000/admin/moora")
    draw_app_header(draw, w, h, scale, "Proses Perhitungan Metode MOORA", "Transparansi tahapan kalkulasi multiobjektif matriks X, X*, W, dan Nilai Yi", "Administrator", "Sugih Sugistiana (Admin)", "Juni 2026")
    draw_app_sidebar(draw, h, scale, active_menu="MOORA")
    
    content_x = 260
    
    # 4 Steps Navigation Tabs
    tabs = [
        ("1. Matriks Keputusan (X)", False),
        ("2. Normalisasi Matriks (X*)", False),
        ("3. Matriks Terbobot (W·X*)", True),
        ("4. Nilai Preferensi (Yi)", False),
    ]
    cur_tx = content_x
    for t_label, is_act in tabs:
        tw = len(t_label) * 8 + 25
        if is_act:
            draw_rounded_rect(draw, (S(cur_tx), S(158), S(cur_tx + tw), S(194)), radius=S(6), fill="#059669")
            draw_centered_in_box(draw, (S(cur_tx), S(158), S(cur_tx + tw), S(194)), t_label, "#FFFFFF", get_font(10 * scale, bold=True))
        else:
            draw_rounded_rect(draw, (S(cur_tx), S(158), S(cur_tx + tw), S(194)), radius=S(6), fill="#FFFFFF", outline="#CBD5E1", width=S(1))
            draw_centered_in_box(draw, (S(cur_tx), S(158), S(cur_tx + tw), S(194)), t_label, "#475569", get_font(10 * scale))
        cur_tx += tw + 10
        
    # Table Card Container
    draw_rounded_rect(draw, (S(content_x), S(208), S(w - 20), S(690)), radius=S(8), fill="#FFFFFF", outline="#E2E8F0", width=S(1))
    
    ty = 220
    draw.rectangle([(S(content_x), S(ty)), (S(w - 20), S(ty + 40))], fill="#F8FAFC")
    draw.line([(S(content_x), S(ty + 40)), (S(w - 20), S(ty + 40))], fill="#CBD5E1", width=S(1))
    
    cols = [
        ("NO", 45), ("NAMA GURU (ALTERNATIF)", 250),
        ("C1 (W=0.35)", 140), ("C2 (W=0.25)", 140), ("C3 (W=0.25)", 140), ("C4 (W=0.15)", 140), ("NILAI Yi", 120)
    ]
    cur_x = content_x + 15
    for cname, cw in cols:
        draw.text((S(cur_x), S(ty + 12)), cname, fill="#475569", font=get_font(9 * scale, bold=True))
        cur_x += cw
        
    moora_rows = [
        ("1", "Ahmad Fauzi, S.Pd.", "0.0944", "0.0692", "0.0692", "0.0426", "0.2754"),
        ("2", "Siti Nurhaliza, M.Pd.", "0.0944", "0.0692", "0.0554", "0.0426", "0.2616"),
        ("3", "Budi Santoso, S.Si.", "0.0944", "0.0554", "0.0692", "0.0426", "0.2616"),
        ("4", "Ratna Dewi, S.Pd.", "0.0755", "0.0692", "0.0692", "0.0341", "0.2480"),
        ("5", "Hendra Gunawan, S.Kom.", "0.0944", "0.0692", "0.0554", "0.0426", "0.2616"),
        ("6", "Dewi Lestari, M.Pd.", "0.0755", "0.0554", "0.0692", "0.0426", "0.2427"),
        ("7", "Rudi Hermawan, S.Pd.", "0.0944", "0.0554", "0.0554", "0.0341", "0.2393"),
        ("8", "Nurul Hidayah, S.Pd.I.", "0.0944", "0.0692", "0.0692", "0.0426", "0.2754"),
    ]
    for idx, (no, name, c1, c2, c3, c4, yi) in enumerate(moora_rows):
        ry = ty + 40 + idx * 52
        if idx % 2 == 1:
            draw.rectangle([(S(content_x + 1), S(ry)), (S(w - 21), S(ry + 52))], fill="#F8FAFC")
        draw.line([(S(content_x), S(ry + 52)), (S(w - 20), S(ry + 52))], fill="#F1F5F9", width=S(1))
        
        cur_x = content_x + 15
        row_vals = [(no, 45), (name, 250), (c1, 140), (c2, 140), (c3, 140), (c4, 140)]
        for val, cw in row_vals:
            draw.text((S(cur_x), S(ry + 16)), str(val), fill="#0F172A", font=get_font(10 * scale, bold=(cw == 250)))
            cur_x += cw
            
        # Nilai Yi Badge
        draw_rounded_rect(draw, (S(cur_x), S(ry + 10), S(cur_x + 95), S(ry + 42)), radius=S(4), fill="#ECFDF5", outline="#A7F3D0", width=S(1))
        draw_centered_in_box(draw, (S(cur_x), S(ry + 10), S(cur_x + 95), S(ry + 42)), yi, "#065F46", get_font(10 * scale, bold=True))

    out_p = "system_screenshots/img_sys_08_proses_moora.png"
    img.save(out_p, quality=95)
    return out_p

# -------------------------------------------------------------
# 9. Peringkat & Hasil Ranking Guru
# -------------------------------------------------------------
def generate_sys_09_ranking_guru():
    scale = 2
    w, h = 1300, 720
    img = Image.new("RGB", (w * scale, h * scale), "#F8FAFC")
    draw = ImageDraw.Draw(img)
    def S(v): return int(v * scale)
    
    draw_browser_chrome(draw, w, scale, "http://localhost:3000/admin/ranking")
    draw_app_header(draw, w, h, scale, "Peringkat & Hasil Ranking Guru", "Hasil akhir evaluasi kinerja guru berdasarkan nilai preferensi MOORA", "Administrator", "Sugih Sugistiana (Admin)", "Juni 2026")
    draw_app_sidebar(draw, h, scale, active_menu="Ranking")
    
    content_x = 260
    content_w = w - content_x - 20
    
    # 3 Podium Cards
    pod_w = (content_w - 24) // 3
    podiums = [
        ("JUARA 2 (RUNNER UP)", "Siti Nurhaliza, M.Pd.", "Guru Bahasa Indonesia", "Yi: 0.2669", "#F1F5F9", "#475569", "🥈 Rank #2"),
        ("JUARA 1 (TERBAIK)", "Ahmad Fauzi, S.Pd.", "Guru Matematika", "Yi: 0.2754", "#FEF3C7", "#D97706", "🥇 Rank #1"),
        ("JUARA 3", "Budi Santoso, S.Si.", "Guru Fisika", "Yi: 0.2616", "#FFEDD5", "#C2410C", "🥉 Rank #3"),
    ]
    for idx, (title, name, mapel, score, bg_c, txt_c, medal) in enumerate(podiums):
        px1 = content_x + idx * (pod_w + 12)
        px2 = px1 + pod_w
        draw_rounded_rect(draw, (S(px1), S(158), S(px2), S(280)), radius=S(8), fill="#FFFFFF", outline="#E2E8F0", width=S(1))
        # Top badge
        draw_rounded_rect(draw, (S(px1), S(158), S(px2), S(190)), radius=S(6), fill=bg_c)
        draw_centered_in_box(draw, (S(px1), S(158), S(px2), S(190)), medal, txt_c, get_font(11 * scale, bold=True))
        
        draw_centered_in_box(draw, (S(px1), S(198), S(px2), S(224)), name, "#0F172A", get_font(12 * scale, bold=True))
        draw_centered_in_box(draw, (S(px1), S(226), S(px2), S(246)), mapel, "#64748B", get_font(9 * scale))
        draw_centered_in_box(draw, (S(px1), S(248), S(px2), S(272)), score, "#059669", get_font(11 * scale, bold=True))

    # Ranking Table
    draw_rounded_rect(draw, (S(content_x), S(295), S(w - 20), S(690)), radius=S(8), fill="#FFFFFF", outline="#E2E8F0", width=S(1))
    
    ty = 305
    draw.rectangle([(S(content_x), S(ty)), (S(w - 20), S(ty + 38))], fill="#F8FAFC")
    draw.line([(S(content_x), S(ty + 38)), (S(w - 20), S(ty + 38))], fill="#CBD5E1", width=S(1))
    
    cols = [("RANK", 70), ("NIP", 160), ("NAMA GURU", 260), ("TUGAS MENGAJAR", 200), ("NILAI PREFERENSI (Yi)", 180), ("PREDIKAT", 120)]
    cur_x = content_x + 15
    for cname, cw in cols:
        draw.text((S(cur_x), S(ty + 11)), cname, fill="#475569", font=get_font(9 * scale, bold=True))
        cur_x += cw
        
    ranks = [
        ("1", "198501152010011001", "Ahmad Fauzi, S.Pd.", "Guru Matematika", "0.2754", "Sangat Baik", "#ECFDF5", "#065F46"),
        ("2", "198703222011012002", "Siti Nurhaliza, M.Pd.", "Guru Bahasa Indonesia", "0.2669", "Sangat Baik", "#ECFDF5", "#065F46"),
        ("3", "198904102014021003", "Budi Santoso, S.Si.", "Guru Fisika", "0.2616", "Sangat Baik", "#ECFDF5", "#065F46"),
        ("4", "199108182016011005", "Hendra Gunawan, S.Kom.", "Guru Informatika", "0.2616", "Sangat Baik", "#ECFDF5", "#065F46"),
        ("5", "199005122015032004", "Ratna Dewi, S.Pd.", "Guru Kimia", "0.2480", "Baik", "#EFF6FF", "#1E40AF"),
        ("6", "199211052017022006", "Dewi Lestari, M.Pd.", "Guru Biologi", "0.2427", "Baik", "#EFF6FF", "#1E40AF"),
        ("7", "198806202012011007", "Rudi Hermawan, S.Pd.", "Guru Bahasa Inggris", "0.2393", "Baik", "#EFF6FF", "#1E40AF"),
    ]
    for idx, (rk, nip, name, mapel, yi, pred, bg_p, txt_p) in enumerate(ranks):
        ry = ty + 38 + idx * 46
        if idx % 2 == 1:
            draw.rectangle([(S(content_x + 1), S(ry)), (S(w - 21), S(ry + 46))], fill="#F8FAFC")
        draw.line([(S(content_x), S(ry + 46)), (S(w - 20), S(ry + 46))], fill="#F1F5F9", width=S(1))
        
        cur_x = content_x + 15
        row_vals = [(f"#{rk}", 70), (nip, 160), (name, 260), (mapel, 200), (yi, 180)]
        for val, cw in row_vals:
            draw.text((S(cur_x), S(ry + 14)), str(val), fill="#0F172A", font=get_font(10 * scale, bold=(cw in (70, 260, 180))))
            cur_x += cw
            
        draw_rounded_rect(draw, (S(cur_x), S(ry + 10), S(cur_x + 105), S(ry + 36)), radius=S(4), fill=bg_p, outline="#CBD5E1", width=S(1))
        draw_centered_in_box(draw, (S(cur_x), S(ry + 10), S(cur_x + 105), S(ry + 36)), pred, txt_p, get_font(9 * scale, bold=True))

    out_p = "system_screenshots/img_sys_09_ranking_guru.png"
    img.save(out_p, quality=95)
    return out_p

# -------------------------------------------------------------
# 10. Laporan & Cetak Rekapitulasi
# -------------------------------------------------------------
def generate_sys_10_laporan_cetak():
    scale = 2
    w, h = 1300, 720
    img = Image.new("RGB", (w * scale, h * scale), "#F8FAFC")
    draw = ImageDraw.Draw(img)
    def S(v): return int(v * scale)
    
    draw_browser_chrome(draw, w, scale, "http://localhost:3000/admin/laporan")
    draw_app_header(draw, w, h, scale, "Laporan & Cetak Rekapitulasi", "Ekspor rekapitulasi penilaian kinerja dan peringkat guru ke format PDF/Excel", "Administrator", "Sugih Sugistiana (Admin)", "Juni 2026")
    draw_app_sidebar(draw, h, scale, active_menu="Laporan")
    
    content_x = 260
    
    # Filter & Export Bar
    draw_rounded_rect(draw, (S(content_x), S(158), S(w - 20), S(225)), radius=S(8), fill="#FFFFFF", outline="#E2E8F0", width=S(1))
    draw.text((S(content_x + 20), S(174)), "Filter Periode: Periode Aktif (Juni 2026)", fill="#0F172A", font=get_font(11 * scale, bold=True))
    draw.text((S(content_x + 20), S(196)), "Cetak dokumen resmi rekapitulasi nilai C1-C4 dan perangkingan MOORA lengkap dengan lembar pengesahan.", fill="#64748B", font=get_font(9 * scale))
    
    # Export Buttons
    draw_rounded_rect(draw, (S(w - 380), S(172), S(w - 210), S(210)), radius=S(6), fill="#DC2626")
    draw_centered_in_box(draw, (S(w - 380), S(172), S(w - 210), S(210)), "📄 Cetak Laporan PDF", "#FFFFFF", get_font(10 * scale, bold=True))
    
    draw_rounded_rect(draw, (S(w - 195), S(172), S(w - 36), S(210)), radius=S(6), fill="#059669")
    draw_centered_in_box(draw, (S(w - 195), S(172), S(w - 36), S(210)), "📊 Export Excel (.xlsx)", "#FFFFFF", get_font(10 * scale, bold=True))
    
    # Report Paper Preview Card
    draw_rounded_rect(draw, (S(content_x + 40), S(245), S(w - 60), S(690)), radius=S(4), fill="#FFFFFF", outline="#CBD5E1", width=S(1))
    
    # Paper Header
    draw_centered_in_box(draw, (S(content_x + 40), S(260), S(w - 60), S(280)), "REKAPITULASI PENILAIAN KINERJA GURU (METODE MOORA)", "#0F172A", get_font(12 * scale, bold=True))
    draw_centered_in_box(draw, (S(content_x + 40), S(282), S(w - 60), S(298)), "SMA AL-IHSAN BOARDING SCHOOL - PERIODE JUNI 2026", "#475569", get_font(10 * scale, bold=True))
    draw.line([(S(content_x + 60), S(305)), (S(w - 80), S(305))], fill="#0F172A", width=S(2))
    
    # Mini Table in Report Preview
    ty = 315
    draw.rectangle([(S(content_x + 60), S(ty)), (S(w - 80), S(ty + 30))], fill="#F1F5F9")
    draw.line([(S(content_x + 60), S(ty + 30)), (S(w - 80), S(ty + 30))], fill="#CBD5E1", width=S(1))
    
    cols = [("RANK", 60), ("NIP", 140), ("NAMA LENGKAP", 220), ("C1 (35%)", 80), ("C2 (25%)", 80), ("C3 (25%)", 80), ("C4 (15%)", 80), ("NILAI Yi", 90), ("PREDIKAT", 100)]
    cur_x = content_x + 70
    for cname, cw in cols:
        draw.text((S(cur_x), S(ty + 8)), cname, fill="#0F172A", font=get_font(8 * scale, bold=True))
        cur_x += cw
        
    rep_rows = [
        ("1", "198501152010011001", "Ahmad Fauzi, S.Pd.", "5.0", "5.0", "5.0", "4.0", "0.2754", "Sangat Baik"),
        ("2", "198703222011012002", "Siti Nurhaliza, M.Pd.", "5.0", "5.0", "4.0", "4.0", "0.2669", "Sangat Baik"),
        ("3", "198904102014021003", "Budi Santoso, S.Si.", "5.0", "4.0", "5.0", "4.0", "0.2616", "Sangat Baik"),
        ("4", "199108182016011005", "Hendra Gunawan, S.Kom.", "5.0", "5.0", "4.0", "4.0", "0.2616", "Sangat Baik"),
        ("5", "199005122015032004", "Ratna Dewi, S.Pd.", "4.0", "5.0", "5.0", "4.0", "0.2480", "Baik"),
        ("6", "199211052017022006", "Dewi Lestari, M.Pd.", "4.0", "4.0", "5.0", "4.0", "0.2427", "Baik"),
    ]
    for idx, (rk, nip, name, c1, c2, c3, c4, yi, pred) in enumerate(rep_rows):
        ry = ty + 30 + idx * 36
        draw.line([(S(content_x + 60), S(ry + 36)), (S(w - 80), S(ry + 36))], fill="#E2E8F0", width=S(1))
        cur_x = content_x + 70
        row_vals = [(f"#{rk}", 60), (nip, 140), (name, 220), (c1, 80), (c2, 80), (c3, 80), (c4, 80), (yi, 90), (pred, 100)]
        for val, cw in row_vals:
            draw.text((S(cur_x), S(ry + 10)), str(val), fill="#0F172A", font=get_font(9 * scale, bold=(cw in (60, 220, 90))))
            cur_x += cw
            
    # Signature Footer in Report Preview
    draw.text((S(w - 320), S(560)), "Bandung, 30 Juni 2026", fill="#0F172A", font=get_font(9 * scale))
    draw.text((S(w - 320), S(576)), "Kepala Sekolah SMA Al-Ihsan,", fill="#0F172A", font=get_font(9 * scale))
    draw.text((S(w - 320), S(640)), "Dr. H. Mulyadi, M.Pd.", fill="#0F172A", font=get_font(9 * scale, bold=True))
    draw.text((S(w - 320), S(656)), "NIP. 197508122000031001", fill="#64748B", font=get_font(8 * scale))

    out_p = "system_screenshots/img_sys_10_laporan_cetak.png"
    img.save(out_p, quality=95)
    return out_p

# -------------------------------------------------------------
# 11. Kelola Akun Pengguna / User
# -------------------------------------------------------------
def generate_sys_11_kelola_pengguna():
    scale = 2
    w, h = 1300, 720
    img = Image.new("RGB", (w * scale, h * scale), "#F8FAFC")
    draw = ImageDraw.Draw(img)
    def S(v): return int(v * scale)
    
    draw_browser_chrome(draw, w, scale, "http://localhost:3000/admin/pengguna")
    draw_app_header(draw, w, h, scale, "Kelola Akun Pengguna / User", "Manajemen kredensial login, penetapan role, dan reset password", "Administrator", "Sugih Sugistiana (Admin)", "Juni 2026")
    draw_app_sidebar(draw, h, scale, active_menu="Pengguna")
    
    content_x = 260
    
    # Table Card
    draw_rounded_rect(draw, (S(content_x), S(158), S(w - 20), S(690)), radius=S(8), fill="#FFFFFF", outline="#E2E8F0", width=S(1))
    
    # Search & Action Bar
    draw_rounded_rect(draw, (S(content_x + 18), S(172), S(content_x + 350), S(206)), radius=S(6), fill="#F8FAFC", outline="#CBD5E1", width=S(1))
    draw.text((S(content_x + 32), S(181)), "🔍 Cari username / nama user...", fill="#94A3B8", font=get_font(10 * scale))
    
    draw_rounded_rect(draw, (S(w - 180), S(172), S(w - 36), S(206)), radius=S(6), fill="#059669")
    draw_centered_in_box(draw, (S(w - 180), S(172), S(w - 36), S(206)), "+ Tambah User", "#FFFFFF", get_font(10 * scale, bold=True))
    
    ty = 220
    draw.rectangle([(S(content_x), S(ty)), (S(w - 20), S(ty + 38))], fill="#F8FAFC")
    draw.line([(S(content_x), S(ty + 38)), (S(w - 20), S(ty + 38))], fill="#CBD5E1", width=S(1))
    
    cols = [("NO", 45), ("NAMA LENGKAP", 240), ("USERNAME", 160), ("ROLE / HAK AKSES", 170), ("RELASI GURU", 200), ("STATUS", 90)]
    cur_x = content_x + 15
    for cname, cw in cols:
        draw.text((S(cur_x), S(ty + 11)), cname, fill="#475569", font=get_font(9 * scale, bold=True))
        cur_x += cw
        
    users = [
        ("1", "Administrator Utama", "admin", "ADMIN", "-", "AKTIF", "#EFF6FF", "#1E40AF"),
        ("2", "Dr. H. Mulyadi, M.Pd.", "kepsek", "KEPALA_SEKOLAH", "-", "AKTIF", "#FEF3C7", "#92400E"),
        ("3", "Ahmad Fauzi, S.Pd.", "guru1", "GURU", "Ahmad Fauzi, S.Pd.", "AKTIF", "#ECFDF5", "#065F46"),
        ("4", "Siti Nurhaliza, M.Pd.", "guru2", "GURU", "Siti Nurhaliza, M.Pd.", "AKTIF", "#ECFDF5", "#065F46"),
        ("5", "Budi Santoso, S.Si.", "guru3", "GURU", "Budi Santoso, S.Si.", "AKTIF", "#ECFDF5", "#065F46"),
        ("6", "Ratna Dewi, S.Pd.", "guru4", "GURU", "Ratna Dewi, S.Pd.", "AKTIF", "#ECFDF5", "#065F46"),
        ("7", "Hendra Gunawan, S.Kom.", "guru5", "GURU", "Hendra Gunawan, S.Kom.", "AKTIF", "#ECFDF5", "#065F46"),
        ("8", "Dewi Lestari, M.Pd.", "guru6", "GURU", "Dewi Lestari, M.Pd.", "AKTIF", "#ECFDF5", "#065F46"),
    ]
    for idx, (no, name, uname, role, rel, st, bg_r, txt_r) in enumerate(users):
        ry = ty + 38 + idx * 52
        if idx % 2 == 1:
            draw.rectangle([(S(content_x + 1), S(ry)), (S(w - 21), S(ry + 52))], fill="#F8FAFC")
        draw.line([(S(content_x), S(ry + 52)), (S(w - 20), S(ry + 52))], fill="#F1F5F9", width=S(1))
        
        cur_x = content_x + 15
        draw.text((S(cur_x), S(ry + 16)), no, fill="#64748B", font=get_font(10 * scale))
        cur_x += 45
        draw.text((S(cur_x), S(ry + 16)), name, fill="#0F172A", font=get_font(10 * scale, bold=True))
        cur_x += 240
        draw.text((S(cur_x), S(ry + 16)), uname, fill="#475569", font=get_font(10 * scale))
        cur_x += 160
        
        # Role Badge
        draw_rounded_rect(draw, (S(cur_x), S(ry + 12), S(cur_x + 140), S(ry + 38)), radius=S(4), fill=bg_r, outline="#CBD5E1", width=S(1))
        draw_centered_in_box(draw, (S(cur_x), S(ry + 12), S(cur_x + 140), S(ry + 38)), role, txt_r, get_font(9 * scale, bold=True))
        cur_x += 170
        
        draw.text((S(cur_x), S(ry + 16)), rel, fill="#64748B", font=get_font(9 * scale))
        cur_x += 200
        
        # Status Pill
        draw_rounded_rect(draw, (S(cur_x), S(ry + 12), S(cur_x + 65), S(ry + 38)), radius=S(4), fill="#ECFDF5", outline="#A7F3D0", width=S(1))
        draw_centered_in_box(draw, (S(cur_x), S(ry + 12), S(cur_x + 65), S(ry + 38)), st, "#065F46", get_font(8 * scale, bold=True))

    out_p = "system_screenshots/img_sys_11_kelola_pengguna.png"
    img.save(out_p, quality=95)
    return out_p

# -------------------------------------------------------------
# 12. Dashboard & Profil Mandiri Guru
# -------------------------------------------------------------
def generate_sys_12_dashboard_guru():
    scale = 2
    w, h = 1300, 720
    img = Image.new("RGB", (w * scale, h * scale), "#F8FAFC")
    draw = ImageDraw.Draw(img)
    def S(v): return int(v * scale)
    
    draw_browser_chrome(draw, w, scale, "http://localhost:3000/guru/dashboard")
    draw_app_header(draw, w, h, scale, "Portal & Biodata Mandiri Guru", "Informasi pencapaian skor kriteria, peringkat kinerja, & catatan evaluasi", "Guru", "Ahmad Fauzi, S.Pd.", "Juni 2026")
    draw_app_sidebar(draw, h, scale, active_menu="Dashboard", role="GURU")
    
    content_x = 260
    content_w = w - content_x - 20
    
    # Profile Card
    draw_rounded_rect(draw, (S(content_x), S(158), S(w - 20), S(270)), radius=S(8), fill="#FFFFFF", outline="#E2E8F0", width=S(1))
    draw_rounded_rect(draw, (S(content_x + 20), S(176), S(content_x + 90), S(246)), radius=S(10), fill="#059669")
    draw_centered_in_box(draw, (S(content_x + 20), S(176), S(content_x + 90), S(246)), "AF", "#FFFFFF", get_font(20 * scale, bold=True))
    
    draw.text((S(content_x + 110), S(176)), "Ahmad Fauzi, S.Pd.", fill="#0F172A", font=get_font(15 * scale, bold=True))
    draw.text((S(content_x + 110), S(202)), "NIP: 198501152010011001 • Tugas Mengajar: Guru Matematika (Kelas 10 & 11)", fill="#475569", font=get_font(10 * scale))
    draw.text((S(content_x + 110), S(224)), "Tugas Tambahan Utama: Wakil Kepala Sekolah Bid. Kurikulum • Pembina OSIS", fill="#475569", font=get_font(10 * scale))
    draw.text((S(content_x + 110), S(244)), "Beban Jam Mengajar: 24 Jam Tatap Muka/Minggu • Status: Pendidik Aktif", fill="#059669", font=get_font(9 * scale, bold=True))
    
    # Result Badge Box
    draw_rounded_rect(draw, (S(w - 280), S(176), S(w - 40), S(252)), radius=S(8), fill="#FEF3C7", outline="#F59E0B", width=S(1))
    draw_centered_in_box(draw, (S(w - 280), S(184), S(w - 40), S(204)), "🥇 PERINGKAT #1", "#92400E", get_font(12 * scale, bold=True))
    draw_centered_in_box(draw, (S(w - 280), S(208), S(w - 40), S(230)), "Nilai Yi: 0.2754", "#0F172A", get_font(14 * scale, bold=True))
    draw_centered_in_box(draw, (S(w - 280), S(232), S(w - 40), S(248)), "Predikat: Sangat Baik", "#065F46", get_font(9 * scale, bold=True))
    
    # 4 Score Cards per Kriteria
    crit_w = (content_w - 36) // 4
    scores = [
        ("C1. KEHADIRAN", "Skor: 5.0", "Predikat: Sangat Baik", "Bobot: 35%", "#059669", "#ECFDF5"),
        ("C2. KETEPATAN WAKTU", "Skor: 5.0", "Predikat: Sangat Baik", "Bobot: 25%", "#2563EB", "#EFF6FF"),
        ("C3. PERANGKAT AJAR", "Skor: 5.0", "Predikat: Sangat Baik", "Bobot: 25%", "#D97706", "#FFFBEB"),
        ("C4. ADMINISTRASI NILAI", "Skor: 4.0", "Predikat: Baik", "Bobot: 15%", "#7C3AED", "#F5F3FF"),
    ]
    for idx, (title, score, pred, wgt, c_col, c_bg) in enumerate(scores):
        cx1 = content_x + idx * (crit_w + 12)
        cx2 = cx1 + crit_w
        draw_rounded_rect(draw, (S(cx1), S(285), S(cx2), S(420)), radius=S(8), fill="#FFFFFF", outline="#E2E8F0", width=S(1))
        draw_rounded_rect(draw, (S(cx1), S(285), S(cx2), S(290)), radius=S(2), fill=c_col)
        
        draw.text((S(cx1 + 16), S(302)), title, fill="#475569", font=get_font(9 * scale, bold=True))
        draw.text((S(cx1 + 16), S(324)), score, fill="#0F172A", font=get_font(16 * scale, bold=True))
        draw.text((S(cx1 + 16), S(358)), pred, fill=c_col, font=get_font(10 * scale, bold=True))
        draw.text((S(cx1 + 16), S(386)), wgt, fill="#94A3B8", font=get_font(9 * scale))
        
    # Feedback Card from Principal
    draw_rounded_rect(draw, (S(content_x), S(435), S(w - 20), S(690)), radius=S(8), fill="#FFFFFF", outline="#E2E8F0", width=S(1))
    draw.rectangle([(S(content_x), S(435)), (S(w - 20), S(475))], fill="#F8FAFC")
    draw.line([(S(content_x), S(475)), (S(w - 20), S(475))], fill="#E2E8F0", width=S(1))
    draw.text((S(content_x + 20), S(448)), "💬 Catatan & Umpan Balik Evaluasi dari Kepala Sekolah", fill="#0F172A", font=get_font(12 * scale, bold=True))
    
    draw_rounded_rect(draw, (S(content_x + 20), S(490), S(w - 40), S(590)), radius=S(6), fill="#F0FDF4", outline="#BBF7D0", width=S(1))
    draw.text((S(content_x + 36), S(506)), "\"Ahmad Fauzi, S.Pd. telah menunjukkan kinerja dan keteladanan yang luar biasa sepanjang periode evaluasi ini.", fill="#064E3B", font=get_font(10 * scale))
    draw.text((S(content_x + 36), S(528)), "Disiplin kehadiran 100%, penyusunan modul ajar berbasis Kurikulum Merdeka sangat lengkap, dan kepemimpinan", fill="#064E3B", font=get_font(10 * scale))
    draw.text((S(content_x + 36), S(550)), "sebagai Wakasek Kurikulum memberikan kontribusi positif yang signifikan bagi kemajuan akademik sekolah.\"", fill="#064E3B", font=get_font(10 * scale))
    
    draw.text((S(w - 320), S(610)), "Penilai: Dr. H. Mulyadi, M.Pd. (Kepala Sekolah)", fill="#0F172A", font=get_font(10 * scale, bold=True))
    draw.text((S(w - 320), S(630)), "Tanggal Verifikasi: 30 Juni 2026", fill="#64748B", font=get_font(9 * scale))

    out_p = "system_screenshots/img_sys_12_dashboard_guru.png"
    img.save(out_p, quality=95)
    return out_p

def generate_all_system_screenshots():
    funcs = [
        generate_sys_01_login,
        generate_sys_02_dashboard_admin,
        generate_sys_03_kelola_guru,
        generate_sys_04_kelola_kriteria,
        generate_sys_05_skala_penilaian,
        generate_sys_06_periode_penilaian,
        generate_sys_07_form_penilaian,
        generate_sys_08_proses_moora,
        generate_sys_09_ranking_guru,
        generate_sys_10_laporan_cetak,
        generate_sys_11_kelola_pengguna,
        generate_sys_12_dashboard_guru,
    ]
    for fn in funcs:
        p = fn()
        print(f"Generated system screenshot: {p}")

if __name__ == "__main__":
    generate_all_system_screenshots()
