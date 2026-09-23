import os
from PIL import Image, ImageDraw, ImageFont

os.makedirs("wireframes", exist_ok=True)

def get_font(size=14, bold=False):
    font_names = [
        "arialbd.ttf" if bold else "arial.ttf",
        "calibrib.ttf" if bold else "calibri.ttf",
        "segoeuib.ttf" if bold else "segoeui.ttf",
        "tahomabd.ttf" if bold else "tahoma.ttf"
    ]
    for fn in font_names:
        try:
            return ImageFont.truetype(fn, size)
        except Exception:
            continue
    return ImageFont.load_default()

def draw_centered_text(draw, cx, y, text, fill, font):
    bbox = draw.textbbox((0, 0), text, font=font)
    w = bbox[2] - bbox[0]
    draw.text((cx - w / 2, y), text, fill=fill, font=font)

def draw_centered_in_box(draw, box, text, fill, font):
    x1, y1, x2, y2 = box
    cx = (x1 + x2) / 2
    cy = (y1 + y2) / 2
    bbox = draw.textbbox((0, 0), text, font=font)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    # small baseline adjustment
    draw.text((cx - w / 2, cy - h / 2 - 1), text, fill=fill, font=font)

def draw_header_nav(draw, w, title="SMA AL-IHSAN BOARDING SCHOOL", role="Administrator", periode="Periode: Juni 2026"):
    # Topbar
    draw.rectangle([(0, 0), (w, 52)], fill="#FFFFFF", outline="#333333", width=2)
    f_bold = get_font(13, bold=True)
    f_small = get_font(10, bold=False)
    f_badge = get_font(10, bold=True)
    
    # Logo box placeholder
    draw.rectangle([(15, 9), (48, 43)], fill="#E5E7EB", outline="#333333", width=1)
    draw_centered_in_box(draw, (15, 9, 48, 43), "LOGO", "#111827", get_font(9, bold=True))
    
    # School / System Title
    draw.text((58, 11), title, fill="#111827", font=f_bold)
    draw.text((58, 29), "SPK Penilaian Kinerja Guru (Metode MOORA)", fill="#4B5563", font=f_small)
    
    # Periode Badge
    draw.rounded_rectangle([(w - 360, 12), (w - 190, 40)], radius=4, fill="#F3F4F6", outline="#9CA3AF", width=1)
    draw_centered_in_box(draw, (w - 360, 12, w - 190, 40), periode, "#374151", f_badge)
    
    # User badge
    draw.rounded_rectangle([(w - 180, 10), (w - 15, 42)], radius=4, fill="#FFFFFF", outline="#333333", width=1)
    draw.text((w - 170, 14), f"User: {role}", fill="#111827", font=get_font(10, bold=True))
    draw.text((w - 170, 27), "[ Logout ]", fill="#6B7280", font=get_font(9))

def draw_sidebar(draw, h, active_menu="Dashboard"):
    draw.rectangle([(0, 52), (200, h)], fill="#F9FAFB", outline="#333333", width=1)
    
    f_sec = get_font(9, bold=True)
    f_item = get_font(10, bold=False)
    f_active = get_font(10, bold=True)
    
    menus = [
        ("NAVIGASI UTAMA", None),
        ("Dashboard", "Dashboard"),
        ("Kelola Guru", "Guru"),
        ("Kelola Kriteria", "Kriteria"),
        ("Skala Penilaian", "Skala"),
        ("Periode Penilaian", "Periode"),
        ("EVALUASI & SPK", None),
        ("Transaksi Penilaian", "Penilaian"),
        ("Perhitungan MOORA", "MOORA"),
        ("Peringkat & Ranking", "Ranking"),
        ("Monitoring & Laporan", "Laporan"),
        ("SISTEM & AKUN", None),
        ("Kelola Pengguna", "Pengguna"),
        ("Log Aktivitas", "Log"),
    ]
    
    y = 66
    for text, key in menus:
        if key is None:
            draw.text((15, y), text, fill="#9CA3AF", font=f_sec)
            y += 20
        else:
            is_active = (key == active_menu or text == active_menu)
            if is_active:
                draw.rectangle([(8, y - 3), (192, y + 20)], fill="#E5E7EB", outline="#111827", width=1)
                draw.text((22, y), f"• {text}", fill="#111827", font=f_active)
            else:
                draw.text((22, y), f"  {text}", fill="#4B5563", font=f_item)
            y += 25

# 1. Wireframe Login (Clean without Demo Accounts, Perfectly Centered)
def make_wf_login():
    w, h = 900, 520
    img = Image.new("RGB", (w, h), "#F3F4F6")
    draw = ImageDraw.Draw(img)
    
    draw.rectangle([(0, 0), (w-1, h-1)], outline="#333333", width=2)
    
    # Centered Login Card
    cx, cy = w // 2, h // 2 - 10
    cw, ch = 420, 390
    x1, y1 = cx - cw // 2, cy - ch // 2
    x2, y2 = cx + cw // 2, cy + ch // 2
    
    draw.rounded_rectangle([(x1, y1), (x2, y2)], radius=10, fill="#FFFFFF", outline="#333333", width=2)
    
    # Card Header with Logo
    draw.rectangle([(x1, y1), (x2, y1 + 125)], fill="#FAFAFA", outline="#D1D5DB", width=1)
    
    # Logo Box
    lw, lh = 60, 42
    lx1, ly1 = cx - lw // 2, y1 + 14
    draw.rectangle([(lx1, ly1), (lx1 + lw, ly1 + lh)], fill="#E5E7EB", outline="#333333", width=1)
    draw_centered_in_box(draw, (lx1, ly1, lx1 + lw, ly1 + lh), "LOGO", "#111827", get_font(10, bold=True))
    
    draw_centered_text(draw, cx, y1 + 64, "SMA AL-IHSAN BOARDING SCHOOL", "#111827", get_font(12, bold=True))
    draw_centered_text(draw, cx, y1 + 84, "SPK PENILAIAN KINERJA GURU METODE MOORA", "#4B5563", get_font(9, bold=False))
    draw_centered_text(draw, cx, y1 + 102, "LOGIN MULTILEVEL PENGGUNA", "#6B7280", get_font(9, bold=True))
    
    # Form fields
    fy = y1 + 140
    # Username
    draw.text((x1 + 35, fy), "USERNAME", fill="#374151", font=get_font(9, bold=True))
    draw.rectangle([(x1 + 35, fy + 16), (x2 - 35, fy + 48)], fill="#FFFFFF", outline="#4B5563", width=1)
    draw.text((x1 + 48, fy + 24), "Masukkan username anda...", fill="#9CA3AF", font=get_font(10))
    
    # Password
    fy += 60
    draw.text((x1 + 35, fy), "PASSWORD", fill="#374151", font=get_font(9, bold=True))
    draw.rectangle([(x1 + 35, fy + 16), (x2 - 35, fy + 48)], fill="#FFFFFF", outline="#4B5563", width=1)
    draw.text((x1 + 48, fy + 24), "••••••••••••••••", fill="#9CA3AF", font=get_font(10))
    
    # Login Button
    fy += 64
    btn_box = (x1 + 35, fy, x2 - 35, fy + 40)
    draw.rounded_rectangle([btn_box[0:2], btn_box[2:4]], radius=6, fill="#E5E7EB", outline="#111827", width=2)
    draw_centered_in_box(draw, btn_box, "MASUK KE SISTEM ->", "#111827", get_font(11, bold=True))
    
    # Info note inside card
    draw_centered_text(draw, cx, y2 - 28, "Hak Akses: Administrator / Kepala Sekolah / Guru", "#6B7280", get_font(9))
    
    # Footer outside card
    draw_centered_text(draw, cx, h - 25, "© 2026 SMA Al-Ihsan Boarding School. Hak Cipta Dilindungi.", "#6B7280", get_font(9))
    
    img.save("wireframes/wf_01_login.png")

# 2. Dashboard Admin
def make_wf_dashboard_admin():
    w, h = 1000, 640
    img = Image.new("RGB", (w, h), "#FFFFFF")
    draw = ImageDraw.Draw(img)
    draw_header_nav(draw, w, role="Administrator")
    draw_sidebar(draw, h, active_menu="Dashboard")
    
    draw.text((220, 65), "Dashboard Administrator", fill="#111827", font=get_font(15, bold=True))
    draw.text((220, 85), "Ringkasan penilaian kinerja guru dan status kesiapan metode MOORA", fill="#6B7280", font=get_font(10))
    
    # 4 Stat Cards
    card_w = (w - 240 - 30) // 4
    stats = [
        ("Guru Aktif", "12 Guru", "Terdaftar di sistem"),
        ("Sudah Dinilai", "12 Guru", "Periode Juni 2026"),
        ("Belum Dinilai", "0 Guru", "Semua data lengkap"),
        ("Periode Aktif", "Juni 2026", "Tahun 2026"),
    ]
    for i, (stitle, sval, ssub) in enumerate(stats):
        cx1 = 220 + i * (card_w + 10)
        cx2 = cx1 + card_w
        draw.rounded_rectangle([(cx1, 110), (cx2, 185)], radius=6, fill="#FAFAFA", outline="#333333", width=1)
        draw.text((cx1 + 12, 118), stitle, fill="#4B5563", font=get_font(10, bold=True))
        draw.text((cx1 + 12, 136), sval, fill="#111827", font=get_font(15, bold=True))
        draw.text((cx1 + 12, 162), ssub, fill="#6B7280", font=get_font(9))
        draw.rectangle([(cx2 - 40, 118), (cx2 - 12, 146)], fill="#E5E7EB", outline="#9CA3AF", width=1)
        draw_centered_in_box(draw, (cx2 - 40, 118, cx2 - 12, 146), "[i]", "#374151", get_font(9, bold=True))
    
    # Progress & Status Box
    draw.rounded_rectangle([(220, 198), (w - 20, 305)], radius=6, fill="#FFFFFF", outline="#333333", width=1)
    draw.text((235, 210), "Status Kelengkapan Penilaian & SPK MOORA (Periode: Juni 2026)", fill="#111827", font=get_font(11, bold=True))
    draw.text((235, 228), "12 dari 12 guru aktif telah memiliki nilai lengkap (Kriteria C1, C2, C3, C4)", fill="#4B5563", font=get_font(9))
    
    # Progress Bar
    draw.rectangle([(235, 248), (w - 180, 264)], fill="#E5E7EB", outline="#9CA3AF", width=1)
    draw.rectangle([(235, 248), (w - 180, 264)], fill="#9CA3AF", outline="#333333", width=1)
    draw_centered_text(draw, w - 100, 249, "100% Lengkap", "#111827", get_font(10, bold=True))
    
    # Action Buttons
    b1 = (235, 274, 430, 298)
    draw.rounded_rectangle(b1, radius=4, fill="#E5E7EB", outline="#111827", width=1)
    draw_centered_in_box(draw, b1, "-> Hitung Ulang SPK MOORA", "#111827", get_font(9, bold=True))
    
    b2 = (440, 274, 600, 298)
    draw.rounded_rectangle(b2, radius=4, fill="#FFFFFF", outline="#4B5563", width=1)
    draw_centered_in_box(draw, b2, "Lihat Hasil Ranking ->", "#111827", get_font(9, bold=True))
    
    # 2 Columns: Leaderboard & Log Aktivitas
    col_w = (w - 240 - 15) // 2
    # Left: Leaderboard
    draw.rounded_rectangle([(220, 320), (220 + col_w, 620)], radius=6, fill="#FFFFFF", outline="#333333", width=1)
    draw.rectangle([(220, 320), (220 + col_w, 352)], fill="#F3F4F6", outline="#D1D5DB", width=1)
    draw.text((235, 329), "Top 3 Ranking Guru Terbaik (MOORA)", fill="#111827", font=get_font(10, bold=True))
    
    top_gurus = [
        ("1", "Ahmad Fauzi, S.Pd", "Matematika", "Yi: 0.3842 (Sangat Baik)"),
        ("2", "Siti Nurhaliza, M.Pd", "Bahasa Inggris", "Yi: 0.3510 (Baik)"),
        ("3", "Budi Santoso, S.Kom", "Informatika", "Yi: 0.3245 (Baik)"),
    ]
    for i, (rk, gnama, gmapel, gyi) in enumerate(top_gurus):
        gy = 365 + i * 78
        draw.rectangle([(235, gy), (220 + col_w - 15, gy + 68)], fill="#FAFAFA", outline="#E5E7EB", width=1)
        rbox = (245, gy + 14, 280, gy + 54)
        draw.rectangle(rbox, fill="#E5E7EB", outline="#333333", width=1)
        draw_centered_in_box(draw, rbox, f"#{rk}", "#111827", get_font(12, bold=True))
        draw.text((292, gy + 12), gnama, fill="#111827", font=get_font(10, bold=True))
        draw.text((292, gy + 30), f"Mapel: {gmapel}", fill="#6B7280", font=get_font(9))
        draw.text((292, gy + 47), gyi, fill="#374151", font=get_font(9, bold=True))
        
    # Right: Log Aktivitas
    draw.rounded_rectangle([(235 + col_w, 320), (w - 20, 620)], radius=6, fill="#FFFFFF", outline="#333333", width=1)
    draw.rectangle([(235 + col_w, 320), (w - 20, 352)], fill="#F3F4F6", outline="#D1D5DB", width=1)
    draw.text((250 + col_w, 329), "Log Aktivitas Sistem Terbaru", fill="#111827", font=get_font(10, bold=True))
    
    logs = [
        ("Hitung MOORA", "Admin melakukan kalkulasi SPK periode Juni 2026", "10 mnt lalu"),
        ("Input Nilai", "Kepsek menginput skor evaluasi guru Siti N.", "25 mnt lalu"),
        ("Update Kriteria", "Admin memperbarui bobot kriteria C1 (0.35)", "1 jam lalu"),
        ("Login Pengguna", "User 'admin' berhasil login ke sistem", "2 jam lalu"),
    ]
    for i, (lmod, lact, ltime) in enumerate(logs):
        ly = 365 + i * 60
        draw.text((250 + col_w, ly), f"• [{lmod}]", fill="#111827", font=get_font(9, bold=True))
        draw.text((250 + col_w, ly + 16), lact, fill="#4B5563", font=get_font(9))
        draw.text((250 + col_w, ly + 33), f"Waktu: {ltime}", fill="#9CA3AF", font=get_font(8))
        draw.line([(250 + col_w, ly + 52), (w - 35, ly + 52)], fill="#F3F4F6", width=1)

    img.save("wireframes/wf_02_dashboard_admin.png")

# 3. Kelola Data Guru
def make_wf_guru():
    w, h = 1000, 620
    img = Image.new("RGB", (w, h), "#FFFFFF")
    draw = ImageDraw.Draw(img)
    draw_header_nav(draw, w, role="Administrator")
    draw_sidebar(draw, h, active_menu="Guru")
    
    draw.text((220, 65), "Kelola Data Guru", fill="#111827", font=get_font(15, bold=True))
    draw.text((220, 85), "Master data guru, penugasan mengajar, dan beban kerja alternatif MOORA", fill="#6B7280", font=get_font(10))
    
    # Action Header Bar
    draw.rectangle([(220, 108), (w - 20, 150)], fill="#FAFAFA", outline="#333333", width=1)
    
    # Search Box
    draw.rectangle([(230, 115), (480, 143)], fill="#FFFFFF", outline="#9CA3AF", width=1)
    draw.text((240, 123), "Cari nama guru / NIP...", fill="#9CA3AF", font=get_font(9))
    
    # Filter
    draw.rectangle([(490, 115), (610, 143)], fill="#FFFFFF", outline="#9CA3AF", width=1)
    draw.text((500, 123), "Status: Aktif [v]", fill="#374151", font=get_font(9))
    
    # Button Tambah
    btn_add = (w - 170, 115, w - 30, 143)
    draw.rounded_rectangle(btn_add, radius=4, fill="#E5E7EB", outline="#111827", width=2)
    draw_centered_in_box(draw, btn_add, "+ Tambah Guru", "#111827", get_font(9, bold=True))
    
    # Table Grid
    ty = 160
    tw = w - 240
    draw.rectangle([(220, ty), (220 + tw, ty + 28)], fill="#E5E7EB", outline="#333333", width=1)
    
    cols = [
        ("No", 35, "center"),
        ("NIP", 95, "left"),
        ("Nama Lengkap", 165, "left"),
        ("L/P", 35, "center"),
        ("Tugas Mengajar", 140, "left"),
        ("Jam Ajar", 65, "center"),
        ("Rombel", 60, "center"),
        ("Status", 65, "center"),
        ("Aksi", 100, "center")
    ]
    cur_x = 220
    for cname, cwidth, align in cols:
        if align == "center":
            draw_centered_in_box(draw, (cur_x, ty, cur_x + cwidth, ty + 28), cname, "#111827", get_font(9, bold=True))
        else:
            draw.text((cur_x + 6, ty + 7), cname, fill="#111827", font=get_font(9, bold=True))
        draw.line([(cur_x + cwidth, ty), (cur_x + cwidth, ty + 28)], fill="#333333", width=1)
        cur_x += cwidth
        
    guru_rows = [
        ("1", "19850110201001", "Ahmad Fauzi, S.Pd", "L", "Guru Matematika", "24 Jam", "32 Siswa", "Aktif", "[Edit] [Hapus]"),
        ("2", "19880315201202", "Siti Nurhaliza, M.Pd", "P", "Guru Bhs Inggris", "26 Jam", "30 Siswa", "Aktif", "[Edit] [Hapus]"),
        ("3", "19900520201503", "Budi Santoso, S.Kom", "L", "Guru Informatika", "24 Jam", "34 Siswa", "Aktif", "[Edit] [Hapus]"),
        ("4", "19920725201804", "Dewi Lestari, S.Si", "P", "Guru Biologi", "22 Jam", "30 Siswa", "Aktif", "[Edit] [Hapus]"),
        ("5", "19871130201105", "Eko Prasetyo, M.Pd", "L", "Guru Fisika", "24 Jam", "32 Siswa", "Aktif", "[Edit] [Hapus]"),
        ("6", "19940214201906", "Fitri Handayani, S.Pd", "P", "Guru Bhs Indonesia", "28 Jam", "35 Siswa", "Aktif", "[Edit] [Hapus]"),
        ("7", "19890918201407", "Gunawan Wibowo, S.Pd", "L", "Guru Kimia", "22 Jam", "30 Siswa", "Aktif", "[Edit] [Hapus]"),
    ]
    ry = ty + 28
    for r_data in guru_rows:
        draw.rectangle([(220, ry), (220 + tw, ry + 28)], fill="#FFFFFF" if int(r_data[0])%2==1 else "#F9FAFB", outline="#D1D5DB", width=1)
        cur_x = 220
        for i, val in enumerate(r_data):
            cwidth = cols[i][1]
            align = cols[i][2]
            if align == "center":
                draw_centered_in_box(draw, (cur_x, ry, cur_x + cwidth, ry + 28), val, "#111827", get_font(8, bold=(i==7)))
            else:
                draw.text((cur_x + 6, ry + 7), val, fill="#111827", font=get_font(8, bold=(i==2)))
            draw.line([(cur_x + cwidth, ry), (cur_x + cwidth, ry + 28)], fill="#E5E7EB", width=1)
            cur_x += cwidth
        ry += 28
        
    # Pagination bar
    draw.rectangle([(220, ry), (220 + tw, ry + 28)], fill="#FAFAFA", outline="#333333", width=1)
    draw.text((230, ry + 7), "Menampilkan 1 - 7 dari 12 Guru", fill="#6B7280", font=get_font(8))
    draw_centered_text(draw, w - 120, ry + 7, "[< Prev]  1  2  [Next >]", "#111827", get_font(8, bold=True))
    
    # Form Modal Preview (Right Side)
    my = ry + 20
    draw.rounded_rectangle([(220, my), (w - 20, my + 145)], radius=6, fill="#FFFFFF", outline="#111827", width=2)
    draw.rectangle([(220, my), (w - 20, my + 24)], fill="#E5E7EB", outline="#9CA3AF", width=1)
    draw.text((235, my + 5), "Modal Form: Tambah / Edit Data Master Guru", fill="#111827", font=get_font(9, bold=True))
    
    draw.text((235, my + 34), "NIP: [ 19850110201001________ ]      Nama: [ Ahmad Fauzi, S.Pd_______________ ]", fill="#374151", font=get_font(8))
    draw.text((235, my + 58), "JK: (o) Laki-laki  ( ) Perempuan     Tugas Mengajar: [ Guru Matematika________ ]", fill="#374151", font=get_font(8))
    draw.text((235, my + 82), "Jam Ajar: [ 24 Jam ]   Rombel: [ 32 Siswa ]   Mengajar: [v] Kls 10  [v] Kls 11  [ ] Kls 12", fill="#374151", font=get_font(8))
    
    draw.rounded_rectangle([(w - 170, my + 110), (w - 100, my + 134)], radius=3, fill="#F3F4F6", outline="#9CA3AF", width=1)
    draw_centered_in_box(draw, (w - 170, my + 110, w - 100, my + 134), "Batal", "#374151", get_font(8))
    
    draw.rounded_rectangle([(w - 90, my + 110), (w - 30, my + 134)], radius=3, fill="#E5E7EB", outline="#111827", width=1)
    draw_centered_in_box(draw, (w - 90, my + 110, w - 30, my + 134), "Simpan", "#111827", get_font(8, bold=True))

    img.save("wireframes/wf_03_kelola_guru.png")

# 4. Kelola Kriteria & Bobot
def make_wf_kriteria():
    w, h = 1000, 580
    img = Image.new("RGB", (w, h), "#FFFFFF")
    draw = ImageDraw.Draw(img)
    draw_header_nav(draw, w, role="Administrator")
    draw_sidebar(draw, h, active_menu="Kriteria")
    
    draw.text((220, 65), "Kelola Kriteria & Bobot Penilaian", fill="#111827", font=get_font(15, bold=True))
    draw.text((220, 85), "Konfigurasi kriteria evaluasi kinerja, bobot preferensi (total 1.00), dan jenis MOORA", fill="#6B7280", font=get_font(10))
    
    # Info Box
    draw.rounded_rectangle([(220, 108), (w - 20, 150)], radius=6, fill="#FAFAFA", outline="#333333", width=1)
    draw.text((235, 116), "Status Total Bobot: 1.00 (100%) - Valid untuk Kalkulasi MOORA", fill="#111827", font=get_font(10, bold=True))
    draw.text((235, 132), "Sifat BENEFIT memaksimalkan nilai evaluasi, sedangkan COST meminimalkan nilai preferensi.", fill="#4B5563", font=get_font(9))
    
    # Table Kriteria
    ty = 162
    tw = w - 240
    draw.rectangle([(220, ty), (220 + tw, ty + 28)], fill="#E5E7EB", outline="#333333", width=1)
    
    cols = [
        ("No", 35, "center"),
        ("Kode", 65, "center"),
        ("Nama Kriteria Penilaian", 220, "left"),
        ("Bobot", 75, "center"),
        ("Persentase", 85, "center"),
        ("Jenis MOORA", 110, "center"),
        ("Status", 70, "center"),
        ("Aksi", 100, "center")
    ]
    cur_x = 220
    for cname, cwidth, align in cols:
        if align == "center":
            draw_centered_in_box(draw, (cur_x, ty, cur_x + cwidth, ty + 28), cname, "#111827", get_font(9, bold=True))
        else:
            draw.text((cur_x + 6, ty + 7), cname, fill="#111827", font=get_font(9, bold=True))
        draw.line([(cur_x + cwidth, ty), (cur_x + cwidth, ty + 28)], fill="#333333", width=1)
        cur_x += cwidth
        
    k_rows = [
        ("1", "C1", "Kompetensi Pedagogik", "0.35", "35%", "BENEFIT", "Aktif", "[Edit / Atur]"),
        ("2", "C2", "Kompetensi Profesional", "0.25", "25%", "BENEFIT", "Aktif", "[Edit / Atur]"),
        ("3", "C3", "Kompetensi Kepribadian", "0.25", "25%", "BENEFIT", "Aktif", "[Edit / Atur]"),
        ("4", "C4", "Kompetensi Sosial", "0.15", "15%", "BENEFIT", "Aktif", "[Edit / Atur]"),
    ]
    ry = ty + 28
    for r in k_rows:
        draw.rectangle([(220, ry), (220 + tw, ry + 32)], fill="#FFFFFF", outline="#D1D5DB", width=1)
        cur_x = 220
        for i, val in enumerate(r):
            cwidth = cols[i][1]
            align = cols[i][2]
            if align == "center":
                draw_centered_in_box(draw, (cur_x, ry, cur_x + cwidth, ry + 32), val, "#111827", get_font(9, bold=(i in (1, 3))))
            else:
                draw.text((cur_x + 6, ry + 8), val, fill="#111827", font=get_font(9))
            draw.line([(cur_x + cwidth, ry), (cur_x + cwidth, ry + 32)], fill="#E5E7EB", width=1)
            cur_x += cwidth
        ry += 32
        
    # Modal Form Edit Kriteria
    my = ry + 25
    draw.rounded_rectangle([(220, my), (w - 20, my + 155)], radius=6, fill="#FFFFFF", outline="#333333", width=1)
    draw.rectangle([(220, my), (w - 20, my + 26)], fill="#E5E7EB", outline="#9CA3AF", width=1)
    draw.text((235, my + 6), "Form Pengaturan Bobot & Parameter Kriteria", fill="#111827", font=get_font(10, bold=True))
    
    draw.text((235, my + 40), "Kode Kriteria: [ C1 ]          Nama Kriteria: [ Kompetensi Pedagogik___________________ ]", fill="#374151", font=get_font(9))
    draw.text((235, my + 68), "Bobot (0.00 - 1.00): [ 0.35 ]   Jenis MOORA: (o) BENEFIT   ( ) COST", fill="#374151", font=get_font(9))
    draw.text((235, my + 94), "Status: [v] Aktif digunakan dalam proses penilaian kinerja periode berjalan", fill="#374151", font=get_font(9))
    
    draw.rounded_rectangle([(w - 180, my + 120), (w - 105, my + 145)], radius=4, fill="#F3F4F6", outline="#9CA3AF", width=1)
    draw_centered_in_box(draw, (w - 180, my + 120, w - 105, my + 145), "Batal", "#374151", get_font(9))
    
    draw.rounded_rectangle([(w - 95, my + 120), (w - 30, my + 145)], radius=4, fill="#E5E7EB", outline="#111827", width=2)
    draw_centered_in_box(draw, (w - 95, my + 120, w - 30, my + 145), "Simpan", "#111827", get_font(9, bold=True))

    img.save("wireframes/wf_04_kelola_kriteria.png")

# 5. Skala Penilaian / Rubrik
def make_wf_skala():
    w, h = 1000, 560
    img = Image.new("RGB", (w, h), "#FFFFFF")
    draw = ImageDraw.Draw(img)
    draw_header_nav(draw, w, role="Administrator")
    draw_sidebar(draw, h, active_menu="Skala")
    
    draw.text((220, 65), "Kelola Skala Penilaian & Rubrik Capaian", fill="#111827", font=get_font(15, bold=True))
    draw.text((220, 85), "Panduan indikator skor kuantitatif (1 sampai 5) sebagai acuan penilaian kriteria", fill="#6B7280", font=get_font(10))
    
    # Filter
    draw.rectangle([(220, 108), (w - 20, 146)], fill="#FAFAFA", outline="#333333", width=1)
    draw.text((235, 120), "Pilih Kriteria: [ C1 - Kompetensi Pedagogik (Bobot 35%)  v ]", fill="#111827", font=get_font(10, bold=True))
    
    # Table Rubrik
    ty = 160
    tw = w - 240
    draw.rectangle([(220, ty), (220 + tw, ty + 28)], fill="#E5E7EB", outline="#333333", width=1)
    
    cols = [
        ("No", 35, "center"),
        ("Nilai", 55, "center"),
        ("Predikat / Label", 130, "left"),
        ("Deskripsi Indikator Ketercapaian Kompetensi", 450, "left"),
        ("Aksi", 90, "center")
    ]
    cur_x = 220
    for cname, cwidth, align in cols:
        if align == "center":
            draw_centered_in_box(draw, (cur_x, ty, cur_x + cwidth, ty + 28), cname, "#111827", get_font(9, bold=True))
        else:
            draw.text((cur_x + 6, ty + 7), cname, fill="#111827", font=get_font(9, bold=True))
        draw.line([(cur_x + cwidth, ty), (cur_x + cwidth, ty + 28)], fill="#333333", width=1)
        cur_x += cwidth
        
    skala_rows = [
        ("1", "5", "Sangat Baik", "Mampu menyusun modul ajar interaktif, perangkat lengkap & inovatif", "[Edit] [Hapus]"),
        ("2", "4", "Baik", "Menyusun perangkat ajar terstruktur dan melaksanakan KBM sesuai RPP", "[Edit] [Hapus]"),
        ("3", "3", "Cukup", "Perangkat pembelajaran cukup lengkap namun variasi metode masih standar", "[Edit] [Hapus]"),
        ("4", "2", "Kurang", "Sebagian perangkat ajar belum terselesaikan tepat waktu", "[Edit] [Hapus]"),
        ("5", "1", "Sangat Kurang", "Tidak melengkapi modul ajar dan administrasi pembelajaran", "[Edit] [Hapus]"),
    ]
    ry = ty + 28
    for r in skala_rows:
        draw.rectangle([(220, ry), (220 + tw, ry + 32)], fill="#FFFFFF", outline="#D1D5DB", width=1)
        cur_x = 220
        for i, val in enumerate(r):
            cwidth = cols[i][1]
            align = cols[i][2]
            if align == "center":
                draw_centered_in_box(draw, (cur_x, ry, cur_x + cwidth, ry + 32), val, "#111827", get_font(9, bold=(i==1)))
            else:
                draw.text((cur_x + 6, ry + 8), val, fill="#111827", font=get_font(8, bold=(i==2)))
            draw.line([(cur_x + cwidth, ry), (cur_x + cwidth, ry + 32)], fill="#E5E7EB", width=1)
            cur_x += cwidth
        ry += 32

    img.save("wireframes/wf_05_skala_penilaian.png")

# 6. Periode Penilaian
def make_wf_periode():
    w, h = 1000, 540
    img = Image.new("RGB", (w, h), "#FFFFFF")
    draw = ImageDraw.Draw(img)
    draw_header_nav(draw, w, role="Administrator")
    draw_sidebar(draw, h, active_menu="Periode")
    
    draw.text((220, 65), "Kelola Periode Penilaian", fill="#111827", font=get_font(15, bold=True))
    draw.text((220, 85), "Manajemen gelombang waktu penilaian evaluasi kinerja guru (Bulanan/Semesteran)", fill="#6B7280", font=get_font(10))
    
    draw.rectangle([(220, 108), (w - 20, 146)], fill="#FAFAFA", outline="#333333", width=1)
    draw.text((235, 120), "Daftar Gelombang Periode Evaluasi Guru", fill="#111827", font=get_font(10, bold=True))
    
    btn_p = (w - 180, 114, w - 30, 140)
    draw.rounded_rectangle(btn_p, radius=4, fill="#E5E7EB", outline="#111827", width=2)
    draw_centered_in_box(draw, btn_p, "+ Tambah Periode", "#111827", get_font(9, bold=True))
    
    ty = 158
    tw = w - 240
    draw.rectangle([(220, ty), (220 + tw, ty + 28)], fill="#E5E7EB", outline="#333333", width=1)
    
    cols = [
        ("No", 35, "center"),
        ("Bulan", 100, "left"),
        ("Tahun", 75, "center"),
        ("Nama Periode", 160, "left"),
        ("Status", 100, "center"),
        ("Jumlah Dinilai", 120, "center"),
        ("Aksi / Kontrol", 170, "center")
    ]
    cur_x = 220
    for cname, cwidth, align in cols:
        if align == "center":
            draw_centered_in_box(draw, (cur_x, ty, cur_x + cwidth, ty + 28), cname, "#111827", get_font(9, bold=True))
        else:
            draw.text((cur_x + 6, ty + 7), cname, fill="#111827", font=get_font(9, bold=True))
        draw.line([(cur_x + cwidth, ty), (cur_x + cwidth, ty + 28)], fill="#333333", width=1)
        cur_x += cwidth
        
    p_rows = [
        ("1", "Juni", "2026", "Juni 2026", "[ AKTIF ]", "12 / 12 Guru", "[Tutup Periode] [Edit]"),
        ("2", "Mei", "2026", "Mei 2026", "[ SELESAI ]", "12 / 12 Guru", "[Buka Kembali] [Lihat]"),
        ("3", "April", "2026", "April 2026", "[ SELESAI ]", "12 / 12 Guru", "[Buka Kembali] [Lihat]"),
    ]
    ry = ty + 28
    for r in p_rows:
        draw.rectangle([(220, ry), (220 + tw, ry + 32)], fill="#FFFFFF", outline="#D1D5DB", width=1)
        cur_x = 220
        for i, val in enumerate(r):
            cwidth = cols[i][1]
            align = cols[i][2]
            if align == "center":
                draw_centered_in_box(draw, (cur_x, ry, cur_x + cwidth, ry + 32), val, "#111827", get_font(9, bold=(i in (3, 4))))
            else:
                draw.text((cur_x + 6, ry + 8), val, fill="#111827", font=get_font(9, bold=(i==3)))
            draw.line([(cur_x + cwidth, ry), (cur_x + cwidth, ry + 32)], fill="#E5E7EB", width=1)
            cur_x += cwidth
        ry += 32

    img.save("wireframes/wf_06_periode_penilaian.png")

# 7. Form Transaksi Penilaian Kinerja Guru
def make_wf_penilaian():
    w, h = 1000, 640
    img = Image.new("RGB", (w, h), "#FFFFFF")
    draw = ImageDraw.Draw(img)
    draw_header_nav(draw, w, role="Kepala Sekolah / Admin")
    draw_sidebar(draw, h, active_menu="Penilaian")
    
    draw.text((220, 65), "Form Transaksi Penilaian Kinerja Guru", fill="#111827", font=get_font(15, bold=True))
    draw.text((220, 85), "Input skor evaluasi kriteria guru (Skala 1 - 5) untuk periode aktif", fill="#6B7280", font=get_font(10))
    
    # Guru Info Card
    draw.rounded_rectangle([(220, 108), (w - 20, 168)], radius=6, fill="#FAFAFA", outline="#333333", width=1)
    draw.text((235, 116), "Guru: Ahmad Fauzi, S.Pd  |  NIP: 19850110201001", fill="#111827", font=get_font(11, bold=True))
    draw.text((235, 134), "Mata Pelajaran: Guru Matematika  |  Beban: 24 Jam Tatap Muka  |  Periode: Juni 2026", fill="#4B5563", font=get_font(9))
    draw.text((235, 150), "Evaluator / Penilai: Kepala Sekolah", fill="#6B7280", font=get_font(9, bold=True))
    
    # 4 Criteria Cards
    cy = 180
    criteria_inputs = [
        ("C1", "Kompetensi Pedagogik (Bobot 35%)", "Kemampuan mengelola pembelajaran, penyusunan RPP/Modul, dan penguasaan kelas", "Nilai: ( ) 1  ( ) 2  ( ) 3  (o) 4  ( ) 5  -> Skor: 4.0 (Baik)"),
        ("C2", "Kompetensi Profesional (Bobot 25%)", "Penguasaan materi bidang studi luas dan mendalam serta pemanfaatan IPTEK", "Nilai: ( ) 1  ( ) 2  ( ) 3  ( ) 4  (o) 5  -> Skor: 5.0 (Sangat Baik)"),
        ("C3", "Kompetensi Kepribadian (Bobot 25%)", "Kedisiplinan, keteladanan akhlak, etika kerja, dan tanggung jawab dinas", "Nilai: ( ) 1  ( ) 2  ( ) 3  (o) 4  ( ) 5  -> Skor: 4.0 (Baik)"),
        ("C4", "Kompetensi Sosial (Bobot 15%)", "Komunikasi efektif dengan rekan sejawat, siswa, wali murid, dan masyarakat", "Nilai: ( ) 1  ( ) 2  ( ) 3  ( ) 4  (o) 5  -> Skor: 5.0 (Sangat Baik)"),
    ]
    for code, name, desc, radio in criteria_inputs:
        draw.rounded_rectangle([(220, cy), (w - 20, cy + 68)], radius=4, fill="#FFFFFF", outline="#9CA3AF", width=1)
        draw.rectangle([(220, cy), (265, cy + 68)], fill="#E5E7EB", outline="#9CA3AF", width=1)
        draw_centered_in_box(draw, (220, cy, 265, cy + 68), code, "#111827", get_font(13, bold=True))
        
        draw.text((275, cy + 8), name, fill="#111827", font=get_font(10, bold=True))
        draw.text((275, cy + 26), desc, fill="#6B7280", font=get_font(8))
        draw.text((275, cy + 46), radio, fill="#111827", font=get_font(9, bold=True))
        cy += 74
        
    # Catatan Evaluator Box
    draw.rounded_rectangle([(220, cy), (w - 20, cy + 60)], radius=4, fill="#FAFAFA", outline="#9CA3AF", width=1)
    draw.text((230, cy + 6), "Catatan Evaluasi / Rekomendasi Kepala Sekolah (Opsional):", fill="#374151", font=get_font(9, bold=True))
    draw.text((230, cy + 28), "Pertahankan kinerja pembelajaran interaktif di kelas dan terus tingkatkan inovasi digital...", fill="#6B7280", font=get_font(8))
    
    # Action Buttons
    btn_sd = (w - 260, cy + 68, w - 150, cy + 96)
    draw.rounded_rectangle(btn_sd, radius=4, fill="#F3F4F6", outline="#9CA3AF", width=1)
    draw_centered_in_box(draw, btn_sd, "Simpan Draft", "#374151", get_font(9))
    
    btn_ss = (w - 140, cy + 68, w - 20, cy + 96)
    draw.rounded_rectangle(btn_ss, radius=4, fill="#E5E7EB", outline="#111827", width=2)
    draw_centered_in_box(draw, btn_ss, "Simpan Selesai ->", "#111827", get_font(9, bold=True))

    img.save("wireframes/wf_07_form_penilaian.png")

# 8. Proses Perhitungan MOORA
def make_wf_moora():
    w, h = 1000, 620
    img = Image.new("RGB", (w, h), "#FFFFFF")
    draw = ImageDraw.Draw(img)
    draw_header_nav(draw, w, role="Administrator")
    draw_sidebar(draw, h, active_menu="MOORA")
    
    draw.text((220, 65), "Perhitungan SPK Metode MOORA", fill="#111827", font=get_font(15, bold=True))
    draw.text((220, 85), "Tahapan matriks keputusan, normalisasi vektor, pembobotan, dan nilai preferensi Yi", fill="#6B7280", font=get_font(10))
    
    draw.rounded_rectangle([(220, 108), (w - 20, 155)], radius=6, fill="#FAFAFA", outline="#333333", width=1)
    draw.text((235, 116), "Status Data: 12 Guru Lengkap Dinilai  |  Periode: Juni 2026", fill="#111827", font=get_font(10, bold=True))
    draw.text((235, 134), "Formula MOORA: Yi = Sum(Max Benefit) - Sum(Min Cost)", fill="#4B5563", font=get_font(9))
    
    btn_calc = (w - 200, 115, w - 30, 146)
    draw.rounded_rectangle(btn_calc, radius=4, fill="#E5E7EB", outline="#111827", width=2)
    draw_centered_in_box(draw, btn_calc, "PROSES KALKULASI", "#111827", get_font(9, bold=True))
    
    # Tab Matrix Selector
    tabs = ["1. Matriks Keputusan (X)", "2. Matriks Normalisasi (X*)", "3. Matriks Terbobot (W*X*)", "4. Nilai Preferensi (Yi)"]
    tx = 220
    for i, tname in enumerate(tabs):
        tw_tab = 180
        is_sel = (i == 3)
        draw.rectangle([(tx, 168), (tx + tw_tab, 192)], fill="#FFFFFF" if is_sel else "#F3F4F6", outline="#333333" if is_sel else "#D1D5DB", width=1)
        draw_centered_in_box(draw, (tx, 168, tx + tw_tab, 192), tname, "#111827" if is_sel else "#6B7280", get_font(8, bold=is_sel))
        tx += tw_tab + 5
        
    ty = 200
    tw = w - 240
    draw.rectangle([(220, ty), (220 + tw, ty + 28)], fill="#E5E7EB", outline="#333333", width=1)
    
    cols = [
        ("No", 35, "center"),
        ("Nama Guru (Alternatif)", 180, "left"),
        ("C1 (0.35)", 95, "center"),
        ("C2 (0.25)", 95, "center"),
        ("C3 (0.25)", 95, "center"),
        ("C4 (0.15)", 95, "center"),
        ("Nilai Yi", 95, "center"),
        ("Ranking", 70, "center")
    ]
    cur_x = 220
    for cname, cwidth, align in cols:
        if align == "center":
            draw_centered_in_box(draw, (cur_x, ty, cur_x + cwidth, ty + 28), cname, "#111827", get_font(9, bold=True))
        else:
            draw.text((cur_x + 6, ty + 7), cname, fill="#111827", font=get_font(9, bold=True))
        draw.line([(cur_x + cwidth, ty), (cur_x + cwidth, ty + 28)], fill="#333333", width=1)
        cur_x += cwidth
        
    moora_rows = [
        ("1", "Ahmad Fauzi, S.Pd", "0.1082", "0.1082", "0.0890", "0.0788", "0.3842", "Rank 1"),
        ("2", "Siti Nurhaliza, M.Pd", "0.1082", "0.0866", "0.0890", "0.0672", "0.3510", "Rank 2"),
        ("3", "Budi Santoso, S.Kom", "0.0812", "0.0866", "0.0890", "0.0672", "0.3245", "Rank 3"),
        ("4", "Dewi Lestari, S.Si", "0.0812", "0.0866", "0.0668", "0.0672", "0.3018", "Rank 4"),
        ("5", "Eko Prasetyo, M.Pd", "0.0812", "0.0649", "0.0668", "0.0672", "0.2801", "Rank 5"),
    ]
    ry = ty + 28
    for r in moora_rows:
        draw.rectangle([(220, ry), (220 + tw, ry + 28)], fill="#FFFFFF", outline="#D1D5DB", width=1)
        cur_x = 220
        for i, val in enumerate(r):
            cwidth = cols[i][1]
            align = cols[i][2]
            if align == "center":
                draw_centered_in_box(draw, (cur_x, ry, cur_x + cwidth, ry + 28), val, "#111827", get_font(8, bold=(i in (6, 7))))
            else:
                draw.text((cur_x + 6, ry + 7), val, fill="#111827", font=get_font(8))
            draw.line([(cur_x + cwidth, ry), (cur_x + cwidth, ry + 28)], fill="#E5E7EB", width=1)
            cur_x += cwidth
        ry += 28
        
    draw.rounded_rectangle([(220, ry + 15), (w - 20, ry + 60)], radius=4, fill="#FAFAFA", outline="#9CA3AF", width=1)
    draw.text((235, ry + 24), "Keterangan Hasil Optimasi MOORA:", fill="#111827", font=get_font(9, bold=True))
    draw.text((235, ry + 40), "Peringkat tertinggi diraih oleh alternatif dengan nilai preferensi (Yi) terbesar.", fill="#4B5563", font=get_font(8))

    img.save("wireframes/wf_08_proses_moora.png")

# 9. Ranking Guru
def make_wf_ranking():
    w, h = 1000, 580
    img = Image.new("RGB", (w, h), "#FFFFFF")
    draw = ImageDraw.Draw(img)
    draw_header_nav(draw, w, role="Administrator / Kepala Sekolah")
    draw_sidebar(draw, h, active_menu="Ranking")
    
    draw.text((220, 65), "Peringkat & Hasil Ranking Guru (MOORA)", fill="#111827", font=get_font(15, bold=True))
    draw.text((220, 85), "Daftar urutan kelayakan kinerja guru hasil metode MOORA periode Juni 2026", fill="#6B7280", font=get_font(10))
    
    pod_w = (w - 240 - 20) // 3
    podiums = [
        ("RANK 2 (Juara 2)", "Siti Nurhaliza, M.Pd", "Nilai Yi: 0.3510", "Predikat: Baik"),
        ("RANK 1 (Juara 1)", "Ahmad Fauzi, S.Pd", "Nilai Yi: 0.3842", "Predikat: Sangat Baik"),
        ("RANK 3 (Juara 3)", "Budi Santoso, S.Kom", "Nilai Yi: 0.3245", "Predikat: Baik"),
    ]
    for i, (prank, pname, pyi, ppred) in enumerate(podiums):
        px1 = 220 + i * (pod_w + 10)
        px2 = px1 + pod_w
        is_first = (i == 1)
        draw.rounded_rectangle([(px1, 108), (px2, 200)], radius=6, fill="#E5E7EB" if is_first else "#FAFAFA", outline="#111827" if is_first else "#9CA3AF", width=2 if is_first else 1)
        draw_centered_text(draw, (px1 + px2) / 2, 118, prank, "#111827", get_font(10, bold=True))
        draw_centered_text(draw, (px1 + px2) / 2, 138, pname, "#111827", get_font(11, bold=True))
        draw_centered_text(draw, (px1 + px2) / 2, 158, pyi, "#374151", get_font(9, bold=True))
        draw_centered_text(draw, (px1 + px2) / 2, 176, ppred, "#6B7280", get_font(8))
        
    ty = 215
    tw = w - 240
    draw.rectangle([(220, ty), (220 + tw, ty + 28)], fill="#E5E7EB", outline="#333333", width=1)
    
    cols = [
        ("Peringkat", 75, "center"),
        ("NIP", 105, "left"),
        ("Nama Lengkap Guru", 185, "left"),
        ("Mata Pelajaran", 135, "left"),
        ("Nilai Preferensi (Yi)", 130, "center"),
        ("Status Predikat", 130, "center")
    ]
    cur_x = 220
    for cname, cwidth, align in cols:
        if align == "center":
            draw_centered_in_box(draw, (cur_x, ty, cur_x + cwidth, ty + 28), cname, "#111827", get_font(9, bold=True))
        else:
            draw.text((cur_x + 6, ty + 7), cname, fill="#111827", font=get_font(9, bold=True))
        draw.line([(cur_x + cwidth, ty), (cur_x + cwidth, ty + 28)], fill="#333333", width=1)
        cur_x += cwidth
        
    rk_rows = [
        ("Rank 1", "19850110201001", "Ahmad Fauzi, S.Pd", "Guru Matematika", "0.3842", "Sangat Baik"),
        ("Rank 2", "19880315201202", "Siti Nurhaliza, M.Pd", "Guru Bhs Inggris", "0.3510", "Baik"),
        ("Rank 3", "19900520201503", "Budi Santoso, S.Kom", "Guru Informatika", "0.3245", "Baik"),
        ("Rank 4", "19920725201804", "Dewi Lestari, S.Si", "Guru Biologi", "0.3018", "Cukup"),
        ("Rank 5", "19871130201105", "Eko Prasetyo, M.Pd", "Guru Fisika", "0.2801", "Cukup"),
    ]
    ry = ty + 28
    for r in rk_rows:
        draw.rectangle([(220, ry), (220 + tw, ry + 28)], fill="#FFFFFF", outline="#D1D5DB", width=1)
        cur_x = 220
        for i, val in enumerate(r):
            cwidth = cols[i][1]
            align = cols[i][2]
            if align == "center":
                draw_centered_in_box(draw, (cur_x, ry, cur_x + cwidth, ry + 28), val, "#111827", get_font(8, bold=(i in (0, 4))))
            else:
                draw.text((cur_x + 6, ry + 7), val, fill="#111827", font=get_font(8))
            draw.line([(cur_x + cwidth, ry), (cur_x + cwidth, ry + 28)], fill="#E5E7EB", width=1)
            cur_x += cwidth
        ry += 28

    img.save("wireframes/wf_09_ranking_guru.png")

# 10. Laporan & Cetak
def make_wf_laporan():
    w, h = 1000, 580
    img = Image.new("RGB", (w, h), "#FFFFFF")
    draw = ImageDraw.Draw(img)
    draw_header_nav(draw, w, role="Administrator / Kepala Sekolah")
    draw_sidebar(draw, h, active_menu="Laporan")
    
    draw.text((220, 65), "Laporan & Cetak Rekapitulasi SPK", fill="#111827", font=get_font(15, bold=True))
    draw.text((220, 85), "Ekspor dan cetak laporan hasil evaluasi kinerja guru format PDF dan Excel", fill="#6B7280", font=get_font(10))
    
    draw.rectangle([(220, 108), (w - 20, 152)], fill="#FAFAFA", outline="#333333", width=1)
    draw.text((235, 122), "Periode: [ Juni 2026  v ]    Kategori: [ Semua Guru  v ]", fill="#111827", font=get_font(10, bold=True))
    
    btn_pdf = (w - 280, 115, w - 160, 144)
    draw.rounded_rectangle(btn_pdf, radius=4, fill="#E5E7EB", outline="#111827", width=1)
    draw_centered_in_box(draw, btn_pdf, "[PDF] Cetak Laporan", "#111827", get_font(9, bold=True))
    
    btn_xls = (w - 150, 115, w - 30, 144)
    draw.rounded_rectangle(btn_xls, radius=4, fill="#F3F4F6", outline="#4B5563", width=1)
    draw_centered_in_box(draw, btn_xls, "[XLS] Export Excel", "#374151", get_font(9, bold=True))
    
    py = 168
    draw.rounded_rectangle([(220, py), (w - 20, h - 20)], radius=6, fill="#FFFFFF", outline="#9CA3AF", width=1)
    
    # Centered PDF Report Header
    draw_centered_text(draw, (220 + w - 20) / 2, py + 14, "LAPORAN HASIL EVALUASI PENILAIAN KINERJA GURU", "#111827", get_font(11, bold=True))
    draw_centered_text(draw, (220 + w - 20) / 2, py + 30, "SMA AL-IHSAN BOARDING SCHOOL", "#111827", get_font(10, bold=True))
    draw_centered_text(draw, (220 + w - 20) / 2, py + 46, "Periode Penilaian: Juni 2026", "#6B7280", get_font(9))
    draw.line([(240, py + 64), (w - 40, py + 64)], fill="#111827", width=2)
    
    # Table inside Report
    draw.rectangle([(240, py + 74), (w - 40, py + 98)], fill="#E5E7EB", outline="#333333", width=1)
    draw.text((250, py + 80), "No   NIP                Nama Guru                 C1    C2    C3    C4    Nilai Yi    Ranking   Keterangan", fill="#111827", font=get_font(9, bold=True))
    
    draw.text((250, py + 106), "1    19850110201001     Ahmad Fauzi, S.Pd         4.0   5.0   4.0   5.0   0.3842      Rank 1    Sangat Baik", fill="#374151", font=get_font(8))
    draw.text((250, py + 126), "2    19880315201202     Siti Nurhaliza, M.Pd      4.0   4.0   4.0   4.0   0.3510      Rank 2    Baik", fill="#374151", font=get_font(8))
    draw.text((250, py + 146), "3    19900520201503     Budi Santoso, S.Kom       3.0   4.0   4.0   4.0   0.3245      Rank 3    Baik", fill="#374151", font=get_font(8))
    
    draw.text((w - 240, py + 230), "Mengetahui,\nKepala Sekolah SMA Al-Ihsan\n\n\n( _______________________ )", fill="#111827", font=get_font(8))

    img.save("wireframes/wf_10_laporan_cetak.png")

# 11. Kelola Pengguna
def make_wf_pengguna():
    w, h = 1000, 540
    img = Image.new("RGB", (w, h), "#FFFFFF")
    draw = ImageDraw.Draw(img)
    draw_header_nav(draw, w, role="Administrator")
    draw_sidebar(draw, h, active_menu="Pengguna")
    
    draw.text((220, 65), "Kelola Akun Pengguna Sistem", fill="#111827", font=get_font(15, bold=True))
    draw.text((220, 85), "Manajemen hak akses pengguna (Admin, Kepala Sekolah, Guru) dan reset password", fill="#6B7280", font=get_font(10))
    
    draw.rectangle([(220, 108), (w - 20, 146)], fill="#FAFAFA", outline="#333333", width=1)
    draw.text((235, 120), "Daftar Akun Pengguna Aktif", fill="#111827", font=get_font(10, bold=True))
    
    btn_u = (w - 180, 114, w - 30, 140)
    draw.rounded_rectangle(btn_u, radius=4, fill="#E5E7EB", outline="#111827", width=2)
    draw_centered_in_box(draw, btn_u, "+ Tambah User", "#111827", get_font(9, bold=True))
    
    ty = 158
    tw = w - 240
    draw.rectangle([(220, ty), (220 + tw, ty + 28)], fill="#E5E7EB", outline="#333333", width=1)
    
    cols = [
        ("No", 35, "center"),
        ("Nama Pengguna", 175, "left"),
        ("Username", 100, "left"),
        ("Role Hak Akses", 130, "center"),
        ("Terkait Guru", 150, "left"),
        ("Status", 70, "center"),
        ("Aksi", 100, "center")
    ]
    cur_x = 220
    for cname, cwidth, align in cols:
        if align == "center":
            draw_centered_in_box(draw, (cur_x, ty, cur_x + cwidth, ty + 28), cname, "#111827", get_font(9, bold=True))
        else:
            draw.text((cur_x + 6, ty + 7), cname, fill="#111827", font=get_font(9, bold=True))
        draw.line([(cur_x + cwidth, ty), (cur_x + cwidth, ty + 28)], fill="#333333", width=1)
        cur_x += cwidth
        
    u_rows = [
        ("1", "Administrator Utama", "admin", "ADMIN", "-", "Aktif", "[Reset] [Edit]"),
        ("2", "Drs. H. Mulyadi, M.Pd", "kepsek", "KEPALA_SEKOLAH", "-", "Aktif", "[Reset] [Edit]"),
        ("3", "Ahmad Fauzi, S.Pd", "guru1", "GURU", "Ahmad Fauzi, S.Pd", "Aktif", "[Reset] [Edit]"),
        ("4", "Siti Nurhaliza, M.Pd", "guru2", "GURU", "Siti Nurhaliza, M.Pd", "Aktif", "[Reset] [Edit]"),
    ]
    ry = ty + 28
    for r in u_rows:
        draw.rectangle([(220, ry), (220 + tw, ry + 32)], fill="#FFFFFF", outline="#D1D5DB", width=1)
        cur_x = 220
        for i, val in enumerate(r):
            cwidth = cols[i][1]
            align = cols[i][2]
            if align == "center":
                draw_centered_in_box(draw, (cur_x, ry, cur_x + cwidth, ry + 32), val, "#111827", get_font(9, bold=(i in (2, 3))))
            else:
                draw.text((cur_x + 6, ry + 8), val, fill="#111827", font=get_font(8))
            draw.line([(cur_x + cwidth, ry), (cur_x + cwidth, ry + 32)], fill="#E5E7EB", width=1)
            cur_x += cwidth
        ry += 32

    img.save("wireframes/wf_11_kelola_pengguna.png")

# 12. Dashboard Guru
def make_wf_guru_dashboard():
    w, h = 1000, 580
    img = Image.new("RGB", (w, h), "#FFFFFF")
    draw = ImageDraw.Draw(img)
    draw_header_nav(draw, w, role="Guru (Ahmad Fauzi, S.Pd)")
    
    draw.rectangle([(0, 52), (200, h)], fill="#F9FAFB", outline="#333333", width=1)
    g_menus = [
        ("MENU GURU", None),
        ("Dashboard & Profil", True),
        ("Hasil Penilaian", False),
        ("Riwayat Evaluasi", False),
    ]
    gy = 66
    for mtext, is_act in g_menus:
        if is_act is None:
            draw.text((15, gy), mtext, fill="#9CA3AF", font=get_font(9, bold=True))
            gy += 20
        else:
            if is_act:
                draw.rectangle([(8, gy - 3), (192, gy + 20)], fill="#E5E7EB", outline="#111827", width=1)
                draw.text((22, gy), f"• {mtext}", fill="#111827", font=get_font(10, bold=True))
            else:
                draw.text((22, gy), f"  {mtext}", fill="#4B5563", font=get_font(10))
            gy += 25
            
    draw.text((220, 65), "Dashboard Guru & Profil Mandiri", fill="#111827", font=get_font(15, bold=True))
    draw.text((220, 85), "Informasi biodata, beban jam tatap muka mengajar, dan hasil evaluasi kinerja", fill="#6B7280", font=get_font(10))
    
    # Profil Card
    draw.rounded_rectangle([(220, 108), (w - 20, 230)], radius=6, fill="#FAFAFA", outline="#333333", width=1)
    
    pbox = (235, 120, 315, 218)
    draw.rectangle(pbox, fill="#E5E7EB", outline="#9CA3AF", width=1)
    draw_centered_in_box(draw, pbox, "[ FOTO GURU ]", "#6B7280", get_font(8, bold=True))
    
    draw.text((330, 120), "Ahmad Fauzi, S.Pd", fill="#111827", font=get_font(13, bold=True))
    draw.text((330, 142), "NIP: 19850110201001  |  Jenis Kelamin: Laki-laki  |  Status: Guru Aktif", fill="#4B5563", font=get_font(9))
    draw.text((330, 160), "Mata Pelajaran: Guru Matematika  |  Tugas Tambahan: Wali Kelas X-A", fill="#4B5563", font=get_font(9))
    draw.text((330, 178), "Beban Mengajar: 24 Jam / Minggu  |  Rata-rata Siswa: 32 Siswa / Rombel", fill="#4B5563", font=get_font(9))
    draw.text((330, 196), "Kelas yang Diampu: Kelas 10 [v]  Kelas 11 [v]  Kelas 12 [ ]", fill="#374151", font=get_font(9, bold=True))
    
    # Hasil Evaluasi Card
    draw.rounded_rectangle([(220, 245), (w - 20, 420)], radius=6, fill="#FFFFFF", outline="#333333", width=1)
    draw.rectangle([(220, 245), (w - 20, 274)], fill="#E5E7EB", outline="#9CA3AF", width=1)
    draw.text((235, 253), "Hasil Evaluasi Kinerja Terkini (Periode: Juni 2026)", fill="#111827", font=get_font(10, bold=True))
    
    cw_box = (w - 240 - 30) // 4
    scores = [
        ("C1 - Pedagogik", "4.0 / 5.0", "Predikat: Baik"),
        ("C2 - Profesional", "5.0 / 5.0", "Predikat: Sangat Baik"),
        ("C3 - Kepribadian", "4.0 / 5.0", "Predikat: Baik"),
        ("C4 - Sosial", "5.0 / 5.0", "Predikat: Sangat Baik"),
    ]
    for i, (sc_name, sc_val, sc_pred) in enumerate(scores):
        sc_x1 = 235 + i * (cw_box + 10)
        sc_x2 = sc_x1 + cw_box
        draw.rounded_rectangle([(sc_x1, 288), (sc_x2, 348)], radius=4, fill="#FAFAFA", outline="#9CA3AF", width=1)
        draw.text((sc_x1 + 10, 296), sc_name, fill="#4B5563", font=get_font(9, bold=True))
        draw.text((sc_x1 + 10, 312), sc_val, fill="#111827", font=get_font(12, bold=True))
        draw.text((sc_x1 + 10, 331), sc_pred, fill="#374151", font=get_font(8))
        
    draw.text((235, 365), "Hasil Akhir MOORA: Nilai Preferensi (Yi) = 0.3842  |  Peringkat: Juara 1 (Sangat Baik)", fill="#111827", font=get_font(10, bold=True))
    draw.text((235, 386), "Catatan Evaluator: 'Pertahankan kinerja pembelajaran interaktif di kelas dan terus tingkatkan inovasi digital.'", fill="#4B5563", font=get_font(8))

    img.save("wireframes/wf_12_dashboard_guru.png")

if __name__ == "__main__":
    print("Generating updated, cleanly-aligned monochromatic wireframe images...")
    make_wf_login()
    make_wf_dashboard_admin()
    make_wf_guru()
    make_wf_kriteria()
    make_wf_skala()
    make_wf_periode()
    make_wf_penilaian()
    make_wf_moora()
    make_wf_ranking()
    make_wf_laporan()
    make_wf_pengguna()
    make_wf_guru_dashboard()
    print("Done generating updated wireframes!")
