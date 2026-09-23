import os
import sqlite3
import datetime
from PIL import Image, ImageDraw, ImageFont

os.makedirs("db_screenshots", exist_ok=True)

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

def truncate_text(text, max_len=28):
    if text is None:
        return "null"
    s = str(text)
    if len(s) > max_len:
        return s[:max_len-3] + "..."
    return s

def render_db_table_screenshot(
    table_name,
    display_title,
    columns_meta, # list of (col_name, col_type, is_pk, is_fk, fk_target)
    rows_data,
    total_count,
    output_filename
):
    # Canvas setup
    scale = 2  # 2x for super sharp retina graphics
    w, h = 1360, 680
    img = Image.new("RGB", (w * scale, h * scale), "#F8FAFC")
    draw = ImageDraw.Draw(img)
    
    def S(v):
        return int(v * scale)
    
    # 1. Window Header (Modern Desktop / Web App Header)
    draw.rectangle([(0, 0), (S(w), S(46))], fill="#0F172A")
    
    # Window traffic light buttons
    draw.ellipse([(S(18), S(17)), (S(28), S(27))], fill="#EF4444")
    draw.ellipse([(S(34), S(17)), (S(44), S(27))], fill="#F59E0B")
    draw.ellipse([(S(50), S(17)), (S(60), S(27))], fill="#10B981")
    
    # Title & Breadcrumb in top bar
    draw.text((S(78), S(14)), "Prisma Studio", fill="#38BDF8", font=get_font(13 * scale, bold=True))
    draw.text((S(175), S(14)), "•", fill="#64748B", font=get_font(13 * scale))
    draw.text((S(190), S(14)), "dev.db (SQLite)", fill="#94A3B8", font=get_font(12 * scale))
    draw.text((S(295), S(14)), f"/  {display_title}", fill="#F1F5F9", font=get_font(13 * scale, bold=True))
    
    # Right top bar badge
    draw_rounded_rect(draw, (S(w - 200), S(10), S(w - 18), S(36)), radius=S(4), fill="#1E293B", outline="#334155", width=S(1))
    draw.ellipse([(S(w - 186), S(20)), (S(w - 178), S(28))], fill="#22C55E")
    draw.text((S(w - 170), S(13)), "Connected : Port 5555", fill="#94A3B8", font=get_font(10 * scale))
    
    # 2. Sub-header & Action Toolbar
    draw.rectangle([(0, S(46)), (S(w), S(106))], fill="#FFFFFF", outline="#E2E8F0", width=S(1))
    
    # Table Icon & Name
    draw_rounded_rect(draw, (S(20), S(56), S(60), S(96)), radius=S(6), fill="#EFF6FF", outline="#BFDBFE", width=S(1))
    draw.text((S(30), S(64)), "TBL", fill="#2563EB", font=get_font(11 * scale, bold=True))
    
    draw.text((S(72), S(56)), f"Model: {table_name}", fill="#0F172A", font=get_font(15 * scale, bold=True))
    draw.text((S(72), S(80)), f"Total {total_count} records • {len(columns_meta)} fields • Engine: SQLite 3", fill="#64748B", font=get_font(10 * scale))
    
    # Action buttons on toolbar
    # Search box
    draw_rounded_rect(draw, (S(w - 530), S(62), S(w - 290), S(92)), radius=S(4), fill="#F8FAFC", outline="#CBD5E1", width=S(1))
    draw.text((S(w - 515), S(69)), f"Search in {table_name}...", fill="#94A3B8", font=get_font(11 * scale))
    
    # + Add record button
    draw_rounded_rect(draw, (S(w - 280), S(62), S(w - 170), S(92)), radius=S(4), fill="#2563EB", outline="#1D4ED8", width=S(1))
    draw.text((S(w - 265), S(68)), "+ Add Record", fill="#FFFFFF", font=get_font(11 * scale, bold=True))
    
    # Refresh button
    draw_rounded_rect(draw, (S(w - 160), S(62), S(w - 85), S(92)), radius=S(4), fill="#FFFFFF", outline="#CBD5E1", width=S(1))
    draw.text((S(w - 148), S(68)), "Refresh", fill="#334155", font=get_font(11 * scale))
    
    # Export button
    draw_rounded_rect(draw, (S(w - 75), S(62), S(w - 20), S(92)), radius=S(4), fill="#FFFFFF", outline="#CBD5E1", width=S(1))
    draw.text((S(w - 65), S(68)), "Export", fill="#334155", font=get_font(11 * scale))
    
    # 3. Main Data Grid Table
    grid_top = 118
    grid_left = 20
    grid_right = w - 20
    grid_bottom = h - 45
    
    # Grid card container
    draw_rounded_rect(draw, (S(grid_left), S(grid_top), S(grid_right), S(grid_bottom)), radius=S(6), fill="#FFFFFF", outline="#CBD5E1", width=S(1))
    
    # Calculate column widths proportionally
    num_cols = len(columns_meta)
    table_w = grid_right - grid_left
    row_num_w = 46
    avail_w = table_w - row_num_w
    
    # Heuristic column weights
    col_weights = []
    for col_name, col_type, is_pk, is_fk, fk_tgt in columns_meta:
        clow = col_name.lower()
        if is_pk:
            col_weights.append(1.8)
        elif is_fk:
            col_weights.append(1.8)
        elif "nama" in clow or "catatan" in clow or "aktivitas" in clow:
            col_weights.append(2.6)
        elif "tugas" in clow or "jabatan" in clow:
            col_weights.append(2.3)
        elif "keterangan" in clow:
            col_weights.append(2.5)
        elif "password" in clow:
            col_weights.append(2.0)
        elif "created" in clow or "updated" in clow or "waktu" in clow:
            col_weights.append(1.5)
        elif "bobot" in clow or "nilai" in clow or "rank" in clow or "nip" in clow or "kode" in clow:
            col_weights.append(1.2)
        elif col_type in ("BOOLEAN", "INTEGER", "Int"):
            col_weights.append(1.0)
        else:
            col_weights.append(1.3)
            
    tot_weight = sum(col_weights)
    col_widths = [max(60, int((wgt / tot_weight) * avail_w)) for wgt in col_weights]
    
    # Adjust last column to match exact width
    diff = avail_w - sum(col_widths)
    col_widths[-1] += diff
    
    # 3a. Header Row
    hdr_h = 40
    draw.rectangle([(S(grid_left), S(grid_top)), (S(grid_right), S(grid_top + hdr_h))], fill="#F1F5F9")
    draw.line([(S(grid_left), S(grid_top + hdr_h)), (S(grid_right), S(grid_top + hdr_h))], fill="#CBD5E1", width=S(1))
    
    # Row Number Header
    draw.text((S(grid_left + 12), S(grid_top + 12)), "#", fill="#64748B", font=get_font(11 * scale, bold=True))
    draw.line([(S(grid_left + row_num_w), S(grid_top)), (S(grid_left + row_num_w), S(grid_bottom))], fill="#CBD5E1", width=S(1))
    
    cur_x = grid_left + row_num_w
    for c_idx, (col_name, col_type, is_pk, is_fk, fk_tgt) in enumerate(columns_meta):
        cw = col_widths[c_idx]
        
        # Col Name
        draw.text((S(cur_x + 8), S(grid_top + 6)), col_name, fill="#0F172A", font=get_font(11 * scale, bold=True))
        
        # Badges & Type
        sub_y = grid_top + 23
        badge_x = cur_x + 8
        if is_pk:
            draw_rounded_rect(draw, (S(badge_x), S(sub_y), S(badge_x + 22), S(sub_y + 12)), radius=S(2), fill="#FEF3C7", outline="#F59E0B", width=S(1))
            draw.text((S(badge_x + 4), S(sub_y + 1)), "PK", fill="#B45309", font=get_font(8 * scale, bold=True))
            badge_x += 26
        if is_fk:
            draw_rounded_rect(draw, (S(badge_x), S(sub_y), S(badge_x + 22), S(sub_y + 12)), radius=S(2), fill="#EDE9FE", outline="#8B5CF6", width=S(1))
            draw.text((S(badge_x + 4), S(sub_y + 1)), "FK", fill="#6D28D9", font=get_font(8 * scale, bold=True))
            badge_x += 26
            
        draw.text((S(badge_x), S(sub_y)), col_type, fill="#64748B", font=get_font(9 * scale))
        
        # Vertical divider line
        if c_idx < num_cols - 1:
            draw.line([(S(cur_x + cw), S(grid_top)), (S(cur_x + cw), S(grid_bottom))], fill="#E2E8F0", width=S(1))
        cur_x += cw

    # 3b. Data Rows
    row_h = 32
    max_visible_rows = int((grid_bottom - 28 - (grid_top + hdr_h)) / row_h)
    display_rows = rows_data[:max_visible_rows]
    
    for r_idx, row in enumerate(display_rows):
        ry = grid_top + hdr_h + (r_idx * row_h)
        # Alternate background
        if r_idx % 2 == 1:
            draw.rectangle([(S(grid_left + 1), S(ry)), (S(grid_right - 1), S(ry + row_h))], fill="#F8FAFC")
        
        # Bottom row line
        draw.line([(S(grid_left), S(ry + row_h)), (S(grid_right), S(ry + row_h))], fill="#F1F5F9", width=S(1))
        
        # Row Number
        draw.text((S(grid_left + 12), S(ry + 8)), str(r_idx + 1), fill="#94A3B8", font=get_font(10 * scale))
        
        cur_x = grid_left + row_num_w
        for c_idx, (col_name, col_type, is_pk, is_fk, fk_tgt) in enumerate(columns_meta):
            cw = col_widths[c_idx]
            val = row[c_idx] if c_idx < len(row) else None
            
            # Format value
            if val is None or val == "":
                txt = "null"
                f_color = "#94A3B8"
            elif col_type == "BOOLEAN" or (isinstance(val, int) and col_type in ("BOOLEAN", "Boolean")):
                is_true = (str(val) in ("1", "True", "true"))
                txt = "true" if is_true else "false"
                f_color = "#16A34A" if is_true else "#DC2626"
            elif "password" in col_name.lower():
                txt = "$2a$10$eK7... [hash]"
                f_color = "#64748B"
            elif isinstance(val, (int, float)) and ("waktu" in col_name.lower() or "created" in col_name.lower() or "updated" in col_name.lower()):
                # Milliseconds timestamp
                if val > 1000000000000:
                    dt = datetime.datetime.fromtimestamp(val / 1000.0)
                    txt = dt.strftime("%Y-%m-%d %H:%M")
                else:
                    txt = str(val)
                f_color = "#334155"
            else:
                txt = str(val)
                f_color = "#1E293B"
                
            # Limit characters
            max_c_len = max(6, int(cw / 7.5))
            draw_txt = truncate_text(txt, max_c_len)
            
            draw.text((S(cur_x + 8), S(ry + 8)), draw_txt, fill=f_color, font=get_font(10 * scale))
            cur_x += cw
            
    # 4. Table Pagination Footer
    draw.rectangle([(S(grid_left), S(grid_bottom - 28)), (S(grid_right), S(grid_bottom))], fill="#F8FAFC", outline="#E2E8F0", width=S(1))
    draw.text((S(grid_left + 15), S(grid_bottom - 21)), f"Showing 1 to {len(display_rows)} of {total_count} records", fill="#64748B", font=get_font(10 * scale))
    draw.text((S(grid_right - 220), S(grid_bottom - 21)), f"Page 1 of 1 • Limit 50 rows", fill="#64748B", font=get_font(10 * scale))
    
    # Bottom Status bar
    draw.rectangle([(0, S(h - 30)), (S(w), S(h))], fill="#0F172A")
    draw.text((S(20), S(h - 22)), "SQLite Database: c:\\Penilaian_Kinerja_Guru\\prisma\\dev.db", fill="#94A3B8", font=get_font(10 * scale))
    draw.text((S(w - 250), S(h - 22)), "SPK Penilaian Kinerja Guru (MOORA)", fill="#38BDF8", font=get_font(10 * scale, bold=True))
    
    # Save image
    out_path = os.path.join("db_screenshots", output_filename)
    img.save(out_path, quality=95)
    print(f"Generated: {out_path} ({img.size[0]}x{img.size[1]})")
    return out_path

def generate_all_11_tables():
    conn = sqlite3.connect('prisma/dev.db')
    cursor = conn.cursor()
    
    tables_config = [
        {
            "db_table": "Role",
            "model_name": "Role (tbl_role)",
            "title": "Role",
            "file": "img_db_01_role.png",
            "columns": [
                ("id", "String", True, False, None),
                ("namaRole", "String", False, False, None),
            ]
        },
        {
            "db_table": "User",
            "model_name": "User (tbl_user)",
            "title": "User",
            "file": "img_db_02_user.png",
            "columns": [
                ("id", "String", True, False, None),
                ("nama", "String", False, False, None),
                ("username", "String", False, False, None),
                ("password", "String", False, False, None),
                ("roleId", "String", False, True, "Role"),
                ("guruId", "String", False, True, "Guru"),
                ("status", "BOOLEAN", False, False, None),
                ("createdAt", "DateTime", False, False, None),
                ("updatedAt", "DateTime", False, False, None),
            ]
        },
        {
            "db_table": "Guru",
            "model_name": "Guru (tbl_guru)",
            "title": "Guru",
            "file": "img_db_03_guru.png",
            "columns": [
                ("id", "String", True, False, None),
                ("nip", "String", False, False, None),
                ("nama", "String", False, False, None),
                ("jenisKelamin", "String", False, False, None),
                ("jabatanTugasMengajar", "String", False, False, None),
                ("tugasTambahanUtama", "String", False, False, None),
                ("tugasTambahanLain", "String", False, False, None),
                ("jumlahSiswaPerRombel", "Int", False, False, None),
                ("jumlahJamAjar", "Int", False, False, None),
                ("mengajarKelas10", "BOOLEAN", False, False, None),
                ("mengajarKelas11", "BOOLEAN", False, False, None),
                ("mengajarKelas12", "BOOLEAN", False, False, None),
                ("statusAktif", "BOOLEAN", False, False, None),
            ]
        },
        {
            "db_table": "Kriteria",
            "model_name": "Kriteria (tbl_kriteria)",
            "title": "Kriteria",
            "file": "img_db_04_kriteria.png",
            "columns": [
                ("id", "String", True, False, None),
                ("kode", "String", False, False, None),
                ("nama", "String", False, False, None),
                ("bobot", "Float", False, False, None),
                ("jenis", "String", False, False, None),
                ("status", "BOOLEAN", False, False, None),
                ("createdAt", "DateTime", False, False, None),
                ("updatedAt", "DateTime", False, False, None),
            ]
        },
        {
            "db_table": "SkalaPenilaian",
            "model_name": "SkalaPenilaian (tbl_skala_penilaian)",
            "title": "SkalaPenilaian",
            "file": "img_db_05_skala_penilaian.png",
            "columns": [
                ("id", "String", True, False, None),
                ("kriteriaId", "String", False, True, "Kriteria"),
                ("nilai", "Int", False, False, None),
                ("label", "String", False, False, None),
                ("keterangan", "String", False, False, None),
            ]
        },
        {
            "db_table": "PeriodePenilaian",
            "model_name": "PeriodePenilaian (tbl_periode_penilaian)",
            "title": "PeriodePenilaian",
            "file": "img_db_06_periode_penilaian.png",
            "columns": [
                ("id", "String", True, False, None),
                ("bulan", "String", False, False, None),
                ("tahun", "Int", False, False, None),
                ("namaPeriode", "String", False, False, None),
                ("status", "String", False, False, None),
                ("createdAt", "DateTime", False, False, None),
                ("updatedAt", "DateTime", False, False, None),
            ]
        },
        {
            "db_table": "Penilaian",
            "model_name": "Penilaian (tbl_penilaian)",
            "title": "Penilaian",
            "file": "img_db_07_penilaian.png",
            "columns": [
                ("id", "String", True, False, None),
                ("guruId", "String", False, True, "Guru"),
                ("periodeId", "String", False, True, "PeriodePenilaian"),
                ("dinilaiOleh", "String", False, False, None),
                ("status", "String", False, False, None),
                ("catatan", "String", False, False, None),
                ("createdAt", "DateTime", False, False, None),
                ("updatedAt", "DateTime", False, False, None),
            ]
        },
        {
            "db_table": "DetailPenilaian",
            "model_name": "DetailPenilaian (tbl_detail_penilaian)",
            "title": "DetailPenilaian",
            "file": "img_db_08_detail_penilaian.png",
            "columns": [
                ("id", "String", True, False, None),
                ("penilaianId", "String", False, True, "Penilaian"),
                ("kriteriaId", "String", False, True, "Kriteria"),
                ("nilai", "Float", False, False, None),
            ]
        },
        {
            "db_table": "HasilMoora",
            "model_name": "HasilMoora (tbl_hasil_moora)",
            "title": "HasilMoora",
            "file": "img_db_09_hasil_moora.png",
            "columns": [
                ("id", "String", True, False, None),
                ("guruId", "String", False, True, "Guru"),
                ("periodeId", "String", False, True, "PeriodePenilaian"),
                ("nilaiPreferensi", "Float", False, False, None),
                ("ranking", "Int", False, False, None),
                ("createdAt", "DateTime", False, False, None),
            ]
        },
        {
            "db_table": "DetailMoora",
            "model_name": "DetailMoora (tbl_detail_moora)",
            "title": "DetailMoora",
            "file": "img_db_10_detail_moora.png",
            "columns": [
                ("id", "String", True, False, None),
                ("hasilMooraId", "String", False, True, "HasilMoora"),
                ("kriteriaId", "String", False, True, "Kriteria"),
                ("nilaiAwal", "Float", False, False, None),
                ("nilaiNormalisasi", "Float", False, False, None),
                ("bobot", "Float", False, False, None),
                ("nilaiTerbobot", "Float", False, False, None),
            ]
        },
        {
            "db_table": "LogAktivitas",
            "model_name": "LogAktivitas (tbl_log_aktivitas)",
            "title": "LogAktivitas",
            "file": "img_db_11_log_aktivitas.png",
            "columns": [
                ("id", "String", True, False, None),
                ("userId", "String", False, True, "User"),
                ("aktivitas", "String", False, False, None),
                ("modul", "String", False, False, None),
                ("dataId", "String", False, False, None),
                ("waktu", "DateTime", False, False, None),
                ("alamatIp", "String", False, False, None),
            ]
        }
    ]
    
    for cfg in tables_config:
        tbl_name = cfg["db_table"]
        cols = [c[0] for c in cfg["columns"]]
        cols_sql = ", ".join([f'"{c}"' for c in cols])
        cursor.execute(f'SELECT count(*) FROM "{tbl_name}"')
        total_cnt = cursor.fetchone()[0]
        
        cursor.execute(f'SELECT {cols_sql} FROM "{tbl_name}" LIMIT 15')
        rows = cursor.fetchall()
        
        render_db_table_screenshot(
            table_name=cfg["model_name"],
            display_title=cfg["title"],
            columns_meta=cfg["columns"],
            rows_data=rows,
            total_count=total_cnt,
            output_filename=cfg["file"]
        )
    
    conn.close()
    print("All 11 database screenshots generated successfully!")

if __name__ == "__main__":
    generate_all_11_tables()
