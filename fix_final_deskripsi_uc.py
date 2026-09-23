"""
Fix terakhir: 
1. Tambahkan H3 "Deskripsi Use Case Diagram" dan P penjelasan SEBELUM Tabel 4.4
2. Hapus H3 "Deskripsi Use Case Diagram" yang ada sebelum Tabel 4.5 (sudah salah posisi)

Target struktur yang benar:
P "Berdasarkan Gambar 4.2..." [814]
H3 "Deskripsi Use Case Diagram" <- INSERT sebelum Tabel 4.4
P "Berdasarkan kebutuhan fungsional..." <- INSERT
Caption Tabel 4.4 [815]
Tabel 4.4 [816]
P penjelasan setelah Tabel 4.4 [817-820]
Caption Tabel 4.5 [822] (hapus H3 Deskripsi yang ada sebelum ini)
"""
import docx
import copy
from lxml import etree
from docx.oxml.ns import qn

doc = docx.Document('SKRIPSI.docx')
doc_sempurna = docx.Document('SKRIPSI_Sempurna.docx')

body_sempurna = list(doc_sempurna._body._body)

def get_text(elem):
    return ''.join(t.text or '' for t in elem.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t'))

# Dapatkan elemen dari backup
h3_deskripsi_uc = body_sempurna[815]   # H3 "Deskripsi Use Case Diagram" 
p_deskripsi_uc = body_sempurna[816]    # P "Berdasarkan kebutuhan fungsional..."

print(f"H3 Deskripsi: {repr(get_text(h3_deskripsi_uc)[:60])}")
print(f"P Deskripsi:  {repr(get_text(p_deskripsi_uc)[:60])}")
print()

body_current = list(doc._body._body)
print(f"Total elements: {len(body_current)}")
print()

# Cari Tabel 4.4 caption di current
def find_nth_seq_tabel(body_list, n, start=784):
    count = 0
    for i, elem in enumerate(body_list):
        if i < start:
            continue
        tag = elem.tag.split('}')[-1]
        if tag == 'p':
            xml = etree.tostring(elem).decode('utf-8', errors='ignore')
            if 'SEQ Tabel' in xml:
                count += 1
                if count == n:
                    return i, elem
    return None, None

idx_tabel44, elem_tabel44 = find_nth_seq_tabel(body_current, 4)
print(f"Tabel 4.4 di [{idx_tabel44}]: {repr(get_text(elem_tabel44)[:60])}")

# Cari H3 "Deskripsi Use Case Diagram" yang salah posisi (sebelum Tabel 4.5)
body_current = list(doc._body._body)
idx_h3_deskripsi_wrong = None
elem_h3_deskripsi_wrong = None
for i, elem in enumerate(body_current):
    if i < 815 or i > 835:
        continue
    tag = elem.tag.split('}')[-1]
    if tag != 'p':
        continue
    text = get_text(elem)
    pPr = elem.find(qn('w:pPr'))
    style = ''
    if pPr is not None:
        pStyle = pPr.find(qn('w:pStyle'))
        if pStyle is not None:
            style = pStyle.get(qn('w:val'), '')
    if 'Heading3' == style and 'Deskripsi Use Case' in text:
        idx_h3_deskripsi_wrong = i
        elem_h3_deskripsi_wrong = elem
        print(f"H3 Deskripsi salah posisi di [{i}]: {repr(text[:60])}")

print()

# Step 1: Hapus H3 "Deskripsi Use Case Diagram" yang salah posisi (sebelum Tabel 4.5)
if elem_h3_deskripsi_wrong is not None:
    print(f"  -> Menghapus H3 Deskripsi salah posisi [{idx_h3_deskripsi_wrong}]")
    elem_h3_deskripsi_wrong.getparent().remove(elem_h3_deskripsi_wrong)
    print("  -> Dihapus")

# Step 2: Insert H3 + P sebelum Tabel 4.4
body_current = list(doc._body._body)
idx_tabel44_new, elem_tabel44_new = find_nth_seq_tabel(body_current, 4)
print(f"Tabel 4.4 sekarang di [{idx_tabel44_new}]")

print(f"  -> Inserting H3 'Deskripsi Use Case Diagram' sebelum Tabel 4.4...")
elem_tabel44_new.addprevious(copy.deepcopy(p_deskripsi_uc))
elem_tabel44_new.addprevious(copy.deepcopy(h3_deskripsi_uc))
print("  -> Done!")

# Simpan
doc.save('SKRIPSI.docx')
print()
print("=== Tersimpan! ===")

# Verifikasi
print()
print("=== VERIFIKASI FINAL LENGKAP ===")
doc_final = docx.Document('SKRIPSI.docx')
body_final = list(doc_final._body._body)
print(f"Total elements: {len(body_final)}")
print()

for j in range(784, min(len(body_final), 835)):
    elem = body_final[j]
    tag = elem.tag.split('}')[-1]
    if tag == 'p':
        xml = etree.tostring(elem).decode('utf-8', errors='ignore')
        text = get_text(elem)
        pPr = elem.find(qn('w:pPr'))
        style = ''
        if pPr is not None:
            pStyle = pPr.find(qn('w:pStyle'))
            if pStyle is not None:
                style = pStyle.get(qn('w:val'), '')
        seq = ' [SEQ]' if 'SEQ ' in xml else ''
        print(f"  [{j}] P style={style!r}{seq}: {repr(text[:90])}")
    elif tag == 'tbl':
        rows = elem.findall('.//' + qn('w:tr'))
        print(f"  [{j}] TBL rows={len(rows)}")
    elif tag == 'sectPr':
        print(f"  [{j}] SECTPR")
    else:
        print(f"  [{j}] {tag.upper()}")
