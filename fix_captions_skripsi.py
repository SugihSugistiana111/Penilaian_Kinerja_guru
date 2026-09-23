import docx
import re
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def make_seq_caption_paragraph(p, label_type, seq_num, description_text):
    """
    Membuat caption otomatis Word SEQ di paragraph p.
    label_type: "Tabel" atau "Gambar"
    seq_num: nomor urut untuk placeholder (1, 2, 3, ...)
    description_text: teks keterangan setelah nomor
    
    Format: "Tabel 4.X Keterangan" atau "Gambar 4.X Keterangan"
    - "Tabel 4.X" / "Gambar 4.X" = BOLD
    - " Keterangan" = NOT BOLD
    - Font: Times New Roman 12pt
    - Alignment: Center
    """
    # Clear existing runs
    for run in p.runs:
        run._r.getparent().remove(run._r)
    # Also clear any existing field codes
    for child in list(p._p):
        tag = child.tag.split('}')[-1] if '}' in child.tag else child.tag
        if tag in ('r', 'fldSimple', 'hyperlink'):
            p._p.remove(child)
    
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(6)
    
    # Run 1: "Tabel 4." or "Gambar 4." (BOLD)
    r1 = p.add_run(f"{label_type} 4.")
    r1.font.name = 'Times New Roman'
    r1.font.size = Pt(12)
    r1.font.bold = True
    
    # SEQ field (BOLD) - for Word auto-numbering
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
    ''' % (nsdecls("w"), label_type, seq_num)
    p._p.append(parse_xml(fld_xml))
    
    # Run 2: " Keterangan" (NOT BOLD)
    r2 = p.add_run(f" {description_text}")
    r2.font.name = 'Times New Roman'
    r2.font.size = Pt(12)
    r2.font.bold = False

def insert_caption_before(target_p, label_type, seq_num, description_text):
    """Insert a new caption paragraph BEFORE target_p"""
    new_p = OxmlElement('w:p')
    target_p._p.addprevious(new_p)
    new_para = docx.text.paragraph.Paragraph(new_p, target_p._parent)
    make_seq_caption_paragraph(new_para, label_type, seq_num, description_text)
    return new_para

def insert_caption_after(target_p, label_type, seq_num, description_text):
    """Insert a new caption paragraph AFTER target_p"""
    new_p = OxmlElement('w:p')
    target_p._p.addnext(new_p)
    new_para = docx.text.paragraph.Paragraph(new_p, target_p._parent)
    make_seq_caption_paragraph(new_para, label_type, seq_num, description_text)
    return new_para


def fix_captions():
    doc = docx.Document('SKRIPSI.docx')
    paragraphs = doc.paragraphs
    
    # =========================================================================
    # STEP 1: Collect all existing Tabel/Gambar caption paragraphs in BAB IV
    # and their descriptions, then remove them
    # =========================================================================
    
    # Maps: paragraph index -> (type, description)
    # We'll find the captions, extract their text, remove them, then re-insert with SEQ
    
    tabel_captions = []   # list of (paragraph_index, description_text, context)
    gambar_captions = []  # list of (paragraph_index, description_text, context)
    
    # Patterns for existing captions
    tabel_pattern = re.compile(r'^Tabel\s+4[\.\s]*(\d+)\s+(.*)', re.IGNORECASE)
    gambar_pattern = re.compile(r'^Gambar\s+4[\.\s]*(\d+)\s+(.*)', re.IGNORECASE)
    
    caption_indices_to_remove = []
    
    for i, p in enumerate(paragraphs):
        t = p.text.strip()
        
        m_tabel = tabel_pattern.match(t)
        if m_tabel:
            desc = m_tabel.group(2).strip()
            tabel_captions.append((i, desc))
            caption_indices_to_remove.append(i)
            continue
            
        m_gambar = gambar_pattern.match(t)
        if m_gambar:
            desc = m_gambar.group(2).strip()
            gambar_captions.append((i, desc))
            caption_indices_to_remove.append(i)
            continue
    
    print(f"Found {len(tabel_captions)} Tabel captions and {len(gambar_captions)} Gambar captions")
    
    for idx, desc in tabel_captions:
        print(f"  Tabel P{idx}: {desc[:80]}")
    for idx, desc in gambar_captions:
        print(f"  Gambar P{idx}: {desc[:80]}")
    
    # =========================================================================
    # STEP 2: Replace each existing caption paragraph in-place with proper SEQ
    # =========================================================================
    
    tabel_counter = 0
    gambar_counter = 0
    
    for i, p in enumerate(paragraphs):
        t = p.text.strip()
        
        m_tabel = tabel_pattern.match(t)
        if m_tabel:
            tabel_counter += 1
            desc = m_tabel.group(2).strip()
            make_seq_caption_paragraph(p, "Tabel", tabel_counter, desc)
            print(f"[OK] Tabel 4.{tabel_counter} {desc[:60]}")
            continue
        
        m_gambar = gambar_pattern.match(t)
        if m_gambar:
            gambar_counter += 1
            desc = m_gambar.group(2).strip()
            make_seq_caption_paragraph(p, "Gambar", gambar_counter, desc)
            print(f"[OK] Gambar 4.{gambar_counter} {desc[:60]}")
            continue
    
    # =========================================================================
    # STEP 3: Handle Activity Diagram captions (AD-01 to AD-15)
    # These currently have title like "AD-01\tLogin" + image but NO Gambar caption
    # We need to ADD "Gambar 4.X Activity Diagram Login" AFTER each image
    # =========================================================================
    
    ad_names = {
        "AD-01": "Activity Diagram Login",
        "AD-02": "Activity Diagram Mengelola Data Pengguna",
        "AD-03": "Activity Diagram Mengelola Data Guru",
        "AD-04": "Activity Diagram Mengelola Kriteria dan Bobot",
        "AD-05": "Activity Diagram Mengelola Skala Penilaian",
        "AD-06": "Activity Diagram Mengelola Periode Penilaian",
        "AD-07": "Activity Diagram Melakukan Penilaian Kinerja Guru",
        "AD-08": "Activity Diagram Mencatat Hasil Penilaian",
        "AD-09": "Activity Diagram Mengolah Penilaian dengan MOORA",
        "AD-10": "Activity Diagram Melihat Pemeringkatan MOORA",
        "AD-11": "Activity Diagram Melihat Hasil Penilaian",
        "AD-12": "Activity Diagram Melihat Detail Penilaian",
        "AD-13": "Activity Diagram Monitoring Kinerja Guru",
        "AD-14": "Activity Diagram Melihat Riwayat Penilaian",
        "AD-15": "Activity Diagram Mencetak Laporan Penilaian",
    }
    
    sd_names = {
        "SD-01": "Sequence Diagram Login",
        "SD-02": "Sequence Diagram Mengelola Data Pengguna",
        "SD-03": "Sequence Diagram Mengelola Data Guru",
        "SD-04": "Sequence Diagram Mengelola Kriteria dan Bobot",
        "SD-05": "Sequence Diagram Mengelola Skala Penilaian",
        "SD-06": "Sequence Diagram Mengelola Periode Penilaian",
        "SD-07": "Sequence Diagram Melakukan Penilaian Kinerja Guru",
        "SD-08": "Sequence Diagram Mencatat Hasil Penilaian",
        "SD-09": "Sequence Diagram Mengolah Penilaian dengan MOORA",
        "SD-10": "Sequence Diagram Melihat Pemeringkatan MOORA",
        "SD-11": "Sequence Diagram Melihat Hasil Penilaian",
        "SD-12": "Sequence Diagram Melihat Detail Penilaian",
        "SD-13": "Sequence Diagram Monitoring Kinerja Guru",
        "SD-14": "Sequence Diagram Melihat Riwayat Penilaian",
        "SD-15": "Sequence Diagram Mencetak Laporan Penilaian",
    }
    
    # Re-read paragraphs after in-place edits
    paragraphs = doc.paragraphs
    
    for i in range(len(paragraphs)):
        p = paragraphs[i]
        t = p.text.strip()
        
        # Check AD titles
        for ad_key, ad_name in ad_names.items():
            if t.startswith(ad_key):
                # Find the image paragraph (should be 2 paragraphs ahead: title -> explanation -> image)
                for offset in range(1, 4):
                    if i + offset < len(paragraphs):
                        next_p = paragraphs[i + offset]
                        if 'w:drawing' in next_p._p.xml:
                            gambar_counter += 1
                            insert_caption_after(next_p, "Gambar", gambar_counter, ad_name)
                            print(f"[NEW] Gambar 4.{gambar_counter} {ad_name} (after AD image)")
                            break
                break
        
        # Check SD titles
        for sd_key, sd_name in sd_names.items():
            if t.startswith(sd_key):
                for offset in range(1, 4):
                    if i + offset < len(paragraphs):
                        next_p = paragraphs[i + offset]
                        if 'w:drawing' in next_p._p.xml:
                            gambar_counter += 1
                            insert_caption_after(next_p, "Gambar", gambar_counter, sd_name)
                            print(f"[NEW] Gambar 4.{gambar_counter} {sd_name} (after SD image)")
                            break
                break
    
    # =========================================================================
    # STEP 4: Handle standalone images that already have captions nearby
    # (Arsitektur, Use Case, ERD, Class Diagram, Wireframes, Flowchart)
    # These were already handled in Step 2 above
    # =========================================================================
    
    # Also handle images near P933 (Class Diagram), P936 (ERD), and others
    # that might not have "Gambar" prefix captions yet
    # Check for uncaptioned standalone images
    paragraphs = doc.paragraphs
    
    # Find images around P760 (Arsitektur), P933 (Class), P936 (ERD), P982-988 (wireframe extras)
    # P760 = Arsitektur Sistem -> already has "Gambar 4. 1 Arsitektur Sistem Usulan"
    # P933 = Class Diagram image (no caption found)
    # P936 = ERD image (no caption found)
    
    # Check specific uncaptioned images
    uncaptioned_images = []
    for i in range(len(paragraphs)):
        p = paragraphs[i]
        if 'w:drawing' in p._p.xml and p.text.strip() == '':
            # Check if next or prev paragraph is already a Gambar caption
            has_caption = False
            for offset in [-1, 1]:
                j = i + offset
                if 0 <= j < len(paragraphs):
                    neighbor = paragraphs[j].text.strip()
                    if neighbor.startswith('Gambar') or neighbor.startswith('AD-') or neighbor.startswith('SD-'):
                        has_caption = True
                        break
                    # Check if neighbor has SEQ Gambar field
                    if 'SEQ Gambar' in paragraphs[j]._p.xml:
                        has_caption = True
                        break
            if not has_caption:
                uncaptioned_images.append(i)
    
    if uncaptioned_images:
        print(f"\n[INFO] Found {len(uncaptioned_images)} uncaptioned images at: {uncaptioned_images}")
        # These are likely Class Diagram and ERD
        # We need to check context to assign proper captions
        for idx in uncaptioned_images:
            # Check surrounding paragraphs for context
            for offset in range(-3, 4):
                j = idx + offset
                if 0 <= j < len(paragraphs):
                    t = paragraphs[j].text.strip()
                    if t:
                        print(f"  Context P{j}: {t[:80]}")
    
    print(f"\nFinal counts: {tabel_counter} Tabel captions, {gambar_counter} Gambar captions")
    
    # Save
    try:
        doc.save('SKRIPSI.docx')
        print("[SUCCESS] SKRIPSI.docx berhasil diperbarui!")
    except PermissionError:
        doc.save('SKRIPSI_Captions.docx')
        print("[WARNING] SKRIPSI.docx sedang dibuka. Disimpan sebagai SKRIPSI_Captions.docx")

if __name__ == "__main__":
    fix_captions()
