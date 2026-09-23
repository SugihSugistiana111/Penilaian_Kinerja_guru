import os
import sqlite3
import math
import docx
from docx.shared import Inches, Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_margins(cell, top=100, bottom=100, left=140, right=140):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_cell_background(cell, color_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>')
    tcPr.append(shd)

def set_table_borders(table, color="B0B0B0", sz="4", val="single"):
    tblPr = table._tbl.tblPr
    borders = parse_xml(f'''
        <w:tblBorders {nsdecls("w")}>
            <w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
            <w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
            <w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
            <w:insideV w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
            <w:left w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
            <w:right w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
        </w:tblBorders>
    ''')
    tblPr.append(borders)

def add_table_caption(paragraph, num_suffix, title_text):
    """
    Menambahkan caption Word otomatis dengan SEQ field Tabel untuk Daftar Tabel
    """
    paragraph.alignment = WD_ALIGN_PARAGRAPH.LEFT
    paragraph.paragraph_format.space_before = Pt(10)
    paragraph.paragraph_format.space_after = Pt(4)
    paragraph.paragraph_format.keep_with_next = True
    
    r1 = paragraph.add_run("Tabel 4.")
    r1.font.name = 'Times New Roman'
    r1.font.size = Pt(11)
    r1.font.bold = True
    
    fld_xml = r'''
        <w:fldSimple %s w:instr="SEQ Tabel \* ARABIC">
            <w:r>
                <w:rPr>
                    <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/>
                    <w:b/>
                    <w:sz w:val="22"/>
                </w:rPr>
                <w:t>%s</w:t>
            </w:r>
        </w:fldSimple>
    ''' % (nsdecls("w"), num_suffix)
    paragraph._p.append(parse_xml(fld_xml))
    
    r2 = paragraph.add_run(f" {title_text}")
    r2.font.name = 'Times New Roman'
    r2.font.size = Pt(11)
    r2.font.bold = True

def add_omml_equation(doc, omml_str):
    """
    Menyisipkan rumus matematika OMML Word Equation yang rapi dan terpusat di dalam paragraf Word
    """
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(6)
    
    wrapper = f'''
    <m:oMathPara {nsdecls("m")}>
        <m:oMath>
            {omml_str}
        </m:oMath>
    </m:oMathPara>
    '''
    elem = parse_xml(wrapper)
    p._p.append(elem)

def get_moora_data():
    conn = sqlite3.connect('prisma/dev.db')
    c = conn.cursor()

    # Kriteria
    c.execute('SELECT id, kode, nama, bobot, jenis FROM Kriteria ORDER BY kode')
    kriteria = c.fetchall()

    # Guru aktif
    c.execute('SELECT id, nip, nama, jabatanTugasMengajar FROM Guru WHERE statusAktif = 1 ORDER BY nip')
    gurus = c.fetchall()

    # Periode aktif
    c.execute("SELECT id, namaPeriode FROM PeriodePenilaian WHERE status = 'AKTIF' LIMIT 1")
    per_row = c.fetchone()
    if not per_row:
        c.execute("SELECT id, namaPeriode FROM PeriodePenilaian ORDER BY createdAt DESC LIMIT 1")
        per_row = c.fetchone()
    
    pid, pnama = per_row[0], per_row[1]

    # Scores
    scores = {}
    for g in gurus:
        scores[g[0]] = {}

    c.execute('''
    SELECT p.guruId, dp.kriteriaId, dp.nilai 
    FROM Penilaian p
    JOIN DetailPenilaian dp ON p.id = dp.penilaianId
    WHERE p.periodeId = ?
    ''', (pid,))

    for gid, kid, val in c.fetchall():
        scores[gid][kid] = val

    conn.close()

    # Hitung pembagi
    divisors = {}
    sum_sqs = {}
    for k in kriteria:
        kid = k[0]
        sum_sq = sum(scores[g[0]].get(kid, 0)**2 for g in gurus)
        div = math.sqrt(sum_sq) if sum_sq > 0 else 1
        divisors[kid] = div
        sum_sqs[kid] = sum_sq

    # Matriks Ternormalisasi & Terbobot
    norm_matrix = {}
    weight_matrix = {}
    yi_list = []

    for idx, g in enumerate(gurus):
        gid = g[0]
        norm_matrix[gid] = {}
        weight_matrix[gid] = {}
        sum_benefit = 0.0
        sum_cost = 0.0

        for k in kriteria:
            kid = k[0]
            raw = scores[gid].get(kid, 0)
            norm = raw / divisors[kid]
            weighted = norm * k[3] # bobot

            norm_matrix[gid][kid] = norm
            weight_matrix[gid][kid] = weighted

            if k[4].upper() == 'BENEFIT':
                sum_benefit += weighted
            else:
                sum_cost += weighted

        yi = sum_benefit - sum_cost
        yi_list.append({
            'index': idx + 1,
            'id': gid,
            'nip': g[1],
            'nama': g[2],
            'jabatan': g[3],
            'kode_alt': f"A{idx+1}",
            'scores': scores[gid],
            'norm': norm_matrix[gid],
            'weighted': weight_matrix[gid],
            'sum_benefit': sum_benefit,
            'sum_cost': sum_cost,
            'yi': yi
        })

    # Ranking
    yi_sorted = sorted(yi_list, key=lambda x: x['yi'], reverse=True)
    for rank_idx, item in enumerate(yi_sorted):
        item['ranking'] = rank_idx + 1

    return {
        'periode_nama': pnama,
        'kriteria': kriteria,
        'gurus': gurus,
        'scores': scores,
        'sum_sqs': sum_sqs,
        'divisors': divisors,
        'data_guru': yi_list,
        'data_ranked': yi_sorted
    }

def create_moora_document():
    data = get_moora_data()
    doc = docx.Document()

    # Page setup - A4, Margin Skripsi (Top 3cm, Left 4cm, Bottom 3cm, Right 3cm)
    for section in doc.sections:
        section.page_width = Cm(21.0)
        section.page_height = Cm(29.7)
        section.top_margin = Cm(3.0)
        section.bottom_margin = Cm(3.0)
        section.left_margin = Cm(4.0)
        section.right_margin = Cm(3.0)

    # Styles
    style_normal = doc.styles['Normal']
    style_normal.font.name = 'Times New Roman'
    style_normal.font.size = Pt(12)
    style_normal.paragraph_format.line_spacing = 1.5
    style_normal.paragraph_format.space_after = Pt(6)

    # Judul Bab
    h1 = doc.add_paragraph()
    h1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_h1 = h1.add_run("BAB IV\nHASIL DAN PEMBAHASAN\n4.5 PERANCANGAN DAN PENERAPAN PROSES PERHITUNGAN METODE MOORA")
    r_h1.font.name = 'Times New Roman'
    r_h1.font.size = Pt(14)
    r_h1.font.bold = True
    h1.paragraph_format.space_after = Pt(18)

    # 4.5.1 Konsep Dasar & 5 Tahapan Algoritma MOORA
    p1 = doc.add_paragraph()
    p1.paragraph_format.line_spacing = 1.5
    p1.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    r_sec1 = p1.add_run("4.5.1 Konsep Dasar dan Tahapan Metode MOORA\n")
    r_sec1.font.bold = True
    r_sec1.font.size = Pt(12)
    p1.add_run(
        "Metode Multi-Objective Optimization on the basis of Ratio Analysis (MOORA) adalah sistem pendukung keputusan "
        "yang diperkenalkan oleh Brauers dan Zavadskas (2006) untuk menyelesaikan masalah optimasi multiobjektif secara simultan. "
        "Pada Sistem Pendukung Keputusan Penilaian Kinerja Guru di SMA Al-Ihsan Boarding School, metode MOORA dipilih karena memiliki "
        "tingkat fleksibilitas tinggi, proses komputasi yang terstruktur dan objektif, serta memisahkan secara tegas antara atribut bernilai "
        "keuntungan (Benefit) dan atribut bernilai biaya (Cost).\n\n"
        "Proses perhitungan MOORA dalam menentukan ranking kinerja guru dilakukan melalui 5 (lima) tahapan matematis sebagai berikut:"
    )

    tahapan = [
        ("1. Pembentukan Matriks Keputusan (X):", "Menyusun matriks nilai evaluasi kinerja berukuran m x n, di mana m menyatakan jumlah guru (alternatif) dan n menyatakan jumlah kriteria evaluasi."),
        ("2. Normalisasi Matriks Keputusan (X*):", "Melakukan normalisasi vektor Euclidean untuk menyatukan skala seluruh elemen matriks ke dalam nilai tanpa satuan (unitless)."),
        ("3. Pembobotan Matriks Ternormalisasi (v):", "Mengalikan seluruh elemen matriks yang telah dinormalisasi dengan bobot preferensi (W) masing-masing kriteria."),
        ("4. Perhitungan Nilai Preferensi Multiobjektif (Yi):", "Menghitung nilai optimasi dengan mengurangkan jumlah nilai kriteria bertipe Benefit dengan jumlah nilai kriteria bertipe Cost."),
        ("5. Perankingan Alternatif Guru:", "Mengurutkan guru berdasarkan nilai preferensi Yi secara menurun (descending) dari nilai tertinggi sebagai alternatif terbaik.")
    ]
    for t_title, t_desc in tahapan:
        p_t = doc.add_paragraph()
        p_t.paragraph_format.line_spacing = 1.5
        p_t.paragraph_format.space_before = Pt(2)
        p_t.paragraph_format.space_after = Pt(2)
        r_tt = p_t.add_run(f"{t_title} ")
        r_tt.font.bold = True
        p_t.add_run(t_desc)

    # 4.5.2 Kriteria dan Bobot Preferensi
    p2 = doc.add_paragraph()
    p2.paragraph_format.line_spacing = 1.5
    p2.paragraph_format.space_before = Pt(12)
    p2.paragraph_format.space_after = Pt(4)
    p2.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    r_sec2 = p2.add_run("4.5.2 Kriteria Penilaian dan Bobot Preferensi\n")
    r_sec2.font.bold = True
    r_sec2.font.size = Pt(12)
    p2.add_run(
        "Kriteria yang digunakan dalam evaluasi kinerja guru di SMA Al-Ihsan Boarding School berjumlah 4 (empat) kriteria utama "
        "yang seluruhnya bertipe BENEFIT (semakin tinggi nilai maka semakin baik performa kinerja guru). "
        "Total nilai bobot preferensi seluruh kriteria harus bernilai 1.00 (100%), yang dirumuskan sebagai:"
    )

    # Equation Total Bobot = 1
    add_omml_equation(doc, r'''
        <m:nary>
            <m:naryPr>
                <m:chr m:val="∑"/>
                <m:limLoc m:val="undOvr"/>
            </m:naryPr>
            <m:sub><m:r><m:t>j=1</m:t></m:r></m:sub>
            <m:sup><m:r><m:t>n</m:t></m:r></m:sup>
            <m:e>
                <m:sSub>
                    <m:e><m:r><m:t>w</m:t></m:r></m:e>
                    <m:sub><m:r><m:t>j</m:t></m:r></m:sub>
                </m:sSub>
            </m:e>
        </m:nary>
        <m:r><m:t> = </m:t></m:r>
        <m:r><m:t>1.00</m:t></m:r>
        <m:r><m:t> (100%)</m:t></m:r>
    ''')

    p2_desc = doc.add_paragraph()
    p2_desc.paragraph_format.line_spacing = 1.5
    p2_desc.add_run("Rincian kriteria, kode, nilai bobot preferensi, dan sifat atribut MOORA disajikan pada tabel di bawah ini:")

    # Tabel 4.12 Kriteria & Bobot
    p_cap1 = doc.add_paragraph(style='Caption')
    add_table_caption(p_cap1, "12", "Daftar Kriteria, Bobot Preferensi, dan Sifat Atribut MOORA")

    tbl_k = doc.add_table(rows=len(data['kriteria']) + 1, cols=5)
    tbl_k.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_k.autofit = False
    set_table_borders(tbl_k)

    header_tr_k = tbl_k.rows[0]._tr.get_or_add_trPr()
    header_tr_k.append(parse_xml(f'<w:tblHeader {nsdecls("w")}/>'))
    header_tr_k.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))

    k_headers = ["No", "Kode", "Nama Kriteria Penilaian", "Bobot (W)", "Sifat / Atribut"]
    k_widths = [Cm(1.0), Cm(1.8), Cm(7.0), Cm(2.8), Cm(3.2)]
    for ci, h_txt in enumerate(k_headers):
        cell = tbl_k.cell(0, ci)
        cell.width = k_widths[ci]
        set_cell_background(cell, "EAECEF")
        set_cell_margins(cell)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h_txt)
        r.font.bold = True
        r.font.size = Pt(10)

    for ri, kr in enumerate(data['kriteria']):
        row = tbl_k.rows[ri + 1]
        trPr = row._tr.get_or_add_trPr()
        trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))

        vals = [str(ri + 1), kr[1], kr[2], f"{kr[3]:.2f} ({int(kr[3]*100)}%)", kr[4]]
        for ci, val in enumerate(vals):
            cell = row.cells[ci]
            cell.width = k_widths[ci]
            set_cell_background(cell, "FAFAFA" if ri % 2 == 1 else "FFFFFF")
            set_cell_margins(cell)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if ci in (0, 1, 3, 4) else WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(val)
            r.font.size = Pt(9.5)
            if ci == 1:
                r.font.bold = True

    # 4.5.3 Data Alternatif Guru
    p3 = doc.add_paragraph()
    p3.paragraph_format.line_spacing = 1.5
    p3.paragraph_format.space_before = Pt(14)
    p3.paragraph_format.space_after = Pt(4)
    p3.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    r_sec3 = p3.add_run("4.5.3 Data Alternatif Guru yang Dievaluasi\n")
    r_sec3.font.bold = True
    r_sec3.font.size = Pt(12)
    p3.add_run(
        f"Data alternatif yang dievaluasi pada periode aktif ({data['periode_nama']}) berjumlah {len(data['gurus'])} orang guru aktif "
        "yang disimbolkan dengan notasi A1 sampai A18 sebagai berikut:"
    )

    # Tabel 4.13 Alternatif Guru
    p_cap2 = doc.add_paragraph(style='Caption')
    add_table_caption(p_cap2, "13", "Daftar Alternatif Guru SMA Al-Ihsan Boarding School")

    tbl_g = doc.add_table(rows=len(data['data_guru']) + 1, cols=5)
    tbl_g.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_g.autofit = False
    set_table_borders(tbl_g)

    header_tr_g = tbl_g.rows[0]._tr.get_or_add_trPr()
    header_tr_g.append(parse_xml(f'<w:tblHeader {nsdecls("w")}/>'))
    header_tr_g.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))

    g_headers = ["No", "Kode Alternatif", "NIP", "Nama Lengkap Guru", "Tugas Mengajar"]
    g_widths = [Cm(0.9), Cm(2.8), Cm(3.6), Cm(5.2), Cm(3.8)]

    for ci, h_txt in enumerate(g_headers):
        cell = tbl_g.cell(0, ci)
        cell.width = g_widths[ci]
        set_cell_background(cell, "EAECEF")
        set_cell_margins(cell)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h_txt)
        r.font.bold = True
        r.font.size = Pt(10)

    for ri, item in enumerate(data['data_guru']):
        row = tbl_g.rows[ri + 1]
        trPr = row._tr.get_or_add_trPr()
        trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))

        vals = [str(ri + 1), item['kode_alt'], item['nip'], item['nama'], item['jabatan']]
        for ci, val in enumerate(vals):
            cell = row.cells[ci]
            cell.width = g_widths[ci]
            set_cell_background(cell, "FAFAFA" if ri % 2 == 1 else "FFFFFF")
            set_cell_margins(cell)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if ci in (0, 1, 2) else WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(val)
            r.font.size = Pt(9)
            if ci == 1:
                r.font.bold = True

    # 4.5.4 Langkah 1: Matriks Keputusan (X)
    p4 = doc.add_paragraph()
    p4.paragraph_format.line_spacing = 1.5
    p4.paragraph_format.space_before = Pt(14)
    p4.paragraph_format.space_after = Pt(4)
    p4.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    r_sec4 = p4.add_run("4.5.4 Langkah 1: Pembentukan Matriks Keputusan (X)\n")
    r_sec4.font.bold = True
    r_sec4.font.size = Pt(12)
    p4.add_run(
        "Matriks keputusan X dibentuk berdasarkan penilaian skor evaluasi seluruh guru alternatif "
        "terhadap kriteria C1 (Kehadiran), C2 (Ketepatan Waktu), C3 (Kelengkapan Perangkat Pembelajaran), dan C4 (Kelengkapan Administrasi Penilaian). "
        "Secara matematis, matriks keputusan direpresentasikan dalam bentuk:"
    )

    # OMML Equation: Matrix X
    add_omml_equation(doc, r'''
        <m:r><m:t>X = </m:t></m:r>
        <m:d>
            <m:dPr>
                <m:begChr m:val="["/>
                <m:endChr m:val="]"/>
            </m:dPr>
            <m:e>
                <m:m>
                    <m:mr>
                        <m:e><m:sSub><m:e><m:r><m:t>x</m:t></m:r></m:e><m:sub><m:r><m:t>11</m:t></m:r></m:sub></m:sSub></m:e>
                        <m:e><m:sSub><m:e><m:r><m:t>x</m:t></m:r></m:e><m:sub><m:r><m:t>12</m:t></m:r></m:sub></m:sSub></m:e>
                        <m:e><m:r><m:t>⋯</m:t></m:r></m:e>
                        <m:e><m:sSub><m:e><m:r><m:t>x</m:t></m:r></m:e><m:sub><m:r><m:t>1n</m:t></m:r></m:sub></m:sSub></m:e>
                    </m:mr>
                    <m:mr>
                        <m:e><m:sSub><m:e><m:r><m:t>x</m:t></m:r></m:e><m:sub><m:r><m:t>21</m:t></m:r></m:sub></m:sSub></m:e>
                        <m:e><m:sSub><m:e><m:r><m:t>x</m:t></m:r></m:e><m:sub><m:r><m:t>22</m:t></m:r></m:sub></m:sSub></m:e>
                        <m:e><m:r><m:t>⋯</m:t></m:r></m:e>
                        <m:e><m:sSub><m:e><m:r><m:t>x</m:t></m:r></m:e><m:sub><m:r><m:t>2n</m:t></m:r></m:sub></m:sSub></m:e>
                    </m:mr>
                    <m:mr>
                        <m:e><m:r><m:t>⋮</m:t></m:r></m:e>
                        <m:e><m:r><m:t>⋮</m:t></m:r></m:e>
                        <m:e><m:r><m:t>⋱</m:t></m:r></m:e>
                        <m:e><m:r><m:t>⋮</m:t></m:r></m:e>
                    </m:mr>
                    <m:mr>
                        <m:e><m:sSub><m:e><m:r><m:t>x</m:t></m:r></m:e><m:sub><m:r><m:t>m1</m:t></m:r></m:sub></m:sSub></m:e>
                        <m:e><m:sSub><m:e><m:r><m:t>x</m:t></m:r></m:e><m:sub><m:r><m:t>m2</m:t></m:r></m:sub></m:sSub></m:e>
                        <m:e><m:r><m:t>⋯</m:t></m:r></m:e>
                        <m:e><m:sSub><m:e><m:r><m:t>x</m:t></m:r></m:e><m:sub><m:r><m:t>mn</m:t></m:r></m:sub></m:sSub></m:e>
                    </m:mr>
                </m:m>
            </m:e>
        </m:d>
        <m:r><m:t> berukuran 18 × 4</m:t></m:r>
    ''')

    p4_sub = doc.add_paragraph()
    p4_sub.paragraph_format.line_spacing = 1.5
    p4_sub.add_run("Rincian skor matriks keputusan (X) dari 18 alternatif guru disajikan pada tabel di bawah ini:")

    # Tabel 4.14 Matriks Keputusan X
    p_cap3 = doc.add_paragraph(style='Caption')
    add_table_caption(p_cap3, "14", "Matriks Keputusan (X) Evaluasi Kinerja Guru")

    tbl_x = doc.add_table(rows=len(data['data_guru']) + 1, cols=7)
    tbl_x.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_x.autofit = False
    set_table_borders(tbl_x)

    header_tr_x = tbl_x.rows[0]._tr.get_or_add_trPr()
    header_tr_x.append(parse_xml(f'<w:tblHeader {nsdecls("w")}/>'))
    header_tr_x.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))

    x_headers = ["No", "Alternatif", "Nama Guru", "C1 (Kehadiran)", "C2 (Ketepatan)", "C3 (Perangkat)", "C4 (Administrasi)"]
    x_widths = [Cm(0.9), Cm(2.2), Cm(4.8), Cm(2.0), Cm(2.0), Cm(2.0), Cm(2.0)]

    for ci, h_txt in enumerate(x_headers):
        cell = tbl_x.cell(0, ci)
        cell.width = x_widths[ci]
        set_cell_background(cell, "EAECEF")
        set_cell_margins(cell)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h_txt)
        r.font.bold = True
        r.font.size = Pt(9.5)

    for ri, item in enumerate(data['data_guru']):
        row = tbl_x.rows[ri + 1]
        trPr = row._tr.get_or_add_trPr()
        trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))

        c1 = f"{item['scores'].get(data['kriteria'][0][0], 0):.1f}"
        c2 = f"{item['scores'].get(data['kriteria'][1][0], 0):.1f}"
        c3 = f"{item['scores'].get(data['kriteria'][2][0], 0):.1f}"
        c4 = f"{item['scores'].get(data['kriteria'][3][0], 0):.1f}"
        vals = [str(ri + 1), item['kode_alt'], item['nama'], c1, c2, c3, c4]
        for ci, val in enumerate(vals):
            cell = row.cells[ci]
            cell.width = x_widths[ci]
            set_cell_background(cell, "FAFAFA" if ri % 2 == 1 else "FFFFFF")
            set_cell_margins(cell)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT if ci == 2 else WD_ALIGN_PARAGRAPH.CENTER
            r = p.add_run(val)
            r.font.size = Pt(9)
            if ci == 1:
                r.font.bold = True

    # 4.5.5 Langkah 2: Normalisasi Matriks (X*)
    p5 = doc.add_paragraph()
    p5.paragraph_format.line_spacing = 1.5
    p5.paragraph_format.space_before = Pt(14)
    p5.paragraph_format.space_after = Pt(4)
    p5.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    r_sec5 = p5.add_run("4.5.5 Langkah 2: Proses Normalisasi Matriks (X*)\n")
    r_sec5.font.bold = True
    r_sec5.font.size = Pt(12)
    p5.add_run(
        "Normalisasi matriks bertujuan untuk menyamakan skala pengukuran kriteria yang berbeda menjadi nilai tanpa dimensi. "
        "Rumus normalisasi rasio vektor metode MOORA dirumuskan sebagai:"
    )

    # OMML Equation: Normalisasi x*ij
    add_omml_equation(doc, r'''
        <m:sSub>
            <m:e><m:r><m:t>x*</m:t></m:r></m:e>
            <m:sub><m:r><m:t>ij</m:t></m:r></m:sub>
        </m:sSub>
        <m:r><m:t> = </m:t></m:r>
        <m:f>
            <m:num>
                <m:sSub>
                    <m:e><m:r><m:t>x</m:t></m:r></m:e>
                    <m:sub><m:r><m:t>ij</m:t></m:r></m:sub>
                </m:sSub>
            </m:num>
            <m:den>
                <m:rad>
                    <m:radPr><m:degHide m:val="1"/></m:radPr>
                    <m:deg/>
                    <m:e>
                        <m:nary>
                            <m:naryPr>
                                <m:chr m:val="∑"/>
                                <m:limLoc m:val="undOvr"/>
                            </m:naryPr>
                            <m:sub><m:r><m:t>i=1</m:t></m:r></m:sub>
                            <m:sup><m:r><m:t>m</m:t></m:r></m:sup>
                            <m:e>
                                <m:sSup>
                                    <m:e>
                                        <m:sSub>
                                            <m:e><m:r><m:t>x</m:t></m:r></m:e>
                                            <m:sub><m:r><m:t>ij</m:t></m:r></m:sub>
                                        </m:sSub>
                                    </m:e>
                                    <m:sup><m:r><m:t>2</m:t></m:r></m:sup>
                                </m:sSup>
                            </m:e>
                        </m:nary>
                    </m:e>
                </m:rad>
            </m:den>
        </m:f>
    ''')

    p5_div = doc.add_paragraph()
    p5_div.paragraph_format.line_spacing = 1.5
    p5_div.paragraph_format.space_before = Pt(4)
    p5_div.add_run(
        "di mana i = 1, 2, ..., m (jumlah guru alternatif) dan j = 1, 2, ..., n (jumlah kriteria).\n\n"
        "Perhitungan nilai penyebut (akar dari jumlah kuadrat) pada masing-masing kriteria adalah:"
    )

    # OMML Equation: 4 Divisors
    add_omml_equation(doc, r'''
        <m:r><m:t>|X</m:t></m:r>
        <m:sSub><m:e><m:r><m:t>C1</m:t></m:r></m:e><m:sub><m:r><m:t></m:t></m:r></m:sub></m:sSub>
        <m:r><m:t>| = </m:t></m:r>
        <m:rad><m:radPr><m:degHide m:val="1"/></m:radPr><m:deg/><m:e><m:r><m:t>378.00</m:t></m:r></m:e></m:rad>
        <m:r><m:t> = 19.4422</m:t></m:r>
    ''')
    add_omml_equation(doc, r'''
        <m:r><m:t>|X</m:t></m:r>
        <m:sSub><m:e><m:r><m:t>C2</m:t></m:r></m:e><m:sub><m:r><m:t></m:t></m:r></m:sub></m:sSub>
        <m:r><m:t>| = </m:t></m:r>
        <m:rad><m:radPr><m:degHide m:val="1"/></m:radPr><m:deg/><m:e><m:r><m:t>378.00</m:t></m:r></m:e></m:rad>
        <m:r><m:t> = 19.4422</m:t></m:r>
    ''')
    add_omml_equation(doc, r'''
        <m:r><m:t>|X</m:t></m:r>
        <m:sSub><m:e><m:r><m:t>C3</m:t></m:r></m:e><m:sub><m:r><m:t></m:t></m:r></m:sub></m:sSub>
        <m:r><m:t>| = </m:t></m:r>
        <m:rad><m:radPr><m:degHide m:val="1"/></m:radPr><m:deg/><m:e><m:r><m:t>351.00</m:t></m:r></m:e></m:rad>
        <m:r><m:t> = 18.7350</m:t></m:r>
    ''')
    add_omml_equation(doc, r'''
        <m:r><m:t>|X</m:t></m:r>
        <m:sSub><m:e><m:r><m:t>C4</m:t></m:r></m:e><m:sub><m:r><m:t></m:t></m:r></m:sub></m:sSub>
        <m:r><m:t>| = </m:t></m:r>
        <m:rad><m:radPr><m:degHide m:val="1"/></m:radPr><m:deg/><m:e><m:r><m:t>344.00</m:t></m:r></m:e></m:rad>
        <m:r><m:t> = 18.5472</m:t></m:r>
    ''')

    p5_samp = doc.add_paragraph()
    p5_samp.paragraph_format.line_spacing = 1.5
    p5_samp.paragraph_format.space_before = Pt(6)
    p5_samp.paragraph_format.space_after = Pt(4)
    p5_samp.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p5_samp.add_run(
        "Contoh perhitungan normalisasi pada guru alternatif A1 (Muhammad Rizky, S.Pd.I. dengan nilai [5.0, 5.0, 5.0, 5.0]):"
    )

    # OMML Equation: Sample A1 Normalization
    add_omml_equation(doc, r'''
        <m:sSub><m:e><m:r><m:t>x*</m:t></m:r></m:e><m:sub><m:r><m:t>11</m:t></m:r></m:sub></m:sSub>
        <m:r><m:t> = </m:t></m:r>
        <m:f><m:num><m:r><m:t>5.0</m:t></m:r></m:num><m:den><m:r><m:t>19.4422</m:t></m:r></m:den></m:f>
        <m:r><m:t> = 0.2572,   </m:t></m:r>
        <m:sSub><m:e><m:r><m:t>x*</m:t></m:r></m:e><m:sub><m:r><m:t>12</m:t></m:r></m:sub></m:sSub>
        <m:r><m:t> = </m:t></m:r>
        <m:f><m:num><m:r><m:t>5.0</m:t></m:r></m:num><m:den><m:r><m:t>19.4422</m:t></m:r></m:den></m:f>
        <m:r><m:t> = 0.2572</m:t></m:r>
    ''')
    add_omml_equation(doc, r'''
        <m:sSub><m:e><m:r><m:t>x*</m:t></m:r></m:e><m:sub><m:r><m:t>13</m:t></m:r></m:sub></m:sSub>
        <m:r><m:t> = </m:t></m:r>
        <m:f><m:num><m:r><m:t>5.0</m:t></m:r></m:num><m:den><m:r><m:t>18.7350</m:t></m:r></m:den></m:f>
        <m:r><m:t> = 0.2669,   </m:t></m:r>
        <m:sSub><m:e><m:r><m:t>x*</m:t></m:r></m:e><m:sub><m:r><m:t>14</m:t></m:r></m:sub></m:sSub>
        <m:r><m:t> = </m:t></m:r>
        <m:f><m:num><m:r><m:t>5.0</m:t></m:r></m:num><m:den><m:r><m:t>18.5472</m:t></m:r></m:den></m:f>
        <m:r><m:t> = 0.2696</m:t></m:r>
    ''')

    p5_tbl_desc = doc.add_paragraph()
    p5_tbl_desc.paragraph_format.line_spacing = 1.5
    p5_tbl_desc.add_run("Hasil matriks keputusan yang telah ternormalisasi secara lengkap disajikan pada tabel berikut:")

    # Tabel 4.15 Matriks Normalisasi X*
    p_cap4 = doc.add_paragraph(style='Caption')
    add_table_caption(p_cap4, "15", "Matriks Ternormalisasi (X*) Metode MOORA")

    tbl_norm = doc.add_table(rows=len(data['data_guru']) + 1, cols=7)
    tbl_norm.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_norm.autofit = False
    set_table_borders(tbl_norm)

    header_tr_norm = tbl_norm.rows[0]._tr.get_or_add_trPr()
    header_tr_norm.append(parse_xml(f'<w:tblHeader {nsdecls("w")}/>'))
    header_tr_norm.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))

    norm_headers = ["No", "Alternatif", "Nama Guru", "C1 (0.35)", "C2 (0.25)", "C3 (0.25)", "C4 (0.15)"]
    norm_widths = [Cm(0.9), Cm(2.2), Cm(4.8), Cm(2.0), Cm(2.0), Cm(2.0), Cm(2.0)]

    for ci, h_txt in enumerate(norm_headers):
        cell = tbl_norm.cell(0, ci)
        cell.width = norm_widths[ci]
        set_cell_background(cell, "EAECEF")
        set_cell_margins(cell)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h_txt)
        r.font.bold = True
        r.font.size = Pt(9.5)

    for ri, item in enumerate(data['data_guru']):
        row = tbl_norm.rows[ri + 1]
        trPr = row._tr.get_or_add_trPr()
        trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))

        n1 = f"{item['norm'].get(data['kriteria'][0][0], 0):.4f}"
        n2 = f"{item['norm'].get(data['kriteria'][1][0], 0):.4f}"
        n3 = f"{item['norm'].get(data['kriteria'][2][0], 0):.4f}"
        n4 = f"{item['norm'].get(data['kriteria'][3][0], 0):.4f}"
        vals = [str(ri + 1), item['kode_alt'], item['nama'], n1, n2, n3, n4]
        for ci, val in enumerate(vals):
            cell = row.cells[ci]
            cell.width = norm_widths[ci]
            set_cell_background(cell, "FAFAFA" if ri % 2 == 1 else "FFFFFF")
            set_cell_margins(cell)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT if ci == 2 else WD_ALIGN_PARAGRAPH.CENTER
            r = p.add_run(val)
            r.font.size = Pt(9)
            if ci == 1:
                r.font.bold = True

    # 4.5.6 Langkah 3: Matriks Terbobot (W * X*)
    p6 = doc.add_paragraph()
    p6.paragraph_format.line_spacing = 1.5
    p6.paragraph_format.space_before = Pt(14)
    p6.paragraph_format.space_after = Pt(4)
    p6.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    r_sec6 = p6.add_run("4.5.6 Langkah 3: Pembobotan Matriks Normalisasi (W x X*)\n")
    r_sec6.font.bold = True
    r_sec6.font.size = Pt(12)
    p6.add_run(
        "Setelah matriks keputusan ternormalisasi, langkah selanjutnya adalah mengalikan setiap nilai elemen dengan bobot preferensi (W) "
        "kriteria yang bersesuaian sesuai rumus:"
    )

    # OMML Equation: Pembobotan vij
    add_omml_equation(doc, r'''
        <m:sSub>
            <m:e><m:r><m:t>v</m:t></m:r></m:e>
            <m:sub><m:r><m:t>ij</m:t></m:r></m:sub>
        </m:sSub>
        <m:r><m:t> = </m:t></m:r>
        <m:sSub>
            <m:e><m:r><m:t>w</m:t></m:r></m:e>
            <m:sub><m:r><m:t>j</m:t></m:r></m:sub>
        </m:sSub>
        <m:r><m:t> × </m:t></m:r>
        <m:sSub>
            <m:e><m:r><m:t>x*</m:t></m:r></m:e>
            <m:sub><m:r><m:t>ij</m:t></m:r></m:sub>
        </m:sSub>
    ''')

    p6_samp = doc.add_paragraph()
    p6_samp.paragraph_format.line_spacing = 1.5
    p6_samp.paragraph_format.space_before = Pt(4)
    p6_samp.add_run(
        "Contoh perhitungan nilai terbobot pada alternatif A1 (Muhammad Rizky, S.Pd.I.):"
    )

    # OMML Equation: Sample A1 Weighting
    add_omml_equation(doc, r'''
        <m:sSub><m:e><m:r><m:t>v</m:t></m:r></m:e><m:sub><m:r><m:t>11</m:t></m:r></m:sub></m:sSub>
        <m:r><m:t> = 0.35 × 0.2572 = 0.0900,   </m:t></m:r>
        <m:sSub><m:e><m:r><m:t>v</m:t></m:r></m:e><m:sub><m:r><m:t>12</m:t></m:r></m:sub></m:sSub>
        <m:r><m:t> = 0.25 × 0.2572 = 0.0643</m:t></m:r>
    ''')
    add_omml_equation(doc, r'''
        <m:sSub><m:e><m:r><m:t>v</m:t></m:r></m:e><m:sub><m:r><m:t>13</m:t></m:r></m:sub></m:sSub>
        <m:r><m:t> = 0.25 × 0.2669 = 0.0667,   </m:t></m:r>
        <m:sSub><m:e><m:r><m:t>v</m:t></m:r></m:e><m:sub><m:r><m:t>14</m:t></m:r></m:sub></m:sSub>
        <m:r><m:t> = 0.15 × 0.2696 = 0.0404</m:t></m:r>
    ''')

    p6_tbl_desc = doc.add_paragraph()
    p6_tbl_desc.paragraph_format.line_spacing = 1.5
    p6_tbl_desc.add_run("Hasil lengkap matriks normalisasi terbobot disajikan pada tabel di bawah ini:")

    # Tabel 4.16 Matriks Normalisasi Terbobot
    p_cap5 = doc.add_paragraph(style='Caption')
    add_table_caption(p_cap5, "16", "Matriks Normalisasi Terbobot (W x X*)")

    tbl_w = doc.add_table(rows=len(data['data_guru']) + 1, cols=7)
    tbl_w.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_w.autofit = False
    set_table_borders(tbl_w)

    header_tr_w = tbl_w.rows[0]._tr.get_or_add_trPr()
    header_tr_w.append(parse_xml(f'<w:tblHeader {nsdecls("w")}/>'))
    header_tr_w.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))

    for ci, h_txt in enumerate(norm_headers):
        cell = tbl_w.cell(0, ci)
        cell.width = norm_widths[ci]
        set_cell_background(cell, "EAECEF")
        set_cell_margins(cell)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h_txt)
        r.font.bold = True
        r.font.size = Pt(9.5)

    for ri, item in enumerate(data['data_guru']):
        row = tbl_w.rows[ri + 1]
        trPr = row._tr.get_or_add_trPr()
        trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))

        w1 = f"{item['weighted'].get(data['kriteria'][0][0], 0):.4f}"
        w2 = f"{item['weighted'].get(data['kriteria'][1][0], 0):.4f}"
        w3 = f"{item['weighted'].get(data['kriteria'][2][0], 0):.4f}"
        w4 = f"{item['weighted'].get(data['kriteria'][3][0], 0):.4f}"
        vals = [str(ri + 1), item['kode_alt'], item['nama'], w1, w2, w3, w4]
        for ci, val in enumerate(vals):
            cell = row.cells[ci]
            cell.width = norm_widths[ci]
            set_cell_background(cell, "FAFAFA" if ri % 2 == 1 else "FFFFFF")
            set_cell_margins(cell)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT if ci == 2 else WD_ALIGN_PARAGRAPH.CENTER
            r = p.add_run(val)
            r.font.size = Pt(9)
            if ci == 1:
                r.font.bold = True

    # 4.5.7 Langkah 4 & 5: Nilai Preferensi Yi dan Perankingan
    p7 = doc.add_paragraph()
    p7.paragraph_format.line_spacing = 1.5
    p7.paragraph_format.space_before = Pt(14)
    p7.paragraph_format.space_after = Pt(4)
    p7.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    r_sec7 = p7.add_run("4.5.7 Langkah 4 & 5: Perhitungan Nilai Preferensi (Yi) dan Perankingan\n")
    r_sec7.font.bold = True
    r_sec7.font.size = Pt(12)
    p7.add_run(
        "Nilai preferensi optimasi multiobjektif (Yi) merupakan nilai akhir yang mengukur performa setiap alternatif, "
        "yang dirumuskan melalui selisih antara akumulasi kriteria yang dimaksimalkan (Benefit) dan kriteria yang diminimalkan (Cost):"
    )

    # OMML Equation: Yi General Formula
    add_omml_equation(doc, r'''
        <m:sSub>
            <m:e><m:r><m:t>Y</m:t></m:r></m:e>
            <m:sub><m:r><m:t>i</m:t></m:r></m:sub>
        </m:sSub>
        <m:r><m:t> = </m:t></m:r>
        <m:nary>
            <m:naryPr>
                <m:chr m:val="∑"/>
                <m:limLoc m:val="undOvr"/>
            </m:naryPr>
            <m:sub><m:r><m:t>j=1</m:t></m:r></m:sub>
            <m:sup><m:r><m:t>g</m:t></m:r></m:sup>
            <m:e>
                <m:sSub>
                    <m:e><m:r><m:t>v</m:t></m:r></m:e>
                    <m:sub><m:r><m:t>ij</m:t></m:r></m:sub>
                </m:sSub>
            </m:e>
        </m:nary>
        <m:r><m:t> - </m:t></m:r>
        <m:nary>
            <m:naryPr>
                <m:chr m:val="∑"/>
                <m:limLoc m:val="undOvr"/>
            </m:naryPr>
            <m:sub><m:r><m:t>j=g+1</m:t></m:r></m:sub>
            <m:sup><m:r><m:t>n</m:t></m:r></m:sup>
            <m:e>
                <m:sSub>
                    <m:e><m:r><m:t>v</m:t></m:r></m:e>
                    <m:sub><m:r><m:t>ij</m:t></m:r></m:sub>
                </m:sSub>
            </m:e>
        </m:nary>
    ''')

    p7_sub = doc.add_paragraph()
    p7_sub.paragraph_format.line_spacing = 1.5
    p7_sub.paragraph_format.space_before = Pt(4)
    p7_sub.add_run(
        "Karena keempat kriteria pada penilaian ini seluruhnya bertipe BENEFIT (g = 4 dan tidak ada kriteria Cost), "
        "maka formula optimasi disederhanakan menjadi penjumlahan keempat nilai terbobot:"
    )

    # OMML Equation: Yi Specific
    add_omml_equation(doc, r'''
        <m:sSub><m:e><m:r><m:t>Y</m:t></m:r></m:e><m:sub><m:r><m:t>i</m:t></m:r></m:sub></m:sSub>
        <m:r><m:t> = </m:t></m:r>
        <m:sSub><m:e><m:r><m:t>v</m:t></m:r></m:e><m:sub><m:r><m:t>i1</m:t></m:r></m:sub></m:sSub>
        <m:r><m:t> + </m:t></m:r>
        <m:sSub><m:e><m:r><m:t>v</m:t></m:r></m:e><m:sub><m:r><m:t>i2</m:t></m:r></m:sub></m:sSub>
        <m:r><m:t> + </m:t></m:r>
        <m:sSub><m:e><m:r><m:t>v</m:t></m:r></m:e><m:sub><m:r><m:t>i3</m:t></m:r></m:sub></m:sSub>
        <m:r><m:t> + </m:t></m:r>
        <m:sSub><m:e><m:r><m:t>v</m:t></m:r></m:e><m:sub><m:r><m:t>i4</m:t></m:r></m:sub></m:sSub>
    ''')

    # Example Y1 calculation
    add_omml_equation(doc, r'''
        <m:sSub><m:e><m:r><m:t>Y</m:t></m:r></m:e><m:sub><m:r><m:t>1</m:t></m:r></m:sub></m:sSub>
        <m:r><m:t> (Muhammad Rizky, S.Pd.I.) = 0.0900 + 0.0643 + 0.0667 + 0.0404 = </m:t></m:r>
        <m:r><m:rPr><m:b/></m:rPr><m:t>0.2615</m:t></m:r>
    ''')

    p7_tbl_desc = doc.add_paragraph()
    p7_tbl_desc.paragraph_format.line_spacing = 1.5
    p7_tbl_desc.paragraph_format.space_before = Pt(6)
    p7_tbl_desc.add_run(
        "Peringkat alternatif ditentukan berdasarkan urutan nilai preferensi Yi dari yang terbesar hingga terkecil. "
        "Hasil lengkap perhitungan nilai preferensi (Yi) dan penetapan ranking kinerja guru disajikan pada tabel di bawah ini:"
    )

    # Tabel 4.17 Hasil Perankingan MOORA
    p_cap6 = doc.add_paragraph(style='Caption')
    add_table_caption(p_cap6, "17", "Hasil Akhir Nilai Preferensi (Yi) dan Peringkat Kinerja Guru (MOORA)")

    tbl_rank = doc.add_table(rows=len(data['data_ranked']) + 1, cols=7)
    tbl_rank.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_rank.autofit = False
    set_table_borders(tbl_rank)

    header_tr_rank = tbl_rank.rows[0]._tr.get_or_add_trPr()
    header_tr_rank.append(parse_xml(f'<w:tblHeader {nsdecls("w")}/>'))
    header_tr_rank.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))

    rank_headers = ["Ranking", "Alternatif", "NIP", "Nama Lengkap Guru", "Tugas Mengajar", "Nilai Preferensi (Yi)", "Kategori Predikat"]
    rank_widths = [Cm(1.6), Cm(2.0), Cm(3.4), Cm(4.8), Cm(3.2), Cm(2.5), Cm(2.6)]

    for ci, h_txt in enumerate(rank_headers):
        cell = tbl_rank.cell(0, ci)
        cell.width = rank_widths[ci]
        set_cell_background(cell, "EAECEF")
        set_cell_margins(cell)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h_txt)
        r.font.bold = True
        r.font.size = Pt(9.5)

    for ri, item in enumerate(data['data_ranked']):
        row = tbl_rank.rows[ri + 1]
        trPr = row._tr.get_or_add_trPr()
        trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))

        yi_val = item['yi']
        if item['ranking'] <= 3:
            predikat = "Sangat Baik"
        elif item['ranking'] <= 9:
            predikat = "Baik"
        else:
            predikat = "Cukup"

        vals = [
            f"Peringkat {item['ranking']}",
            item['kode_alt'],
            item['nip'],
            item['nama'],
            item['jabatan'],
            f"{yi_val:.4f}",
            predikat
        ]
        
        is_top3 = item['ranking'] <= 3

        for ci, val in enumerate(vals):
            cell = row.cells[ci]
            cell.width = rank_widths[ci]
            set_cell_background(cell, "E8F5E9" if is_top3 else ("FAFAFA" if ri % 2 == 1 else "FFFFFF"))
            set_cell_margins(cell)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT if ci in (3, 4) else WD_ALIGN_PARAGRAPH.CENTER
            r = p.add_run(val)
            r.font.size = Pt(9)
            if is_top3 or ci in (0, 1, 5):
                r.font.bold = True

    # 4.5.8 Kesimpulan & Pembahasan Hasil
    p8 = doc.add_paragraph()
    p8.paragraph_format.line_spacing = 1.5
    p8.paragraph_format.space_before = Pt(14)
    p8.paragraph_format.space_after = Pt(4)
    p8.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    r_sec8 = p8.add_run("4.5.8 Pembahasan Hasil Keputusan SPK MOORA\n")
    r_sec8.font.bold = True
    r_sec8.font.size = Pt(12)
    
    top1 = data['data_ranked'][0]
    top2 = data['data_ranked'][1]
    top3 = data['data_ranked'][2]

    p8.add_run(
        f"Berdasarkan hasil kalkulasi metode MOORA pada {data['periode_nama']}, dari total {len(data['gurus'])} alternatif guru yang dievaluasi, "
        f"diperoleh peringkat 3 besar guru terbaik sebagai berikut:\n\n"
        f"1. Peringkat 1 ({top1['kode_alt']}): {top1['nama']} ({top1['jabatan']}) dengan Nilai Preferensi Yi = {top1['yi']:.4f} (Predikat Sangat Baik).\n"
        f"2. Peringkat 2 ({top2['kode_alt']}): {top2['nama']} ({top2['jabatan']}) dengan Nilai Preferensi Yi = {top2['yi']:.4f} (Predikat Sangat Baik).\n"
        f"3. Peringkat 3 ({top3['kode_alt']}): {top3['nama']} ({top3['jabatan']}) dengan Nilai Preferensi Yi = {top3['yi']:.4f} (Predikat Sangat Baik).\n\n"
        "Hasil perankingan ini membuktikan bahwa metode MOORA mampu memberikan keputusan evaluasi kinerja yang objektif, "
        "transparan, dan akurat, serta dapat dijadikan dasar pertimbangan pemberian penghargaan guru berprestasi oleh Kepala Sekolah "
        "SMA Al-Ihsan Boarding School."
    )

    # Save to DOCX
    out_docx = r"c:\Penilaian_Kinerja_Guru\Bab4_Perancangan_Proses_Perhitungan_MOORA.docx"
    try:
        doc.save(out_docx)
        print(f"[SUCCESS] File DOCX berhasil disimpan di: {out_docx}")
    except PermissionError:
        alt_docx = r"c:\Penilaian_Kinerja_Guru\Bab4_Perancangan_Proses_Perhitungan_MOORA_Baru.docx"
        doc.save(alt_docx)
        print(f"[WARNING] File Bab4_Perancangan_Proses_Perhitungan_MOORA.docx sedang dibuka di Word.")
        print(f"[SUCCESS] Disimpan sebagai: {alt_docx}")

    # Generate Markdown version
    out_md = r"c:\Penilaian_Kinerja_Guru\Bab4_Perancangan_Proses_Perhitungan_MOORA.md"
    with open(out_md, "w", encoding="utf-8") as f:
        f.write("# BAB IV: HASIL DAN PEMBAHASAN\n")
        f.write("## 4.5 Perancangan dan Penerapan Proses Perhitungan Metode MOORA\n\n")
        f.write("### 4.5.1 Konsep Dasar dan Tahapan Metode MOORA\n\n")
        f.write("Metode MOORA (*Multi-Objective Optimization on the basis of Ratio Analysis*) digunakan untuk menentukan perangkingan kinerja guru berdasarkan rasio optimal multiobjektif.\n\n")
        
        f.write("### 4.5.2 Kriteria Penilaian dan Bobot Preferensi\n\n")
        f.write("$$\\sum_{j=1}^{n} w_j = 1.00 \\quad (100\\%$$\n\n")
        f.write("**Tabel 4.12. Daftar Kriteria, Bobot Preferensi, dan Sifat Atribut MOORA**\n\n")
        f.write("| No | Kode | Nama Kriteria Penilaian | Bobot (W) | Sifat / Atribut |\n")
        f.write("| :---: | :---: | :--- | :---: | :---: |\n")
        for ri, kr in enumerate(data['kriteria']):
            f.write(f"| {ri+1} | `{kr[1]}` | {kr[2]} | {kr[3]:.2f} ({int(kr[3]*100)}%) | {kr[4]} |\n")
        f.write("\n---\n\n")

        f.write("### 4.5.3 Data Alternatif Guru yang Dievaluasi\n\n")
        f.write(f"**Tabel 4.13. Daftar Alternatif Guru SMA Al-Ihsan Boarding School ({data['periode_nama']})**\n\n")
        f.write("| No | Kode Alt | NIP | Nama Lengkap Guru | Tugas Mengajar |\n")
        f.write("| :---: | :---: | :---: | :--- | :--- |\n")
        for ri, item in enumerate(data['data_guru']):
            f.write(f"| {ri+1} | **{item['kode_alt']}** | `{item['nip']}` | {item['nama']} | {item['jabatan']} |\n")
        f.write("\n---\n\n")

        f.write("### 4.5.4 Langkah 1: Pembentukan Matriks Keputusan (X)\n\n")
        f.write("$$X = \\begin{bmatrix} x_{11} & x_{12} & \\dots & x_{1n} \\\\ x_{21} & x_{22} & \\dots & x_{2n} \\\\ \\vdots & \\vdots & \\ddots & \\vdots \\\\ x_{m1} & x_{m2} & \\dots & x_{mn} \\end{bmatrix}$$\n\n")
        f.write("**Tabel 4.14. Matriks Keputusan (X) Evaluasi Kinerja Guru**\n\n")
        f.write("| No | Alternatif | Nama Guru | C1 | C2 | C3 | C4 |\n")
        f.write("| :---: | :---: | :--- | :---: | :---: | :---: | :---: |\n")
        for ri, item in enumerate(data['data_guru']):
            c1 = f"{item['scores'].get(data['kriteria'][0][0], 0):.1f}"
            c2 = f"{item['scores'].get(data['kriteria'][1][0], 0):.1f}"
            c3 = f"{item['scores'].get(data['kriteria'][2][0], 0):.1f}"
            c4 = f"{item['scores'].get(data['kriteria'][3][0], 0):.1f}"
            f.write(f"| {ri+1} | **{item['kode_alt']}** | {item['nama']} | {c1} | {c2} | {c3} | {c4} |\n")
        f.write("\n---\n\n")

        f.write("### 4.5.5 Langkah 2: Proses Normalisasi Matriks (X*)\n\n")
        f.write("$$x^*_{ij} = \\frac{x_{ij}}{\\sqrt{\\sum_{i=1}^{m} x_{ij}^2}}$$\n\n")
        f.write("- $|X_{C1}| = \\sqrt{378.00} = 19.4422$\n")
        f.write("- $|X_{C2}| = \\sqrt{378.00} = 19.4422$\n")
        f.write("- $|X_{C3}| = \\sqrt{351.00} = 18.7350$\n")
        f.write("- $|X_{C4}| = \\sqrt{344.00} = 18.5472$\n\n")
        f.write("**Tabel 4.15. Matriks Ternormalisasi (X*) Metode MOORA**\n\n")
        f.write("| No | Alternatif | Nama Guru | C1 (0.35) | C2 (0.25) | C3 (0.25) | C4 (0.15) |\n")
        f.write("| :---: | :---: | :--- | :---: | :---: | :---: | :---: |\n")
        for ri, item in enumerate(data['data_guru']):
            n1 = f"{item['norm'].get(data['kriteria'][0][0], 0):.4f}"
            n2 = f"{item['norm'].get(data['kriteria'][1][0], 0):.4f}"
            n3 = f"{item['norm'].get(data['kriteria'][2][0], 0):.4f}"
            n4 = f"{item['norm'].get(data['kriteria'][3][0], 0):.4f}"
            f.write(f"| {ri+1} | **{item['kode_alt']}** | {item['nama']} | {n1} | {n2} | {n3} | {n4} |\n")
        f.write("\n---\n\n")

        f.write("### 4.5.6 Langkah 3: Pembobotan Matriks Normalisasi (W x X*)\n\n")
        f.write("$$v_{ij} = w_j \\times x^*_{ij}$$\n\n")
        f.write("**Tabel 4.16. Matriks Normalisasi Terbobot (W x X*)**\n\n")
        f.write("| No | Alternatif | Nama Guru | C1 (0.35) | C2 (0.25) | C3 (0.25) | C4 (0.15) |\n")
        f.write("| :---: | :---: | :--- | :---: | :---: | :---: | :---: |\n")
        for ri, item in enumerate(data['data_guru']):
            w1 = f"{item['weighted'].get(data['kriteria'][0][0], 0):.4f}"
            w2 = f"{item['weighted'].get(data['kriteria'][1][0], 0):.4f}"
            w3 = f"{item['weighted'].get(data['kriteria'][2][0], 0):.4f}"
            w4 = f"{item['weighted'].get(data['kriteria'][3][0], 0):.4f}"
            f.write(f"| {ri+1} | **{item['kode_alt']}** | {item['nama']} | {w1} | {w2} | {w3} | {w4} |\n")
        f.write("\n---\n\n")

        f.write("### 4.5.7 Langkah 4 & 5: Hasil Akhir Nilai Preferensi (Yi) dan Perankingan\n\n")
        f.write("$$Y_i = \\sum_{j=1}^{g} v_{ij} - \\sum_{j=g+1}^{n} v_{ij}$$\n\n")
        f.write("**Tabel 4.17. Hasil Akhir Nilai Preferensi (Yi) dan Peringkat Kinerja Guru (MOORA)**\n\n")
        f.write("| Ranking | Alternatif | NIP | Nama Lengkap Guru | Tugas Mengajar | Nilai Preferensi (Yi) | Predikat |\n")
        f.write("| :---: | :---: | :---: | :--- | :--- | :---: | :---: |\n")
        for ri, item in enumerate(data['data_ranked']):
            pred = "Sangat Baik" if item['ranking'] <= 3 else ("Baik" if item['ranking'] <= 9 else "Cukup")
            f.write(f"| **Peringkat {item['ranking']}** | **{item['kode_alt']}** | `{item['nip']}` | {item['nama']} | {item['jabatan']} | **{item['yi']:.4f}** | {pred} |\n")
            
        f.write("\n---\n\n")
        f.write("### 4.5.8 Pembahasan Hasil Keputusan SPK MOORA\n\n")
        f.write(f"Berdasarkan hasil kalkulasi metode MOORA pada {data['periode_nama']}:\n")
        f.write(f"1. **Peringkat 1 ({top1['kode_alt']})**: {top1['nama']} ({top1['jabatan']}) — Nilai Preferensi Yi = `{top1['yi']:.4f}` (Sangat Baik)\n")
        f.write(f"2. **Peringkat 2 ({top2['kode_alt']})**: {top2['nama']} ({top2['jabatan']}) — Nilai Preferensi Yi = `{top2['yi']:.4f}` (Sangat Baik)\n")
        f.write(f"3. **Peringkat 3 ({top3['kode_alt']})**: {top3['nama']} ({top3['jabatan']}) — Nilai Preferensi Yi = `{top3['yi']:.4f}` (Sangat Baik)\n")

    print(f"[SUCCESS] File Markdown berhasil disimpan di: {out_md}")

if __name__ == "__main__":
    create_moora_document()
