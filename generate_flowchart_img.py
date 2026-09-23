import os
import docx
from PIL import Image, ImageDraw, ImageFont
from docx.shared import Inches, Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

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
    lines = text.split('\n')
    line_height = font.size + 4 if hasattr(font, 'size') else 14
    total_h = len(lines) * line_height
    start_y = cy - total_h / 2
    
    for idx, line in enumerate(lines):
        bbox = draw.textbbox((0, 0), line, font=font)
        w = bbox[2] - bbox[0]
        draw.text((cx - w / 2, start_y + idx * line_height), line, fill=fill, font=font)

def draw_arrow(draw, x1, y1, x2, y2, color="#111827", width=2, arrow_size=6):
    draw.line([(x1, y1), (x2, y2)], fill=color, width=width)
    if y2 > y1: # Downward
        draw.polygon([(x2, y2), (x2 - arrow_size, y2 - arrow_size * 1.5), (x2 + arrow_size, y2 - arrow_size * 1.5)], fill=color)
    elif x2 > x1: # Rightward
        draw.polygon([(x2, y2), (x2 - arrow_size * 1.5, y2 - arrow_size), (x2 - arrow_size * 1.5, y2 + arrow_size)], fill=color)
    elif x2 < x1: # Leftward
        draw.polygon([(x2, y2), (x2 + arrow_size * 1.5, y2 - arrow_size), (x2 + arrow_size * 1.5, y2 + arrow_size)], fill=color)
    elif y2 < y1: # Upward
        draw.polygon([(x2, y2), (x2 - arrow_size, y2 + arrow_size * 1.5), (x2 + arrow_size, y2 + arrow_size * 1.5)], fill=color)

def draw_diamond(draw, cx, cy, w, h, fill="#FFFFFF", outline="#111827", width=2):
    pts = [(cx, cy - h/2), (cx + w/2, cy), (cx, cy + h/2), (cx - w/2, cy)]
    draw.polygon(pts, fill=fill, outline=outline)
    if width > 1:
        draw.line(pts + [pts[0]], fill=outline, width=width)

def draw_parallelogram(draw, cx, cy, w, h, skew=20, fill="#FFFFFF", outline="#111827", width=2):
    x1, y1 = cx - w/2, cy - h/2
    x2, y2 = cx + w/2, cy + h/2
    pts = [(x1 + skew, y1), (x2, y1), (x2 - skew, y2), (x1, y2)]
    draw.polygon(pts, fill=fill, outline=outline)
    if width > 1:
        draw.line(pts + [pts[0]], fill=outline, width=width)

def make_flowchart_image():
    w, h = 900, 1180
    img = Image.new("RGB", (w, h), "#FFFFFF")
    draw = ImageDraw.Draw(img)
    
    # Outer frame
    draw.rectangle([(0, 0), (w-1, h-1)], outline="#D1D5DB", width=1)
    
    f_title = get_font(13, bold=True)
    f_sub = get_font(10, bold=False)
    f_node = get_font(10, bold=True)
    f_text = get_font(9, bold=False)
    f_label = get_font(9, bold=True)
    
    # Diagram Header
    draw_centered_text(draw, w//2, 18, "FLOWCHART ALGORITMA METODE MOORA", "#111827", f_title)
    draw_centered_text(draw, w//2, 38, "Sistem Pendukung Keputusan Penilaian Kinerja Guru SMA Al-Ihsan", "#6B7280", f_sub)
    draw.line([(60, 56), (w - 60, 56)], fill="#E5E7EB", width=2)
    
    cx = w // 2
    
    # 1. Start Terminator
    y = 75
    draw.rounded_rectangle([(cx - 75, y), (cx + 75, y + 36)], radius=18, fill="#F3F4F6", outline="#111827", width=2)
    draw_centered_in_box(draw, (cx - 75, y, cx + 75, y + 36), "MULAI (START)", "#111827", f_node)
    
    draw_arrow(draw, cx, y + 36, cx, y + 68)
    
    # 2. Input Data
    y += 68
    draw_parallelogram(draw, cx, y + 22, 380, 44, skew=20, fill="#FAFAFA", outline="#111827", width=2)
    draw_centered_in_box(draw, (cx - 190, y, cx + 190, y + 44), "Input Data: Guru (m), Kriteria (n),\nBobot (W), Skor Penilaian Periode", "#111827", f_node)
    
    draw_arrow(draw, cx, y + 44, cx, y + 76)
    
    # 3. Decision Validasi Kelengkapan
    y += 76
    draw_diamond(draw, cx, y + 28, 300, 56, fill="#FFFFFF", outline="#111827", width=2)
    draw_centered_in_box(draw, (cx - 150, y, cx + 150, y + 56), "Validasi Data Lengkap?\n(Seluruh Guru Dinilai)", "#111827", f_node)
    
    # Branch "Tidak Lengkap" -> Exit error
    draw_arrow(draw, cx + 150, y + 28, cx + 270, y + 28)
    draw.text((cx + 160, y + 14), "TIDAK", fill="#DC2626", font=f_label)
    
    draw.rectangle([(cx + 270, y + 8), (cx + 410, y + 48)], fill="#FEE2E2", outline="#DC2626", width=2)
    draw_centered_in_box(draw, (cx + 270, y + 8, cx + 410, y + 48), "Tampilkan Pesan:\nData Nilai Belum Lengkap", "#991B1B", f_label)
    
    draw_arrow(draw, cx + 340, y + 48, cx + 340, y + 90)
    draw.rounded_rectangle([(cx + 270, y + 90), (cx + 410, y + 124)], radius=17, fill="#F3F4F6", outline="#111827", width=2)
    draw_centered_in_box(draw, (cx + 270, y + 90, cx + 410, y + 124), "SELESAI (BATAL)", "#111827", f_node)
    
    # Branch "YA" -> Proceed
    draw_arrow(draw, cx, y + 56, cx, y + 88)
    draw.text((cx + 8, y + 62), "YA", fill="#16A34A", font=f_label)
    
    # 4. Tahap 1: Matriks Keputusan X
    y += 88
    draw.rectangle([(cx - 190, y), (cx + 190, y + 48)], fill="#FFFFFF", outline="#111827", width=2)
    draw_centered_in_box(draw, (cx - 190, y, cx + 190, y + 48), "1. Bentuk Matriks Keputusan (X)\nX = [x_ij] berukuran m × n", "#111827", f_node)
    
    draw_arrow(draw, cx, y + 48, cx, y + 80)
    
    # 5. Tahap 2: Hitung Pembagi Euclidean
    y += 80
    draw.rectangle([(cx - 210, y), (cx + 210, y + 54)], fill="#FFFFFF", outline="#111827", width=2)
    draw_centered_in_box(draw, (cx - 210, y, cx + 210, y + 54), "2. Hitung Pembagi Euclidean Setiap Kriteria\n|X_j| = √( ∑_{i=1}^m (x_ij)² )", "#111827", f_node)
    
    draw_arrow(draw, cx, y + 54, cx, y + 86)
    
    # 6. Tahap 3: Normalisasi Rasio Vektor X*
    y += 86
    draw.rectangle([(cx - 210, y), (cx + 210, y + 54)], fill="#FFFFFF", outline="#111827", width=2)
    draw_centered_in_box(draw, (cx - 210, y, cx + 210, y + 54), "3. Hitung Matriks Ternormalisasi (X*)\nx*_ij = x_ij / |X_j|", "#111827", f_node)
    
    draw_arrow(draw, cx, y + 54, cx, y + 86)
    
    # 7. Tahap 4: Pembobotan Matriks (v_ij)
    y += 86
    draw.rectangle([(cx - 210, y), (cx + 210, y + 54)], fill="#FFFFFF", outline="#111827", width=2)
    draw_centered_in_box(draw, (cx - 210, y, cx + 210, y + 54), "4. Pembobotan Matriks Normalisasi (V)\nv_ij = w_j × x*_ij", "#111827", f_node)
    
    draw_arrow(draw, cx, y + 54, cx, y + 86)
    
    # 8. Tahap 5: Hitung Nilai Preferensi Yi
    y += 86
    draw.rectangle([(cx - 225, y), (cx + 225, y + 56)], fill="#FFFFFF", outline="#111827", width=2)
    draw_centered_in_box(draw, (cx - 225, y, cx + 225, y + 56), "5. Hitung Nilai Preferensi Multiobjektif (Yi)\nYi = ∑ (Benefit) - ∑ (Cost)", "#111827", f_node)
    
    draw_arrow(draw, cx, y + 56, cx, y + 88)
    
    # 9. Tahap 6: Perankingan Alternatif
    y += 88
    draw.rectangle([(cx - 210, y), (cx + 210, y + 50)], fill="#FFFFFF", outline="#111827", width=2)
    draw_centered_in_box(draw, (cx - 210, y, cx + 210, y + 50), "6. Urutkan Alternatif Guru (Ranking)\nSort Descending berdasarkan Nilai Yi", "#111827", f_node)
    
    draw_arrow(draw, cx, y + 50, cx, y + 82)
    
    # 10. Simpan & Tampilkan Hasil
    y += 82
    draw_parallelogram(draw, cx, y + 24, 400, 48, skew=20, fill="#FAFAFA", outline="#111827", width=2)
    draw_centered_in_box(draw, (cx - 200, y, cx + 200, y + 48), "Output: Simpan HasilMoora ke Database\n& Tampilkan Leaderboard Ranking", "#111827", f_node)
    
    draw_arrow(draw, cx, y + 48, cx, y + 80)
    
    # 11. End Terminator
    y += 80
    draw.rounded_rectangle([(cx - 75, y), (cx + 75, y + 36)], radius=18, fill="#F3F4F6", outline="#111827", width=2)
    draw_centered_in_box(draw, (cx - 75, y, cx + 75, y + 36), "SELESAI (END)", "#111827", f_node)
    
    img.save("wireframes/flowchart_moora.png")
    print("flowchart_moora.png created successfully!")

if __name__ == "__main__":
    make_flowchart_image()
