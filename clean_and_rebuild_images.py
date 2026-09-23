import docx
from lxml import etree
from docx.oxml.ns import nsdecls, qn
from docx.oxml import parse_xml, OxmlElement
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH

def set_caption(p, seq_num, desc_text):
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
    
    # Bold prefix
    r1 = p.add_run("Gambar 4.")
    r1.font.name = 'Times New Roman'
    r1.font.size = Pt(12)
    r1.font.bold = True
    
    # SEQ field
    fld_xml = '''
        <w:fldSimple %s w:instr=" SEQ Gambar \\* ARABIC ">
            <w:r>
                <w:rPr>
                    <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/>
                    <w:b/>
                    <w:sz w:val="24"/>
                </w:rPr>
                <w:t>%d</w:t>
            </w:r>
        </w:fldSimple>
    ''' % (nsdecls("w"), seq_num)
    p._p.append(parse_xml(fld_xml))
    
    # Regular desc
    r2 = p.add_run(f" {desc_text}")
    r2.font.name = 'Times New Roman'
    r2.font.size = Pt(12)
    r2.font.bold = False

def clean_and_rebuild_all_images():
    doc = docx.Document('SKRIPSI.docx')
    body = doc._body._body
    
    target_captions = [
        "Arsitektur Sistem Usulan",
        "Use Case Diagram",
        "Activity Diagram Login",
        "Activity Diagram Mengelola Data Pengguna",
        "Activity Diagram Mengelola Data Guru",
        "Activity Diagram Mengelola Kriteria dan Bobot",
        "Activity Diagram Mengelola Skala Penilaian",
        "Activity Diagram Mengelola Periode Penilaian",
        "Activity Diagram Melakukan Penilaian Kinerja Guru",
        "Activity Diagram Mencatat Hasil Penilaian",
        "Activity Diagram Mengolah Penilaian dengan MOORA",
        "Activity Diagram Melihat Pemeringkatan MOORA",
        "Activity Diagram Melihat Hasil Penilaian",
        "Activity Diagram Melihat Detail Penilaian",
        "Activity Diagram Monitoring Kinerja Guru",
        "Activity Diagram Melihat Riwayat Penilaian",
        "Activity Diagram Mencetak Laporan Penilaian",
        "Sequence Diagram Login",
        "Sequence Diagram Mengelola Data Pengguna",
        "Sequence Diagram Mengelola Data Guru",
        "Sequence Diagram Mengelola Kriteria dan Bobot",
        "Sequence Diagram Mengelola Skala Penilaian",
        "Sequence Diagram Mengelola Periode Penilaian",
        "Sequence Diagram Melakukan Penilaian Kinerja Guru",
        "Sequence Diagram Mencatat Hasil Penilaian",
        "Sequence Diagram Mengolah Penilaian dengan MOORA",
        "Sequence Diagram Melihat Pemeringkatan MOORA",
        "Sequence Diagram Melihat Hasil Penilaian",
        "Sequence Diagram Melihat Detail Penilaian",
        "Sequence Diagram Monitoring Kinerja Guru",
        "Sequence Diagram Melihat Riwayat Penilaian",
        "Sequence Diagram Mencetak Laporan Penilaian",
        "Class Diagram Sistem Pendukung Keputusan MOORA",
        "Entity Relationship Diagram (ERD)",
        "Struktur Menu Administrator",
        "Struktur Menu Kepala Sekolah",
        "Struktur Menu Guru",
        "Rancangan Antarmuka Halaman Login",
        "Rancangan Antarmuka Dashboard Administrator",
        "Rancangan Antarmuka Kelola Data Guru",
        "Rancangan Antarmuka Kelola Kriteria & Bobot",
        "Rancangan Antarmuka Kelola Skala Penilaian / Rubrik",
        "Rancangan Antarmuka Kelola Periode Penilaian",
        "Rancangan Antarmuka Form Transaksi Penilaian Kinerja Guru",
        "Rancangan Antarmuka Proses Perhitungan SPK MOORA",
        "Rancangan Antarmuka Peringkat & Hasil Ranking Guru",
        "Rancangan Antarmuka Laporan & Cetak Rekapitulasi",
        "Rancangan Antarmuka Kelola Akun Pengguna / User",
        "Rancangan Antarmuka Dashboard & Profil Mandiri Guru",
        "Flowchart Proses Komputasi Algoritma Metode MOORA",
    ]
    
    # 1. Remove ALL existing "Gambar 4." captions in BAB IV (after element 750)
    for elem in list(body):
        tag = elem.tag.split('}')[-1]
        if tag == 'p':
            p_obj = docx.text.paragraph.Paragraph(elem, doc)
            t = p_obj.text.strip()
            xml_s = etree.tostring(elem).decode('utf-8', errors='ignore')
            if 'w:drawing' not in xml_s and 'w:pict' not in xml_s:
                if t.startswith("Gambar 4.") or t.startswith("Gambar 4 ") or "SEQ Gambar" in xml_s:
                    elem.getparent().remove(elem)
                    
    # 2. Find all drawings in BAB IV
    drawings = []
    for elem in list(body):
        xml_s = etree.tostring(elem).decode('utf-8', errors='ignore')
        if 'w:drawing' in xml_s or 'w:pict' in xml_s:
            # check if it is BAB IV (after element 700)
            # Find its index in body
            idx = list(body).index(elem)
            if idx > 700:
                drawings.append(elem)
                
    print(f"Total drawings found in BAB IV: {len(drawings)} (Expected: {len(target_captions)})")
    
    # 3. Add one caption right after each drawing
    for i, (drawing, desc) in enumerate(zip(drawings, target_captions), start=1):
        new_p = OxmlElement('w:p')
        drawing.addnext(new_p)
        para = docx.text.paragraph.Paragraph(new_p, doc)
        set_caption(para, i, desc)
        print(f"[OK] Gambar 4.{i} {desc}")
        
    doc.save('SKRIPSI.docx')
    print("[SUCCESS] SKRIPSI.docx saved with perfectly clean 50 sequential image captions!")

if __name__ == "__main__":
    clean_and_rebuild_all_images()
