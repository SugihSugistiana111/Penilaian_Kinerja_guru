import docx
from docx.shared import Inches, Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn
import os

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
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

def set_table_borders(table, color="CCCCCC", sz="4", val="single"):
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

def add_caption_field(paragraph, table_num_suffix, title_text, label="Tabel"):
    """
    Menambahkan caption Word otomatis dengan SEQ field yang kompatibel 
    dengan References -> Insert Table of Figures (Daftar Tabel).
    """
    paragraph.alignment = WD_ALIGN_PARAGRAPH.LEFT
    paragraph.paragraph_format.space_before = Pt(8)
    paragraph.paragraph_format.space_after = Pt(4)
    paragraph.paragraph_format.keep_with_next = True
    
    # Run 1: Label prefix "Tabel 4."
    r1 = paragraph.add_run(f"Tabel 4.")
    r1.font.name = 'Times New Roman'
    r1.font.size = Pt(11)
    r1.font.bold = True
    
    # Field SEQ Tabel
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
    ''' % (nsdecls("w"), table_num_suffix)
    paragraph._p.append(parse_xml(fld_xml))
    
    # Run 2: Titik dan Judul Tabel
    r2 = paragraph.add_run(f" {title_text}")
    r2.font.name = 'Times New Roman'
    r2.font.size = Pt(11)
    r2.font.bold = True

def create_table_structure_document():
    doc = docx.Document()
    
    # Page setup - A4, Margin Standar Skripsi (Top 3cm, Left 4cm, Bottom 3cm, Right 3cm)
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
    
    # Judul Bab / Header
    h1 = doc.add_paragraph()
    h1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_h1 = h1.add_run("BAB IV\nHASIL DAN PEMBAHASAN\nPERANCANGAN STRUKTUR TABEL BASIS DATA")
    r_h1.font.name = 'Times New Roman'
    r_h1.font.size = Pt(14)
    r_h1.font.bold = True
    h1.paragraph_format.space_after = Pt(18)
    
    # Intro
    p_intro = doc.add_paragraph()
    p_intro.paragraph_format.line_spacing = 1.5
    p_intro.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    r_intro = p_intro.add_run(
        "Perancangan basis data pada Sistem Pendukung Keputusan (SPK) Penilaian Kinerja Guru dengan metode "
        "Multi-Objective Optimization on the basis of Ratio Analysis (MOORA) di SMA Al-Ihsan Boarding School "
        "terdiri dari 11 (sebelas) entitas tabel utama. Struktur rancangan setiap tabel dijelaskan secara rinci "
        "meliputi nama field, tipe data, ukuran (size), dan keterangan fungsi atribut sebagai berikut:"
    )
    r_intro.font.name = 'Times New Roman'
    r_intro.font.size = Pt(12)
    
    # Data tables specification
    tables_data = [
        {
            "num": "1",
            "name": "Role",
            "title": "Struktur Tabel Role (tbl_role)",
            "desc": "Tabel Role digunakan untuk menyimpan data tingkat hak akses atau peran pengguna dalam sistem (Administrator, Kepala Sekolah, dan Guru).",
            "primary_key": "id",
            "foreign_keys": "-",
            "fields": [
                ["1", "id", "VARCHAR", "30", "Primary Key, Identifier unik peran pengguna (CUID)"],
                ["2", "namaRole", "VARCHAR", "50", "Nama hak akses pengguna (ADMIN, KEPALA_SEKOLAH, GURU), Unique"]
            ]
        },
        {
            "num": "2",
            "name": "User",
            "title": "Struktur Tabel User (tbl_user)",
            "desc": "Tabel User digunakan untuk menyimpan data kredensial akun pengguna sistem untuk keperluan autentikasi dan otorisasi login.",
            "primary_key": "id",
            "foreign_keys": "roleId -> Role(id), guruId -> Guru(id)",
            "fields": [
                ["1", "id", "VARCHAR", "30", "Primary Key, Identifier unik akun pengguna (CUID)"],
                ["2", "nama", "VARCHAR", "100", "Nama lengkap pengguna"],
                ["3", "username", "VARCHAR", "50", "Username unik untuk autentikasi login (Unique)"],
                ["4", "password", "VARCHAR", "255", "Password akun pengguna terenkripsi (Hash/Bcrypt)"],
                ["5", "roleId", "VARCHAR", "30", "Foreign Key mengacu pada tabel Role (id)"],
                ["6", "guruId", "VARCHAR", "30", "Foreign Key mengacu pada tabel Guru (id), Nullable"],
                ["7", "status", "BOOLEAN", "-", "Status keaktifan akun pengguna (Default: true)"],
                ["8", "createdAt", "DATETIME", "-", "Waktu pencatatan/pembuatan akun pengguna"],
                ["9", "updatedAt", "DATETIME", "-", "Waktu pembaruan data pengguna terakhir"]
            ]
        },
        {
            "num": "3",
            "name": "Guru",
            "title": "Struktur Tabel Guru (tbl_guru)",
            "desc": "Tabel Guru digunakan untuk menyimpan data master identitas guru, penugasan mengajar, dan beban kerja yang menjadi alternatif dalam penilaian kinerja.",
            "primary_key": "id",
            "foreign_keys": "-",
            "fields": [
                ["1", "id", "VARCHAR", "30", "Primary Key, Identifier unik data guru (CUID)"],
                ["2", "nip", "VARCHAR", "30", "Nomor Induk Pegawai / NIK Guru (Unique)"],
                ["3", "nama", "VARCHAR", "100", "Nama lengkap guru beserta gelar"],
                ["4", "jenisKelamin", "VARCHAR", "10", "Jenis kelamin guru (L = Laki-laki / P = Perempuan)"],
                ["5", "jabatanTugasMengajar", "VARCHAR", "100", "Mata pelajaran yang diampu / penugasan dinas"],
                ["6", "tugasTambahanUtama", "VARCHAR", "100", "Tugas tambahan utama (e.g. Wali Kelas), Nullable"],
                ["7", "tugasTambahanLain", "VARCHAR", "100", "Tugas tambahan lain yang diemban guru, Nullable"],
                ["8", "jumlahSiswaPerRombel", "INTEGER", "4", "Rata-rata jumlah siswa per rombongan belajar"],
                ["9", "jumlahJamAjar", "INTEGER", "4", "Total jam beban tatap muka mengajar per minggu"],
                ["10", "mengajarKelas10", "BOOLEAN", "-", "Status mengajar kelas 10 (Default: false)"],
                ["11", "mengajarKelas11", "BOOLEAN", "-", "Status mengajar kelas 11 (Default: false)"],
                ["12", "mengajarKelas12", "BOOLEAN", "-", "Status mengajar kelas 12 (Default: false)"],
                ["13", "statusAktif", "BOOLEAN", "-", "Status keaktifan status guru (Default: true)"],
                ["14", "createdAt", "DATETIME", "-", "Waktu pertama kali data guru didaftarkan"],
                ["15", "updatedAt", "DATETIME", "-", "Waktu pembaruan profil data guru terakhir"]
            ]
        },
        {
            "num": "4",
            "name": "Kriteria",
            "title": "Struktur Tabel Kriteria (tbl_kriteria)",
            "desc": "Tabel Kriteria digunakan untuk mengelola data kriteria penilaian kinerja guru beserta bobot preferensi dan kategori sifat atribut MOORA (Benefit atau Cost).",
            "primary_key": "id",
            "foreign_keys": "-",
            "fields": [
                ["1", "id", "VARCHAR", "30", "Primary Key, Identifier unik kriteria penilaian (CUID)"],
                ["2", "kode", "VARCHAR", "10", "Kode identifikasi kriteria (C1, C2, C3, C4, dst), Unique"],
                ["3", "nama", "VARCHAR", "100", "Nama kriteria evaluasi kinerja guru"],
                ["4", "bobot", "FLOAT", "-", "Nilai bobot preferensi kriteria (Rentang 0.00 - 1.00)"],
                ["5", "jenis", "VARCHAR", "10", "Sifat kriteria dalam metode MOORA (BENEFIT / COST)"],
                ["6", "status", "BOOLEAN", "-", "Status keaktifan kriteria dalam penilaian (Default: true)"],
                ["7", "createdAt", "DATETIME", "-", "Waktu penambahan data kriteria"],
                ["8", "updatedAt", "DATETIME", "-", "Waktu pembaruan konfigurasi kriteria terakhir"]
            ]
        },
        {
            "num": "5",
            "name": "SkalaPenilaian",
            "title": "Struktur Tabel Skala Penilaian (tbl_skala_penilaian)",
            "desc": "Tabel Skala Penilaian digunakan untuk menyimpan rubrik tingkatan skor penilaian (sub-kriteria) dan indikator ketercapaian kompetensi.",
            "primary_key": "id",
            "foreign_keys": "kriteriaId -> Kriteria(id)",
            "fields": [
                ["1", "id", "VARCHAR", "30", "Primary Key, Identifier unik skala nilai (CUID)"],
                ["2", "kriteriaId", "VARCHAR", "30", "Foreign Key mengacu pada tabel Kriteria (id), Nullable"],
                ["3", "nilai", "INTEGER", "2", "Tingkatan skor kuantitatif rubrik (Nilai 1 - 5)"],
                ["4", "label", "VARCHAR", "50", "Label predikat (Sangat Baik, Baik, Cukup, Kurang, Sangat Kurang)"],
                ["5", "keterangan", "TEXT", "-", "Deskripsi indikator ketercapaian rubrik penilaian, Nullable"]
            ]
        },
        {
            "num": "6",
            "name": "PeriodePenilaian",
            "title": "Struktur Tabel Periode Penilaian (tbl_periode_penilaian)",
            "desc": "Tabel Periode Penilaian digunakan untuk mencatat dan mengorganisir gelombang evaluasi kinerja guru berkala (bulanan/semesteran/tahunan).",
            "primary_key": "id",
            "foreign_keys": "-",
            "fields": [
                ["1", "id", "VARCHAR", "30", "Primary Key, Identifier unik periode penilaian (CUID)"],
                ["2", "bulan", "VARCHAR", "20", "Nama bulan pelaksanaan evaluasi (Januari - Desember)"],
                ["3", "tahun", "INTEGER", "4", "Tahun pelaksanaan evaluasi (e.g. 2026)"],
                ["4", "namaPeriode", "VARCHAR", "50", "Label nama periode evaluasi (e.g. 'Juni 2026')"],
                ["5", "status", "VARCHAR", "20", "Status operasional periode (DRAFT, AKTIF, SELESAI)"],
                ["6", "createdAt", "DATETIME", "-", "Waktu pembuatan agenda periode"],
                ["7", "updatedAt", "DATETIME", "-", "Waktu pembaruan status periode"]
            ]
        },
        {
            "num": "7",
            "name": "Penilaian",
            "title": "Struktur Tabel Penilaian (tbl_penilaian)",
            "desc": "Tabel Penilaian digunakan untuk menyimpan data transaksi evaluasi kinerja setiap guru pada periode penilaian tertentu.",
            "primary_key": "id",
            "foreign_keys": "guruId -> Guru(id), periodeId -> PeriodePenilaian(id)",
            "fields": [
                ["1", "id", "VARCHAR", "30", "Primary Key, Identifier transaksi penilaian (CUID)"],
                ["2", "guruId", "VARCHAR", "30", "Foreign Key mengacu pada tabel Guru (id)"],
                ["3", "periodeId", "VARCHAR", "30", "Foreign Key mengacu pada tabel PeriodePenilaian (id)"],
                ["4", "dinilaiOleh", "VARCHAR", "100", "Nama evaluator/penilai (e.g. Kepala Sekolah), Nullable"],
                ["5", "status", "VARCHAR", "20", "Status status evaluasi (DRAFT / SELESAI)"],
                ["6", "catatan", "TEXT", "-", "Catatan kualitatif saran dan evaluasi penilai, Nullable"],
                ["7", "createdAt", "DATETIME", "-", "Waktu perekaman entri penilaian"],
                ["8", "updatedAt", "DATETIME", "-", "Waktu perubahan skor atau catatan penilaian"]
            ]
        },
        {
            "num": "8",
            "name": "DetailPenilaian",
            "title": "Struktur Tabel Detail Penilaian (tbl_detail_penilaian)",
            "desc": "Tabel Detail Penilaian digunakan untuk menyimpan rincian skor nilai asli (raw score) pada masing-masing kriteria untuk setiap guru.",
            "primary_key": "id",
            "foreign_keys": "penilaianId -> Penilaian(id), kriteriaId -> Kriteria(id)",
            "fields": [
                ["1", "id", "VARCHAR", "30", "Primary Key, Identifier unik detail penilaian (CUID)"],
                ["2", "penilaianId", "VARCHAR", "30", "Foreign Key mengacu pada tabel Penilaian (id)"],
                ["3", "kriteriaId", "VARCHAR", "30", "Foreign Key mengacu pada tabel Kriteria (id)"],
                ["4", "nilai", "FLOAT", "-", "Nilai skor kriteria yang diberikan penilai (Skala 1.0 - 5.0)"]
            ]
        },
        {
            "num": "9",
            "name": "HasilMoora",
            "title": "Struktur Tabel Hasil MOORA (tbl_hasil_moora)",
            "desc": "Tabel Hasil MOORA digunakan untuk menyimpan nilai akhir preferensi optimasi multiobjektif (Yi) dan urutan peringkat (ranking) kinerja guru.",
            "primary_key": "id",
            "foreign_keys": "guruId -> Guru(id), periodeId -> PeriodePenilaian(id)",
            "fields": [
                ["1", "id", "VARCHAR", "30", "Primary Key, Identifier unik hasil kalkulasi MOORA (CUID)"],
                ["2", "guruId", "VARCHAR", "30", "Foreign Key mengacu pada tabel Guru (id)"],
                ["3", "periodeId", "VARCHAR", "30", "Foreign Key mengacu pada tabel PeriodePenilaian (id)"],
                ["4", "nilaiPreferensi", "FLOAT", "-", "Nilai akhir preferensi MOORA (Nilai Yi = Max Benefit - Min Cost)"],
                ["5", "ranking", "INTEGER", "4", "Urutan ranking kinerja guru berdasarkan nilai preferensi tertinggi"],
                ["6", "createdAt", "DATETIME", "-", "Waktu pemrosesan kalkulasi SPK MOORA"]
            ]
        },
        {
            "num": "10",
            "name": "DetailMoora",
            "title": "Struktur Tabel Detail MOORA (tbl_detail_moora)",
            "desc": "Tabel Detail MOORA digunakan untuk menyimpan jejak matriks per kriteria (matriks keputusan X, matriks ternormalisasi X*, bobot W, dan matriks terbobot).",
            "primary_key": "id",
            "foreign_keys": "hasilMooraId -> HasilMoora(id), kriteriaId -> Kriteria(id)",
            "fields": [
                ["1", "id", "VARCHAR", "30", "Primary Key, Identifier unik detail matriks MOORA (CUID)"],
                ["2", "hasilMooraId", "VARCHAR", "30", "Foreign Key mengacu pada tabel HasilMoora (id)"],
                ["3", "kriteriaId", "VARCHAR", "30", "Foreign Key mengacu pada tabel Kriteria (id)"],
                ["4", "nilaiAwal", "FLOAT", "-", "Nilai asli skor kriteria (Matriks Keputusan Xij)"],
                ["5", "nilaiNormalisasi", "FLOAT", "-", "Nilai matriks setelah normalisasi vektor MOORA (X*ij)"],
                ["6", "bobot", "FLOAT", "-", "Bobot preferensi kriteria yang diaplikasikan (Wj)"],
                ["7", "nilaiTerbobot", "FLOAT", "-", "Nilai matriks setelah dikalikan bobot kriteria (Wj * X*ij)"]
            ]
        },
        {
            "num": "11",
            "name": "LogAktivitas",
            "title": "Struktur Tabel Log Aktivitas (tbl_log_aktivitas)",
            "desc": "Tabel Log Aktivitas digunakan untuk mencatat riwayat audit trail setiap tindakan pengguna pada sistem guna menjaga keamanan data.",
            "primary_key": "id",
            "foreign_keys": "userId -> User(id)",
            "fields": [
                ["1", "id", "VARCHAR", "30", "Primary Key, Identifier unik log aktivitas (CUID)"],
                ["2", "userId", "VARCHAR", "30", "Foreign Key mengacu pada tabel User (id), Nullable"],
                ["3", "aktivitas", "VARCHAR", "255", "Deskripsi aktivitas atau transaksi yang dijalankan pengguna"],
                ["4", "modul", "VARCHAR", "100", "Nama modul sistem terkait (e.g. Master Guru, Penilaian, MOORA)"],
                ["5", "dataId", "VARCHAR", "50", "Identifier rekaman data yang dimanipulasi, Nullable"],
                ["6", "waktu", "DATETIME", "-", "Waktu pencatatan aktivitas berlangsung (Timestamp)"],
                ["7", "alamatIp", "VARCHAR", "50", "Alamat IP perangkat pengguna (IP Address), Nullable"]
            ]
        }
    ]

    col_widths = [Cm(0.9), Cm(4.2), Cm(2.2), Cm(1.6), Cm(5.5)]
    headers = ["No", "Field", "Type", "Size", "Keterangan"]

    for idx, t_info in enumerate(tables_data):
        # Paragraph deskripsi singkat tabel
        p_desc = doc.add_paragraph()
        p_desc.paragraph_format.line_spacing = 1.5
        p_desc.paragraph_format.space_before = Pt(12)
        p_desc.paragraph_format.space_after = Pt(4)
        p_desc.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        
        r_num = p_desc.add_run(f"4.3.{t_info['num']} {t_info['title']}\n")
        r_num.font.bold = True
        r_num.font.size = Pt(12)
        
        r_d = p_desc.add_run(f"{t_info['desc']} Tabel ini memiliki primary key ")
        r_pk = p_desc.add_run(f"{t_info['primary_key']}")
        r_pk.font.bold = True
        
        if t_info['foreign_keys'] != "-":
            p_desc.add_run(f" dan foreign key berupa ")
            r_fk = p_desc.add_run(f"{t_info['foreign_keys']}")
            r_fk.font.italic = True
        p_desc.add_run(". Rincian struktur tabel disajikan pada tabel di bawah ini:")

        # Caption Tabel
        p_caption = doc.add_paragraph(style='Caption')
        add_caption_field(p_caption, t_info['num'], t_info['title'])

        # Table creation
        num_rows = len(t_info['fields']) + 1
        table = doc.add_table(rows=num_rows, cols=5)
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        table.autofit = False
        set_table_borders(table, color="B0B0B0", sz="4", val="single")

        # Make header repeat across pages & prevent row split
        header_tr = table.rows[0]._tr.get_or_add_trPr()
        header_tr.append(parse_xml(f'<w:tblHeader {nsdecls("w")}/>'))
        header_tr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))

        # Header Row Content
        for col_idx, h_text in enumerate(headers):
            cell = table.cell(0, col_idx)
            cell.width = col_widths[col_idx]
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            set_cell_background(cell, "EAECEF")
            set_cell_margins(cell, top=120, bottom=120, left=140, right=140)
            
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.line_spacing = 1.0
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(2)
            
            run = p.add_run(h_text)
            run.font.name = 'Times New Roman'
            run.font.size = Pt(10.5)
            run.font.bold = True

        # Data Rows Content
        for r_idx, row_data in enumerate(t_info['fields']):
            row_elem = table.rows[r_idx + 1]
            trPr = row_elem._tr.get_or_add_trPr()
            trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))

            # Alternating background
            bg_color = "FAFAFA" if r_idx % 2 == 1 else "FFFFFF"

            for c_idx, val in enumerate(row_data):
                cell = row_elem.cells[c_idx]
                cell.width = col_widths[c_idx]
                cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
                set_cell_background(cell, bg_color)
                set_cell_margins(cell, top=80, bottom=80, left=120, right=120)
                
                p = cell.paragraphs[0]
                p.paragraph_format.line_spacing = 1.15
                p.paragraph_format.space_before = Pt(2)
                p.paragraph_format.space_after = Pt(2)
                
                # Alignment
                if c_idx == 0:
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                elif c_idx in (2, 3):
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                else:
                    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                
                run = p.add_run(val)
                run.font.name = 'Times New Roman'
                run.font.size = Pt(10)
                
                # Highlight field name
                if c_idx == 1:
                    run.font.bold = True
                    if val == t_info['primary_key']:
                        run.font.underline = True

        # Empty paragraph for spacing
        p_space = doc.add_paragraph()
        p_space.paragraph_format.space_before = Pt(4)
        p_space.paragraph_format.space_after = Pt(8)

    # Save to file
    out_docx = r"c:\Penilaian_Kinerja_Guru\Bab4_Struktur_Tabel.docx"
    try:
        doc.save(out_docx)
        print(f"[SUCCESS] File DOCX berhasil dibuat di: {out_docx}")
    except PermissionError:
        alt_docx = r"c:\Penilaian_Kinerja_Guru\Bab4_Struktur_Tabel_Baru.docx"
        doc.save(alt_docx)
        print(f"[WARNING] File Bab4_Struktur_Tabel.docx sedang dibuka di Microsoft Word.")
        print(f"[SUCCESS] Disimpan sebagai: {alt_docx}")

    # Generate Markdown file as well
    out_md = r"c:\Penilaian_Kinerja_Guru\Bab4_Struktur_Tabel.md"
    with open(out_md, "w", encoding="utf-8") as f:
        f.write("# BAB IV: HASIL DAN PEMBAHASAN\n")
        f.write("## 4.3 Perancangan Struktur Tabel Basis Data\n\n")
        f.write("Perancangan basis data pada Sistem Pendukung Keputusan (SPK) Penilaian Kinerja Guru dengan metode MOORA di SMA Al-Ihsan Boarding School terdiri dari 11 (sebelas) tabel utama:\n\n")
        
        for t_info in tables_data:
            f.write(f"### 4.3.{t_info['num']} {t_info['title']}\n\n")
            f.write(f"{t_info['desc']} Memiliki Primary Key `{t_info['primary_key']}`")
            if t_info['foreign_keys'] != "-":
                f.write(f" dan Foreign Key `{t_info['foreign_keys']}`.")
            else:
                f.write(".")
            f.write("\n\n")
            f.write(f"**Tabel 4.{t_info['num']}. {t_info['title']}**\n\n")
            f.write("| No | Field | Type | Size | Keterangan |\n")
            f.write("| :---: | :--- | :---: | :---: | :--- |\n")
            for r in t_info['fields']:
                pk_mark = " *(PK)*" if r[1] == t_info['primary_key'] else ""
                f.write(f"| {r[0]} | `{r[1]}`{pk_mark} | {r[2]} | {r[3]} | {r[4]} |\n")
            f.write("\n---\n\n")
            
    print(f"[SUCCESS] File Markdown berhasil dibuat di: {out_md}")

if __name__ == "__main__":
    create_table_structure_document()
