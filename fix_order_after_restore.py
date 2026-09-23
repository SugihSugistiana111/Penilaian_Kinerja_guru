"""
Fix urutan elemen yang salah setelah restore.

Masalah:
1. [790] P penjelasan muncul SEBELUM [791] H3 -> seharusnya SESUDAH H3
2. [794] P penjelasan muncul SEBELUM [795] H3 -> seharusnya SESUDAH H3
3. [806] P penjelasan SEBELUM [807] H3 -> seharusnya SESUDAH H3
4. [809] DUPLIKAT penjelasan Identifikasi Aktor -> hapus salah satu
5. [816] Penjelasan "Berdasarkan kebutuhan fungsional" -> adalah penjelasan awal section Deskripsi Use Case
6. [823] DUPLIKAT penjelasan Berdasarkan kebutuhan fungsional -> hapus

Urutan yang benar:
H3 -> P penjelasan -> Caption -> Tabel

Di SKRIPSI_Sempurna.docx (referensi yang benar):
[790] H3 Kebutuhan Perangkat Keras
[791] P penjelasan
[792] Caption Tabel 4.1
[793] Tabel

[794] H3 Kebutuhan Perangkat Lunak
[795] P penjelasan
[796] Caption Tabel 4.2
[797] Tabel

[806] H3 Identifikasi Aktor
[807] P penjelasan
[808] Caption Tabel 4.3
[809] Tabel

[815] H3 Deskripsi Use Case Diagram
[816] P "Berdasarkan kebutuhan fungsional..."
[817] Caption Tabel 4.4
"""
import docx
import copy
from lxml import etree
from docx.oxml.ns import qn

doc = docx.Document('SKRIPSI.docx')
body_elem = doc._body._body

def get_text(elem):
    return ''.join(t.text or '' for t in elem.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t'))

body_list = list(body_elem)

print(f"Total elements: {len(body_list)}")
print()

# Verifikasi kondisi saat ini:
print("=== Kondisi saat ini [789]-[830] ===")
for j in range(789, min(len(body_list), 830)):
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
        seq = ' [SEQ]' if 'SEQ ' in xml else ''
        print(f"  [{j}] P style={style!r}{seq}: {repr(text[:80])}")
    elif tag == 'tbl':
        rows = elem.findall('.//' + qn('w:tr'))
        print(f"  [{j}] TBL rows={len(rows)}")
    else:
        print(f"  [{j}] {tag.upper()}")

print()
print("=== MELAKUKAN PERBAIKAN ===")
print()

# Masalah 1: [790] P penjelasan ada sebelum [791] H3 Kebutuhan Perangkat Keras
# Solusi: Pindah P [790] ke sesudah H3 [791] (yaitu sebelum caption [792])
# Caranya: detach [790] dari parent, insert setelah [791]

# Refresh list setelah setiap operasi
def refresh():
    return list(doc._body._body)

# Ambil referensi elemen berdasarkan konten
def find_elem_after(body_list, text_contains, style_contains='', start=784):
    for i, elem in enumerate(body_list):
        if i < start:
            continue
        tag = elem.tag.split('}')[-1]
        if tag != 'p':
            continue
        text = get_text(elem)
        xml = etree.tostring(elem).decode('utf-8', errors='ignore')
        pPr = elem.find(qn('w:pPr'))
        style = ''
        if pPr is not None:
            pStyle = pPr.find(qn('w:pStyle'))
            if pStyle is not None:
                style = pStyle.get(qn('w:val'), '')
        if text_contains in text and style_contains in style:
            return i, elem
    return None, None

# ============================================================
# FIX 1: Urutan Kebutuhan Perangkat Keras
# Saat ini: [790] P_penjelasan, [791] H3, [792] Caption
# Target:   [790] H3, [791] P_penjelasan, [792] Caption
# ============================================================
body_list = refresh()
# Cari elemen
idx_h3_keras = None
idx_p_keras = None
for i, elem in enumerate(body_list):
    if i < 789 or i > 795:
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
    if 'Heading3' == style and 'Kebutuhan Perangkat Keras' in text:
        idx_h3_keras = i
    elif 'Kebutuhan perangkat keras merupakan' in text:
        idx_p_keras = i

print(f"H3 Kebutuhan Perangkat Keras: [{idx_h3_keras}]")
print(f"P penjelasan: [{idx_p_keras}]")

if idx_h3_keras is not None and idx_p_keras is not None and idx_p_keras < idx_h3_keras:
    print("  -> P ada sebelum H3, perlu dipindah ke sesudah H3")
    elem_p = body_list[idx_p_keras]
    elem_h3 = body_list[idx_h3_keras]
    # Detach P dari parent
    elem_p.getparent().remove(elem_p)
    # Insert P setelah H3
    elem_h3.addnext(elem_p)
    print("  -> Fix 1 selesai: P dipindah ke sesudah H3")
elif idx_h3_keras is not None and idx_p_keras is not None:
    print("  -> Urutan sudah benar (H3 sebelum P)")

print()

# ============================================================
# FIX 2: Urutan Kebutuhan Perangkat Lunak
# ============================================================
body_list = refresh()
idx_h3_lunak = None
idx_p_lunak = None
for i, elem in enumerate(body_list):
    if i < 789 or i > 802:
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
    if 'Heading3' == style and 'Kebutuhan Perangkat Lunak' in text:
        idx_h3_lunak = i
    elif 'Kebutuhan perangkat lunak merupakan' in text:
        idx_p_lunak = i

print(f"H3 Kebutuhan Perangkat Lunak: [{idx_h3_lunak}]")
print(f"P penjelasan lunak: [{idx_p_lunak}]")

if idx_h3_lunak is not None and idx_p_lunak is not None and idx_p_lunak < idx_h3_lunak:
    print("  -> P ada sebelum H3, perlu dipindah ke sesudah H3")
    elem_p = body_list[idx_p_lunak]
    elem_h3 = body_list[idx_h3_lunak]
    elem_p.getparent().remove(elem_p)
    elem_h3.addnext(elem_p)
    print("  -> Fix 2 selesai")
elif idx_h3_lunak is not None and idx_p_lunak is not None:
    print("  -> Urutan sudah benar")

print()

# ============================================================
# FIX 3: Urutan Identifikasi Aktor + hapus duplikat
# Saat ini ada duplikat P "Identifikasi aktor digunakan..." -> [806] sebelum H3 [807] dan [809] setelah tabel
# Target: H3 [807] -> P [808] -> Caption -> Tabel
# ============================================================
body_list = refresh()
idx_h3_identifikasi = None
idx_p_identifikasi_before = None  # yang ada sebelum H3 (perlu dihapus atau dipindah)
idx_p_identifikasi_after = None   # yang ada setelah tabel (duplikat - perlu dihapus)

for i, elem in enumerate(body_list):
    if i < 800 or i > 820:
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
    xml = etree.tostring(elem).decode('utf-8', errors='ignore')
    
    if 'Heading3' == style and 'Identifikasi Aktor' in text:
        idx_h3_identifikasi = i
    elif 'Identifikasi aktor digunakan' in text and 'SEQ' not in xml:
        if idx_h3_identifikasi is None:
            idx_p_identifikasi_before = i
        else:
            idx_p_identifikasi_after = i

print(f"H3 Identifikasi Aktor: [{idx_h3_identifikasi}]")
print(f"P penjelasan sebelum H3: [{idx_p_identifikasi_before}]")
print(f"P penjelasan setelah tabel (duplikat?): [{idx_p_identifikasi_after}]")

# Hapus duplikat yang setelah tabel (jika ada)
if idx_p_identifikasi_after is not None:
    elem_dup = body_list[idx_p_identifikasi_after]
    print(f"  -> Menghapus duplikat P [{idx_p_identifikasi_after}]: {repr(get_text(elem_dup)[:60])}")
    elem_dup.getparent().remove(elem_dup)
    print("  -> Duplikat dihapus")

# Pindah P sebelum H3 ke sesudah H3
body_list = refresh()
# Cari ulang setelah hapus duplikat
idx_h3_identifikasi2 = None
idx_p_identifikasi_before2 = None
for i, elem in enumerate(body_list):
    if i < 800 or i > 820:
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
    xml = etree.tostring(elem).decode('utf-8', errors='ignore')
    
    if 'Heading3' == style and 'Identifikasi Aktor' in text:
        idx_h3_identifikasi2 = i
    elif 'Identifikasi aktor digunakan' in text and 'SEQ' not in xml:
        if idx_h3_identifikasi2 is None:
            idx_p_identifikasi_before2 = i

if idx_h3_identifikasi2 is not None and idx_p_identifikasi_before2 is not None and idx_p_identifikasi_before2 < idx_h3_identifikasi2:
    print(f"  -> P [{idx_p_identifikasi_before2}] ada sebelum H3 [{idx_h3_identifikasi2}], dipindah")
    elem_p = body_list[idx_p_identifikasi_before2]
    elem_h3 = body_list[idx_h3_identifikasi2]
    elem_p.getparent().remove(elem_p)
    elem_h3.addnext(elem_p)
    print("  -> Fix 3 selesai")

print()

# ============================================================
# FIX 4: Hapus duplikat "Berdasarkan kebutuhan fungsional..." 
# yang ada di [823] (muncul dua kali setelah restore)
# ============================================================
body_list = refresh()
found_ber_keb = []
for i, elem in enumerate(body_list):
    if i < 815 or i > 840:
        continue
    tag = elem.tag.split('}')[-1]
    if tag != 'p':
        continue
    text = get_text(elem)
    if 'Berdasarkan kebutuhan fungsional yang telah ditetapkan pada Bab III' in text:
        found_ber_keb.append((i, elem))

print(f"Paragraf 'Berdasarkan kebutuhan fungsional...': ditemukan {len(found_ber_keb)} kali")
for idx, elem in found_ber_keb:
    print(f"  [{idx}]: {repr(get_text(elem)[:80])}")

if len(found_ber_keb) > 1:
    # Hapus yang pertama (yang ada sebelum H3 Deskripsi Use Case Diagram) 
    # karena yang benar adalah yang ada SETELAH H3
    # Cari H3 Deskripsi Use Case Diagram
    idx_h3_deskripsi = None
    for i, elem in enumerate(body_list):
        if i < 815 or i > 840:
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
            idx_h3_deskripsi = i
            break
    
    print(f"H3 Deskripsi Use Case Diagram: [{idx_h3_deskripsi}]")
    
    # Hapus yang ada sebelum H3 Deskripsi
    for idx, elem in found_ber_keb:
        if idx_h3_deskripsi is not None and idx < idx_h3_deskripsi:
            print(f"  -> Menghapus duplikat [{idx}]")
            elem.getparent().remove(elem)
            print("  -> Dihapus")
        elif idx_h3_deskripsi is not None and idx > idx_h3_deskripsi:
            print(f"  -> Mempertahankan [{idx}] (setelah H3)")

print()

# ============================================================
# SIMPAN
# ============================================================
print("=== MENYIMPAN DOKUMEN ===")
doc.save('SKRIPSI.docx')
print("Tersimpan!")

# ============================================================
# VERIFIKASI FINAL
# ============================================================
print()
print("=== VERIFIKASI FINAL ===")
doc_final = docx.Document('SKRIPSI.docx')
body_final = list(doc_final._body._body)
print(f"Total elements: {len(body_final)}")
print()

for j in range(784, min(len(body_final), 840)):
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
