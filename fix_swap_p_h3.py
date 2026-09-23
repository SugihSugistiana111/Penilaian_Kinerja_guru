"""
Fix terakhir: Tukar urutan P [815] dan H3 [816] agar menjadi H3 -> P -> Caption
"""
import docx
from lxml import etree
from docx.oxml.ns import qn

doc = docx.Document('SKRIPSI.docx')
body_list = list(doc._body._body)

def get_text(elem):
    return ''.join(t.text or '' for t in elem.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t'))

print(f"Total elements: {len(body_list)}")
print()

# Cari P "Berdasarkan kebutuhan fungsional" yang ada sebelum H3 "Deskripsi Use Case Diagram"
# dan H3 "Deskripsi Use Case Diagram" yang ada sebelum Tabel 4.4
idx_p_ber_keb = None
idx_h3_deskripsi = None
idx_tabel44 = None

count_seq = 0
for i, elem in enumerate(body_list):
    if i < 810 or i > 830:
        continue
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
        
        if 'Berdasarkan kebutuhan fungsional yang telah ditetapkan pada Bab III' in text and idx_tabel44 is None:
            idx_p_ber_keb = i
        elif 'Heading3' in style and 'Deskripsi Use Case' in text:
            idx_h3_deskripsi = i
        elif 'SEQ Tabel' in xml and idx_tabel44 is None:
            # Tabel 4.4 = SEQ ke-4 dari BAB IV
            idx_tabel44 = i

print(f"P 'Berdasarkan kebutuhan fungsional': [{idx_p_ber_keb}]")
print(f"H3 'Deskripsi Use Case Diagram': [{idx_h3_deskripsi}]")
print(f"Caption Tabel 4.4: [{idx_tabel44}]")

print()
print("Elemen saat ini:")
for j in range(813, min(len(body_list), 820)):
    elem = body_list[j]
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
        seq = ' [SEQ]' if 'SEQ' in xml else ''
        print(f"  [{j}] P style={style!r}{seq}: {repr(text[:80])}")
    elif tag == 'tbl':
        rows = elem.findall('.//' + qn('w:tr'))
        print(f"  [{j}] TBL rows={len(rows)}")

print()

# Fix: Jika P ada sebelum H3, tukar urutan
if idx_p_ber_keb is not None and idx_h3_deskripsi is not None and idx_p_ber_keb < idx_h3_deskripsi:
    print(f"P [{idx_p_ber_keb}] ada sebelum H3 [{idx_h3_deskripsi}] -> tukar urutan")
    elem_p = body_list[idx_p_ber_keb]
    elem_h3 = body_list[idx_h3_deskripsi]
    
    # Detach P dan insert setelah H3
    elem_p.getparent().remove(elem_p)
    elem_h3.addnext(elem_p)
    print("  -> Tukar selesai")
else:
    print("Urutan sudah benar, tidak perlu fix")

print()

# Simpan
doc.save('SKRIPSI.docx')
print("Tersimpan!")

# Verifikasi final
print()
print("=== VERIFIKASI FINAL ===")
doc_v = docx.Document('SKRIPSI.docx')
body_v = list(doc_v._body._body)
print(f"Total: {len(body_v)}")

for j in range(784, min(len(body_v), 832)):
    elem = body_v[j]
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
        seq = ' [SEQ]' if 'SEQ' in xml else ''
        print(f"  [{j}] P style={style!r}{seq}: {repr(text[:85])}")
    elif tag == 'tbl':
        rows = elem.findall('.//' + qn('w:tr'))
        print(f"  [{j}] TBL rows={len(rows)}")
    elif tag == 'sectPr':
        print(f"  [{j}] SECTPR")
    else:
        print(f"  [{j}] {tag.upper()}")
