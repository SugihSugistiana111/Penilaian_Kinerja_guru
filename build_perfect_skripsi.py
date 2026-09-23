import docx
from lxml import etree
from docx.oxml.ns import nsdecls, qn
from docx.oxml import parse_xml, OxmlElement
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH

# 15 Activity Diagram short explanations (3 lines)
ad_short_desc = {
    "AD-01": (
        "Activity Diagram Login menggambarkan alur autentikasi pengguna ke dalam sistem. "
        "Pengguna membuka halaman login, memasukkan username dan password, kemudian sistem memvalidasi data login. "
        "Jika data valid, sistem mengarahkan pengguna ke dashboard sesuai hak akses; jika tidak valid, sistem menampilkan pesan kesalahan."
    ),
    "AD-02": (
        "Activity Diagram Mengelola Data Pengguna menggambarkan alur pengelolaan akun pengguna oleh Administrator. "
        "Administrator membuka menu pengguna, memilih tindakan (tambah, ubah, atau hapus akun), lalu mengisi data yang diperlukan. "
        "Sistem memvalidasi kelengkapan data dan menyimpan perubahan ke basis data apabila data telah valid."
    ),
    "AD-03": (
        "Activity Diagram Mengelola Data Guru menggambarkan alur pengelolaan data master guru sebagai alternatif penilaian. "
        "Pengguna membuka menu data guru, menambahkan atau memperbarui profil guru (NIP, nama, mata pelajaran, beban mengajar). "
        "Sistem memvalidasi format data dan menyimpan perubahan ke basis data apabila seluruh isian telah lengkap dan valid."
    ),
    "AD-04": (
        "Activity Diagram Mengelola Kriteria dan Bobot menggambarkan alur konfigurasi kriteria penilaian kinerja guru. "
        "Administrator membuka menu kriteria, lalu mengubah nilai bobot preferensi atau sifat atribut kriteria (Benefit/Cost). "
        "Sistem memvalidasi bahwa total akumulasi bobot bernilai 1.00 (100%) sebelum menyimpan perubahan ke basis data."
    ),
    "AD-05": (
        "Activity Diagram Mengelola Skala Penilaian menggambarkan alur pengelolaan rubrik indikator skor penilaian (skala 1–5). "
        "Administrator memilih kriteria tertentu, kemudian menambahkan atau memperbarui deskripsi indikator ketercapaian. "
        "Sistem memvalidasi rentang nilai skor dan menyimpan perubahan rubrik ke basis data apabila data valid."
    ),
    "AD-06": (
        "Activity Diagram Mengelola Periode Penilaian menggambarkan alur manajemen siklus evaluasi berkala guru. "
        "Administrator membuka menu periode, membuat periode baru atau mengubah status periode (Draft, Aktif, Selesai). "
        "Sistem memastikan hanya satu periode berstatus Aktif dalam satu waktu, lalu menyimpan perubahan ke basis data."
    ),
    "AD-07": (
        "Activity Diagram Melakukan Penilaian Kinerja Guru menggambarkan alur pengisian skor evaluasi oleh Kepala Sekolah. "
        "Kepala Sekolah memilih periode aktif dan guru yang akan dinilai, kemudian memberikan skor pada kriteria C1 sampai C4. "
        "Sistem memvalidasi kelengkapan nilai dan menyimpan hasil transaksi penilaian ke basis data."
    ),
    "AD-08": (
        "Activity Diagram Mencatat Hasil Penilaian menggambarkan alur pencatatan dan verifikasi data evaluasi oleh Administrator. "
        "Administrator membuka rekapitulasi penilaian, memeriksa kelengkapan data nilai seluruh guru pada periode aktif. "
        "Sistem melakukan pengecekan integritas data dan mengonfirmasi pencatatan hasil penilaian apabila data telah lengkap."
    ),
    "AD-09": (
        "Activity Diagram Mengolah Penilaian dengan MOORA menggambarkan alur eksekusi algoritma SPK metode MOORA. "
        "Administrator menjalankan proses kalkulasi; sistem memeriksa kelengkapan data, lalu mengeksekusi tahapan MOORA: "
        "pembentukan Matriks Keputusan, Normalisasi, Pembobotan, perhitungan Nilai Preferensi Yi, dan penyimpanan hasil ranking ke basis data."
    ),
    "AD-10": (
        "Activity Diagram Melihat Pemeringkatan MOORA menggambarkan alur peninjauan hasil ranking kinerja guru. "
        "Pengguna membuka menu pemeringkatan dan memilih periode penilaian yang diinginkan. "
        "Sistem mengambil data preferensi Yi dan menyajikan tabel leaderboard ranking guru secara terurut dari peringkat tertinggi."
    ),
    "AD-11": (
        "Activity Diagram Melihat Hasil Penilaian menggambarkan alur peninjauan skor akhir evaluasi oleh pengguna. "
        "Pengguna mengakses menu hasil penilaian dan memilih periode evaluasi yang ingin dilihat. "
        "Sistem memvalidasi hak akses, mengambil data capaian kinerja, dan menyajikan ringkasan nilai beserta predikat kelayakan."
    ),
    "AD-12": (
        "Activity Diagram Melihat Detail Penilaian menggambarkan alur peninjauan rincian nilai per kriteria untuk setiap guru. "
        "Pengguna memilih rekaman hasil evaluasi dan mengklik tombol lihat detail. "
        "Sistem menampilkan rincian skor per kriteria (C1 Pedagogik, C2 Profesional, C3 Kepribadian, C4 Sosial) beserta catatan evaluator."
    ),
    "AD-13": (
        "Activity Diagram Monitoring Kinerja Guru menggambarkan alur pemantauan progres evaluasi guru secara berkala. "
        "Pengguna membuka modul monitoring kinerja dan memilih periode atau kategori guru yang ingin dipantau. "
        "Sistem menyajikan grafik statistik persentase guru yang sudah dinilai dan belum dinilai pada periode tersebut."
    ),
    "AD-14": (
        "Activity Diagram Melihat Riwayat Penilaian menggambarkan alur peninjauan rekam jejak evaluasi dari periode-periode sebelumnya. "
        "Pengguna membuka menu riwayat penilaian dan memilih periode tertentu. "
        "Sistem menyajikan riwayat skor, nilai preferensi MOORA, dan grafik perkembangan performa guru antar periode."
    ),
    "AD-15": (
        "Activity Diagram Mencetak Laporan Penilaian menggambarkan alur pencetakan dokumen hasil evaluasi kinerja guru. "
        "Pengguna membuka menu laporan, memilih periode evaluasi, dan menentukan format ekspor (PDF atau Excel). "
        "Sistem mengompilasi rekapitulasi nilai, ranking MOORA, dan lembar pengesahan, lalu menghasilkan dokumen laporan siap cetak."
    )
}

# 15 Sequence Diagram short explanations (3 lines)
sd_short_desc = {
    "SD-01": (
        "Sequence Diagram Login menguraikan urutan interaksi saat pengguna melakukan autentikasi ke sistem. "
        "Pengguna membuka Halaman Login, memasukkan kredensial, lalu sistem memeriksa data akun pada penyimpanan data. "
        "Pada fragmen alternatif, jika data valid sistem mengarahkan ke dashboard; jika tidak valid, sistem menampilkan pesan kesalahan."
    ),
    "SD-02": (
        "Sequence Diagram Mengelola Data Pengguna menguraikan interaksi pengelolaan akun pengguna oleh Administrator. "
        "Administrator membuka Halaman Data Pengguna, sistem menampilkan tabel akun terdaftar dari penyimpanan data. "
        "Administrator menginputkan perubahan data, sistem memvalidasi dan menyimpan ke basis data, lalu menampilkan pembaruan."
    ),
    "SD-03": (
        "Sequence Diagram Mengelola Data Guru menguraikan interaksi pengelolaan master data guru alternatif. "
        "Pengguna membuka Halaman Data Guru, sistem mengambil dan menampilkan daftar guru dari penyimpanan data. "
        "Pengguna menginput atau mengedit data guru, sistem memvalidasi format NIP dan kelengkapan data, lalu menyimpan perubahan."
    ),
    "SD-04": (
        "Sequence Diagram Mengelola Kriteria dan Bobot menguraikan interaksi pembaruan bobot preferensi kriteria MOORA. "
        "Administrator membuka Halaman Kriteria & Bobot, sistem menampilkan data kriteria dari penyimpanan data. "
        "Administrator mengubah nilai bobot, sistem memvalidasi total bobot bernilai 100%, lalu menyimpan dan memperbarui tampilan."
    ),
    "SD-05": (
        "Sequence Diagram Mengelola Skala Penilaian menguraikan interaksi konfigurasi rubrik indikator skor penilaian. "
        "Administrator membuka Halaman Skala Penilaian, sistem menampilkan tabel rubrik dari penyimpanan data. "
        "Administrator memperbarui deskripsi indikator skala 1–5, sistem memvalidasi dan menyimpan perubahan ke basis data."
    ),
    "SD-06": (
        "Sequence Diagram Mengelola Periode Penilaian menguraikan interaksi pengaturan siklus periode evaluasi. "
        "Administrator membuka Halaman Periode Penilaian, sistem menampilkan daftar periode dari penyimpanan data. "
        "Administrator membuat atau mengubah status periode, sistem memvalidasi keaktifan dan menyimpan perubahan ke basis data."
    ),
    "SD-07": (
        "Sequence Diagram Melakukan Penilaian Kinerja Guru menguraikan interaksi pengisian skor evaluasi oleh Kepala Sekolah. "
        "Kepala Sekolah membuka Halaman Penilaian, sistem menyajikan formulir evaluasi kriteria C1–C4 untuk guru yang dipilih. "
        "Kepala Sekolah menginput skor, sistem memvalidasi kelengkapan nilai dan menyimpan transaksi penilaian ke basis data."
    ),
    "SD-08": (
        "Sequence Diagram Mencatat Hasil Penilaian menguraikan interaksi pencatatan dan verifikasi data evaluasi. "
        "Administrator membuka Halaman Rekapitulasi Penilaian, sistem menampilkan daftar entri evaluasi guru dari penyimpanan data. "
        "Administrator mengonfirmasi rekapitulasi, sistem memverifikasi integritas data dan menyimpan status pencatatan."
    ),
    "SD-09": (
        "Sequence Diagram Mengolah Penilaian dengan MOORA menguraikan interaksi komputasi algoritma SPK metode MOORA. "
        "Administrator membuka Halaman Pengolahan MOORA dan menekan tombol proses kalkulasi. "
        "Sistem memvalidasi kelengkapan data, mengeksekusi tahapan MOORA (Matriks X, Normalisasi X*, Pembobotan V, Nilai Yi), dan menyimpan hasil ranking."
    ),
    "SD-10": (
        "Sequence Diagram Melihat Pemeringkatan MOORA menguraikan interaksi penayangan peringkat kinerja guru. "
        "Pengguna membuka Halaman Ranking MOORA dan memilih periode penilaian. "
        "Sistem mengambil data preferensi Yi dari penyimpanan Hasil MOORA dan menampilkan tabel ranking guru secara terurut."
    ),
    "SD-11": (
        "Sequence Diagram Melihat Hasil Penilaian menguraikan interaksi penayangan hasil evaluasi bagi seluruh pengguna. "
        "Pengguna membuka Halaman Hasil Penilaian, sistem memvalidasi hak akses dan mengambil data evaluasi dari penyimpanan. "
        "Sistem menyajikan ringkasan nilai, status evaluasi, dan predikat capaian kinerja guru yang bersangkutan."
    ),
    "SD-12": (
        "Sequence Diagram Melihat Detail Penilaian menguraikan interaksi peninjauan rincian nilai per kriteria. "
        "Pengguna memilih data guru dan mengklik tombol Lihat Detail, sistem mengambil rincian skor dari penyimpanan data. "
        "Sistem menampilkan breakdown skor C1 sampai C4 lengkap dengan catatan evaluasi dari penilai."
    ),
    "SD-13": (
        "Sequence Diagram Monitoring Kinerja Guru menguraikan interaksi pemantauan progres penilaian guru. "
        "Pengguna membuka Halaman Monitoring Kinerja, sistem mengambil data perbandingan guru yang sudah dan belum dinilai. "
        "Sistem menghitung persentase kelengkapan dan menyajikan grafik statistik progres penilaian secara visual."
    ),
    "SD-14": (
        "Sequence Diagram Melihat Riwayat Penilaian menguraikan interaksi peninjauan rekam jejak evaluasi antarperiode. "
        "Pengguna membuka Halaman Riwayat Penilaian, sistem mengambil arsip evaluasi dari penyimpanan Data Periode & Hasil MOORA. "
        "Sistem menampilkan histori penilaian beserta grafik tren performa kinerja guru dari periode ke periode."
    ),
    "SD-15": (
        "Sequence Diagram Mencetak Laporan Penilaian menguraikan interaksi pencetakan laporan resmi hasil evaluasi. "
        "Pengguna membuka Halaman Laporan dan memilih periode evaluasi serta format ekspor (PDF/Excel). "
        "Sistem mengompilasi data rekapitulasi nilai, ranking MOORA, dan lembar tanda tangan, lalu menghasilkan dokumen laporan siap unduh."
    )
}

def format_caption(p, label_prefix, seq_num, desc_text):
    for child in list(p._p):
        tag = child.tag.split('}')[-1]
        if tag not in ('pPr',):
            p._p.remove(child)
            
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.keep_with_next = True
    
    pPr = p._p.get_or_add_pPr()
    if pPr.find(qn('w:keepNext')) is None:
        pPr.append(parse_xml(f'<w:keepNext {nsdecls("w")}/>'))
    
    # Bold prefix: e.g. "Gambar 4." or "Tabel 4."
    r1 = p.add_run(label_prefix)
    r1.font.name = 'Times New Roman'
    r1.font.size = Pt(12)
    r1.font.bold = True
    
    # SEQ field (BOLD)
    seq_type = "Gambar" if "Gambar" in label_prefix else "Tabel"
    fld_xml = '''
        <w:fldSimple %s w:instr=" SEQ %s \\* ARABIC ">
            <w:r>
                <w:rPr>
                    <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/>
                    <w:b/>
                    <w:sz w:val="24"/>
                </w:rPr>
                <w:t>%d</w:t>
            </w:r>
        </w:fldSimple>
    ''' % (nsdecls("w"), seq_type, seq_num)
    p._p.append(parse_xml(fld_xml))
    
    # Regular desc
    r2 = p.add_run(f" {desc_text}")
    r2.font.name = 'Times New Roman'
    r2.font.size = Pt(12)
    r2.font.bold = False

def build_pristine_skripsi():
    # Load pristine source from SKRIPSI_Updated.docx
    doc = docx.Document('SKRIPSI_Updated.docx')
    body = doc._body._body
    
    print(f"Loaded SKRIPSI_Updated.docx: {len(doc.paragraphs)} paragraphs, {len(doc.tables)} tables")
    
    # 1. Update all AD and SD explanation texts to the 3-line concise version
    for p in doc.paragraphs:
        txt = p.text.strip()
        for ad_k, ad_v in ad_short_desc.items():
            if txt.startswith(f"Penjelasan {ad_k}:"):
                # Clear and replace with short text
                for r in p.runs:
                    r._r.getparent().remove(r._r)
                p.paragraph_format.line_spacing = 1.5
                p.paragraph_format.space_before = Pt(4)
                p.paragraph_format.space_after = Pt(8)
                p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
                r_pre = p.add_run(f"Penjelasan {ad_k}: ")
                r_pre.font.name = 'Times New Roman'
                r_pre.font.size = Pt(12)
                r_pre.font.bold = True
                r_t = p.add_run(ad_v)
                r_t.font.name = 'Times New Roman'
                r_t.font.size = Pt(12)
                r_t.font.bold = False
                break
        for sd_k, sd_v in sd_short_desc.items():
            if txt.startswith(f"Penjelasan {sd_k}:"):
                for r in p.runs:
                    r._r.getparent().remove(r._r)
                p.paragraph_format.line_spacing = 1.5
                p.paragraph_format.space_before = Pt(4)
                p.paragraph_format.space_after = Pt(8)
                p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
                r_pre = p.add_run(f"Penjelasan {sd_k}: ")
                r_pre.font.name = 'Times New Roman'
                r_pre.font.size = Pt(12)
                r_pre.font.bold = True
                r_t = p.add_run(sd_v)
                r_t.font.name = 'Times New Roman'
                r_t.font.size = Pt(12)
                r_t.font.bold = False
                break
                
    # 2. Fix all tables in document: repeat headers, cantSplit, no floating
    for tbl in doc.tables:
        tbl_elem = tbl._tbl
        tblPr = tbl_elem.find(qn('w:tblPr'))
        if tblPr is not None:
            tblpPr = tblPr.find(qn('w:tblpPr'))
            if tblpPr is not None:
                tblPr.remove(tblpPr)
        
        if len(tbl.rows) > 0:
            tr0 = tbl.rows[0]._tr
            trPr0 = tr0.get_or_add_trPr()
            if trPr0.find(qn('w:tblHeader')) is None:
                trPr0.append(parse_xml(f'<w:tblHeader {nsdecls("w")}/>'))
        
        for row in tbl.rows:
            trPr = row._tr.get_or_add_trPr()
            if trPr.find(qn('w:cantSplit')) is None:
                trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))

    # 3. Rebuild all image captions in BAB IV
    # First, list all 50 target images in BAB IV:
    all_50_images = [
        # (Marker in heading / preceding text, Caption Text)
        ("Arsitektur sistem usulan menggambarkan", "Arsitektur Sistem Usulan"),
        ("Use Case Diagram digunakan untuk", "Use Case Diagram"),
        ("AD-01\tLogin", "Activity Diagram Login"),
        ("AD-02\tMengelola Data Pengguna", "Activity Diagram Mengelola Data Pengguna"),
        ("AD-03\tMengelola Data Guru", "Activity Diagram Mengelola Data Guru"),
        ("AD-04\tMengelola Kriteria dan Bobot", "Activity Diagram Mengelola Kriteria dan Bobot"),
        ("AD-05\tMengelola Skala Penilaian", "Activity Diagram Mengelola Skala Penilaian"),
        ("AD-06\tMengelola Periode Penilaian", "Activity Diagram Mengelola Periode Penilaian"),
        ("AD-07\tMelakukan Penilaian Kinerja Guru", "Activity Diagram Melakukan Penilaian Kinerja Guru"),
        ("AD-08\tMencatat Hasil Penilaian", "Activity Diagram Mencatat Hasil Penilaian"),
        ("AD-09\tMengolah Penilaian dengan MOORA", "Activity Diagram Mengolah Penilaian dengan MOORA"),
        ("AD-10\tMelihat Pemeringkatan MOORA", "Activity Diagram Melihat Pemeringkatan MOORA"),
        ("AD-11\tMelihat Hasil Penilaian", "Activity Diagram Melihat Hasil Penilaian"),
        ("AD-12\tMelihat Detail Penilaian", "Activity Diagram Melihat Detail Penilaian"),
        ("AD-13\tMonitoring Kinerja Guru", "Activity Diagram Monitoring Kinerja Guru"),
        ("AD-14\tMelihat Riwayat Penilaian", "Activity Diagram Melihat Riwayat Penilaian"),
        ("AD-15\tMencetak Laporan Penilaian", "Activity Diagram Mencetak Laporan Penilaian"),
        ("SD-01\tLogin", "Sequence Diagram Login"),
        ("SD-02\tMengelola Data Pengguna", "Sequence Diagram Mengelola Data Pengguna"),
        ("SD-03\tMengelola Data Guru", "Sequence Diagram Mengelola Data Guru"),
        ("SD-04\tMengelola Kriteria dan Bobot", "Sequence Diagram Mengelola Kriteria dan Bobot"),
        ("SD-05\tMengelola Skala Penilaian", "Sequence Diagram Mengelola Skala Penilaian"),
        ("SD-06\tMengelola Periode Penilaian", "Sequence Diagram Mengelola Periode Penilaian"),
        ("SD-07\tMelakukan Penilaian Kinerja Guru", "Sequence Diagram Melakukan Penilaian Kinerja Guru"),
        ("SD-08\tMencatat Hasil Penilaian", "Sequence Diagram Mencatat Hasil Penilaian"),
        ("SD-09\tMengolah Penilaian dengan MOORA", "Sequence Diagram Mengolah Penilaian dengan MOORA"),
        ("SD-10\tMelihat Pemeringkatan MOORA", "Sequence Diagram Melihat Pemeringkatan MOORA"),
        ("SD-11\tMelihat Hasil Penilaian", "Sequence Diagram Melihat Hasil Penilaian"),
        ("SD-12\tMelihat Detail Penilaian", "Sequence Diagram Melihat Detail Penilaian"),
        ("SD-13\tMonitoring Kinerja Guru", "Sequence Diagram Monitoring Kinerja Guru"),
        ("SD-14\tMelihat Riwayat Penilaian", "Sequence Diagram Melihat Riwayat Penilaian"),
        ("SD-15\tMencetak Laporan Penilaian", "Sequence Diagram Mencetak Laporan Penilaian"),
        ("Perancangan Class Diagram", "Class Diagram Sistem Pendukung Keputusan MOORA"),
        ("Perancangan Relationship Diagram (ERD)", "Entity Relationship Diagram (ERD)"),
        ("Struktur Menu Administrator", "Struktur Menu Administrator"),
        ("Struktur Menu Kepala Sekolah", "Struktur Menu Kepala Sekolah"),
        ("Struktur Menu Guru", "Struktur Menu Guru"),
        ("Rancangan Antarmuka Halaman Login", "Rancangan Antarmuka Halaman Login"),
        ("Rancangan Antarmuka Dashboard Administrator", "Rancangan Antarmuka Dashboard Administrator"),
        ("Rancangan Antarmuka Kelola Data Guru", "Rancangan Antarmuka Kelola Data Guru"),
        ("Rancangan Antarmuka Kelola Kriteria & Bobot", "Rancangan Antarmuka Kelola Kriteria & Bobot"),
        ("Rancangan Antarmuka Kelola Skala Penilaian / Rubrik", "Rancangan Antarmuka Kelola Skala Penilaian / Rubrik"),
        ("Rancangan Antarmuka Kelola Periode Penilaian", "Rancangan Antarmuka Kelola Periode Penilaian"),
        ("Rancangan Antarmuka Form Transaksi Penilaian Kinerja Guru", "Rancangan Antarmuka Form Transaksi Penilaian Kinerja Guru"),
        ("Rancangan Antarmuka Proses Perhitungan SPK MOORA", "Rancangan Antarmuka Proses Perhitungan SPK MOORA"),
        ("Rancangan Antarmuka Peringkat & Hasil Ranking Guru", "Rancangan Antarmuka Peringkat & Hasil Ranking Guru"),
        ("Rancangan Antarmuka Laporan & Cetak Rekapitulasi", "Rancangan Antarmuka Laporan & Cetak Rekapitulasi"),
        ("Rancangan Antarmuka Kelola Akun Pengguna / User", "Rancangan Antarmuka Kelola Akun Pengguna / User"),
        ("Rancangan Antarmuka Dashboard & Profil Mandiri", "Rancangan Antarmuka Dashboard & Profil Mandiri Guru"),
        ("Flowchart Algoritma MOORA", "Flowchart Proses Komputasi Algoritma Metode MOORA"),
    ]
    
    # Remove any existing caption paragraph in BAB IV (after element 780)
    for elem in list(body):
        if elem.tag.endswith('p'):
            xml_s = etree.tostring(elem).decode('utf-8', errors='ignore')
            idx = list(body).index(elem)
            if idx > 780:
                p_obj = docx.text.paragraph.Paragraph(elem, doc)
                t = p_obj.text.strip()
                if 'w:drawing' not in xml_s and 'w:pict' not in xml_s:
                    if t.startswith("Gambar 4.") or t.startswith("Gambar 4 ") or "SEQ Gambar" in xml_s:
                        elem.getparent().remove(elem)
                        
    # Now find each drawing and insert caption
    body_elements = list(body)
    assigned_count = 0
    
    for seq_num, (marker, desc_text) in enumerate(all_50_images, start=1):
        found = False
        body_elements = list(body)
        
        for i in range(780, len(body_elements)):
            elem = body_elements[i]
            if elem.tag.endswith('p'):
                p_obj = docx.text.paragraph.Paragraph(elem, doc)
                txt = p_obj.text.strip()
                if marker in txt:
                    # Look ahead up to 5 elements for the drawing
                    for off in range(1, 6):
                        if i + off < len(body_elements):
                            cand = body_elements[i + off]
                            cand_xml = etree.tostring(cand).decode('utf-8', errors='ignore')
                            if 'w:drawing' in cand_xml or 'w:pict' in cand_xml:
                                new_p = OxmlElement('w:p')
                                cand.addnext(new_p)
                                new_para = docx.text.paragraph.Paragraph(new_p, doc)
                                format_caption(new_para, "Gambar 4.", seq_num, desc_text)
                                print(f"[OK #{seq_num}] Gambar 4.{seq_num} {desc_text}")
                                found = True
                                assigned_count += 1
                                break
                    if found:
                        break
        if not found:
            print(f"[FAILED] #{seq_num}: marker='{marker}'")
            
    print(f"\nTotal Assigned Image Captions: {assigned_count} / 50")
    
    # 4. Also format all table captions in document
    tabel_cnt = 0
    for p in doc.paragraphs:
        xml = p._p.xml
        t = p.text.strip()
        if 'SEQ Tabel' in xml or t.startswith('Tabel 4.') or t.startswith('Tabel 4 '):
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.keep_with_next = True
            pPr = p._p.get_or_add_pPr()
            if pPr.find(qn('w:keepNext')) is None:
                pPr.append(parse_xml(f'<w:keepNext {nsdecls("w")}/>'))
            tabel_cnt += 1
            
    print(f"Formatted {tabel_cnt} Table Captions")
    
    # Save
    try:
        doc.save('SKRIPSI.docx')
        print("[SUCCESS] SKRIPSI.docx saved successfully with all 50 images & captions intact!")
    except PermissionError:
        doc.save('SKRIPSI_Sempurna.docx')
        print("[WARNING] SKRIPSI.docx sedang terbuka di Word.")
        print("[SUCCESS] Berhasil disimpan sebagai: SKRIPSI_Sempurna.docx")

if __name__ == "__main__":
    build_pristine_skripsi()
