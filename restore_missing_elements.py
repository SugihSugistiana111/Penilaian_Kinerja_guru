"""
Script ini me-restore elemen yang hilang dari SKRIPSI_Sempurna.docx ke SKRIPSI.docx
TANPA mengubah konten yang sudah ada.

Yang dilakukan:
1. Insert kembali H3 "Kebutuhan Perangkat Keras" sebelum Tabel 4.1
2. Insert kembali P penjelasan "Kebutuhan perangkat keras merupakan..."
3. Insert kembali H3 "Kebutuhan Perangkat Lunak" sebelum Tabel 4.2
4. Insert kembali P penjelasan "Kebutuhan perangkat lunak merupakan..."
5. Fix style Tabel 4.3 dari Heading3 -> style Normal/caption
6. Insert kembali H3 "Identifikasi Aktor" SEBELUM Tabel 4.3
7. Insert kembali P penjelasan "Identifikasi aktor digunakan..."
8. Insert kembali H3 "Deskripsi Use Case Diagram"
9. Insert kembali P penjelasan "Berdasarkan kebutuhan fungsional..."

Catatan: Semua teks yang ada tetap dipertahankan, hanya menambahkan elemen yang hilang.
"""
import docx
import copy
from lxml import etree
from docx.oxml.ns import qn

# Load kedua dokumen
doc_sempurna = docx.Document('SKRIPSI_Sempurna.docx')
doc_current = docx.Document('SKRIPSI.docx')

body_sempurna = list(doc_sempurna._body._body)
body_current = list(doc_current._body._body)

print(f"SKRIPSI_Sempurna.docx: {len(body_sempurna)} elements")
print(f"SKRIPSI.docx: {len(body_current)} elements")
print()

def get_text(elem):
    return ''.join(t.text or '' for t in elem.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t'))

def insert_before(body, ref_elem, new_elem):
    """Insert new_elem before ref_elem in body"""
    ref_elem.addprevious(new_elem)

def copy_element(elem):
    """Deep copy an element"""
    return copy.deepcopy(elem)

# === STEP 1: Locate elemen di current doc ===
body_elem_current = doc_current._body._body

# Cari Tabel 4.1 caption di current (index 790 di body_elements = paragraf di dalam body)
# Tabel 4.1 = elemen [790] di body_elements
cap_tabel41 = body_current[790]  # "Tabel 4.1 Kebutuhan Perangkat Keras"
cap_tabel42 = body_current[792]  # "Tabel 4.2 Kebutuhan Perangkat Lunak"
cap_tabel43 = body_current[802]  # "Tabel 4.3 Identifikasi Aktor" (style Heading3 - SALAH)

text_41 = get_text(cap_tabel41)
text_42 = get_text(cap_tabel42)
text_43 = get_text(cap_tabel43)

print(f"Tabel 4.1 caption: {repr(text_41[:60])}")
print(f"Tabel 4.2 caption: {repr(text_42[:60])}")
print(f"Tabel 4.3 caption (style Heading3): {repr(text_43[:60])}")
print()

# === STEP 2: Get elemen dari backup ===
h3_perangkat_keras = body_sempurna[790]   # H3 "Kebutuhan Perangkat Keras"
p_perangkat_keras = body_sempurna[791]    # P "Kebutuhan perangkat keras merupakan..."
h3_perangkat_lunak = body_sempurna[794]   # H3 "Kebutuhan Perangkat Lunak"
p_perangkat_lunak = body_sempurna[795]    # P "Kebutuhan perangkat lunak merupakan..."
h3_identifikasi = body_sempurna[806]      # H3 "Identifikasi Aktor"
p_identifikasi = body_sempurna[807]       # P "Identifikasi aktor digunakan..."
h3_deskripsi_uc = body_sempurna[815]      # H3 "Deskripsi Use Case Diagram"
p_deskripsi_uc = body_sempurna[816]       # P "Berdasarkan kebutuhan fungsional..."

print("Elemen yang akan di-restore:")
print(f"  H3: {repr(get_text(h3_perangkat_keras)[:60])}")
print(f"  P:  {repr(get_text(p_perangkat_keras)[:60])}")
print(f"  H3: {repr(get_text(h3_perangkat_lunak)[:60])}")
print(f"  P:  {repr(get_text(p_perangkat_lunak)[:60])}")
print(f"  H3: {repr(get_text(h3_identifikasi)[:60])}")
print(f"  P:  {repr(get_text(p_identifikasi)[:60])}")
print(f"  H3: {repr(get_text(h3_deskripsi_uc)[:60])}")
print(f"  P:  {repr(get_text(p_deskripsi_uc)[:60])}")
print()

# === STEP 3: Insert elemen ===
# PENTING: Insert dari bawah ke atas agar index tidak bergeser!

# 3a. Fix style Tabel 4.3 (ubah Heading3 -> Normal/None)
print("Fixing Tabel 4.3 style...")
pPr_43 = cap_tabel43.find(qn('w:pPr'))
if pPr_43 is not None:
    pStyle = pPr_43.find(qn('w:pStyle'))
    if pStyle is not None:
        # Hapus pStyle Heading3
        pPr_43.remove(pStyle)
        print("  - Removed Heading3 style from Tabel 4.3 caption")
    
    # Juga hapus numPr jika ada (numbering dari heading)
    numPr = pPr_43.find(qn('w:numPr'))
    if numPr is not None:
        pPr_43.remove(numPr)
        print("  - Removed numPr from Tabel 4.3 caption")
    
    # Hapus keepNext jika ada
    keepNext = pPr_43.find(qn('w:keepNext'))
    if keepNext is not None:
        pPr_43.remove(keepNext)
        print("  - Removed keepNext from Tabel 4.3 caption")
    
    # Update indentation dan justification
    ind = pPr_43.find(qn('w:ind'))
    if ind is not None:
        pPr_43.remove(ind)
        print("  - Removed indent from Tabel 4.3 caption")

print()

# 3b. Sekarang tentukan posisi yang tepat untuk insert
# Kita perlu cari elemen-elemen berdasarkan teks, bukan index tetap (karena setelah insert index bergeser)

# Cari Tabel 4.3 caption di body_elem_current
def find_elem_by_text(body_elem, search_text, elem_type='p', after_idx=0):
    for i, child in enumerate(body_elem):
        if i < after_idx:
            continue
        tag = child.tag.split('}')[-1]
        if tag == elem_type:
            text = get_text(child)
            if search_text in text:
                return i, child
    return None, None

# Cari Tabel 4.3 caption dengan SEQ Tabel
def find_seq_elem(body_elem, seq_type, nth=0, after_idx=0):
    count = 0
    for i, child in enumerate(body_elem):
        if i < after_idx:
            continue
        tag = child.tag.split('}')[-1]
        if tag == 'p':
            xml_str = etree.tostring(child).decode('utf-8', errors='ignore')
            if f'SEQ {seq_type}' in xml_str:
                if count == nth:
                    return i, child
                count += 1
    return None, None

# Refresh body_current setelah modifikasi
body_current_fresh = list(doc_current._body._body)
print(f"Elements setelah fix style: {len(body_current_fresh)}")
print()

# Cari Tabel 4.1 caption (yang pertama SEQ Tabel di BAB IV)
# BAB IV ada di element 784
bab4_start = 784
seq_in_bab4 = 0
tabel41_idx = None
tabel42_idx = None
tabel43_idx = None

for i, child in enumerate(body_current_fresh):
    if i < bab4_start:
        continue
    tag = child.tag.split('}')[-1]
    if tag == 'p':
        xml_str = etree.tostring(child).decode('utf-8', errors='ignore')
        if 'SEQ Tabel' in xml_str:
            text = get_text(child)
            seq_in_bab4 += 1
            if seq_in_bab4 == 1:
                tabel41_idx = i
                print(f"  Tabel 4.1 at [{i}]: {repr(text[:60])}")
            elif seq_in_bab4 == 2:
                tabel42_idx = i
                print(f"  Tabel 4.2 at [{i}]: {repr(text[:60])}")
            elif seq_in_bab4 == 3:
                tabel43_idx = i
                print(f"  Tabel 4.3 at [{i}]: {repr(text[:60])}")
            elif seq_in_bab4 == 4:
                print(f"  Tabel 4.4 at [{i}]: {repr(text[:60])}")
                break

# Juga cari H3 "Deskripsi Use Case Diagram" and penjelasannya
# Di current, setelah Tabel 4.5 ada heading Skenario Use Case
# Kita perlu tahu apa yang ada setelah Tabel 4.4 sebelum Tabel 4.5

print()
print("=== Elemen antara Tabel 4.4 dan Tabel 4.5 di SKRIPSI.docx ===")
in_range = False
count_seq = 0
for i, child in enumerate(body_current_fresh):
    if i < bab4_start:
        continue
    tag = child.tag.split('}')[-1]
    if tag == 'p':
        xml_str = etree.tostring(child).decode('utf-8', errors='ignore')
        text = get_text(child)
        if 'SEQ Tabel' in xml_str:
            count_seq += 1
            if count_seq == 4:
                in_range = True
                print(f"  [{i}] START: {repr(text[:60])}")
            elif count_seq == 5:
                in_range = False
                print(f"  [{i}] END: {repr(text[:60])}")
                break
        elif in_range:
            pPr = child.find(qn('w:pPr'))
            style = ''
            if pPr is not None:
                pStyle = pPr.find(qn('w:pStyle'))
                if pStyle is not None:
                    style = pStyle.get(qn('w:val'), '')
            print(f"  [{i}] P style={style!r}: {repr(text[:80])}")
    elif in_range and tag == 'tbl':
        rows = child.findall('.//' + qn('w:tr'))
        print(f"  [{i}] TBL rows={len(rows)}")

print()
print("=== STEP 3: Melakukan insert elemen dari backup ===")

# PENTING: Insert dari BAWAH ke ATAS agar index tidak bergeser

# Pertama cari Tabel 4.5 (SEQ ke-5 di BAB IV) untuk mengetahui di mana insert H3 Deskripsi Use Case
# Di current, setelah fix: Tabel 4.4 ada dan langsung diikuti Tabel 4.5 tanpa heading "Deskripsi Use Case Diagram"

# Refresh lagi
body_current_fresh2 = list(doc_current._body._body)

# Find Tabel 4.4 index
count4 = 0
tabel44_idx = None
tabel45_idx = None
for i, child in enumerate(body_current_fresh2):
    if i < bab4_start:
        continue
    tag = child.tag.split('}')[-1]
    if tag == 'p':
        xml_str = etree.tostring(child).decode('utf-8', errors='ignore')
        if 'SEQ Tabel' in xml_str:
            count4 += 1
            if count4 == 4:
                tabel44_idx = i
            elif count4 == 5:
                tabel45_idx = i
                break

print(f"Tabel 4.4 di index [{tabel44_idx}], Tabel 4.5 di index [{tabel45_idx}]")

# Juga cari Tabel 4.3 dan Tabel 4.1 lagi dari fresh list
count3 = 0
tabel41_fresh = None
tabel42_fresh = None  
tabel43_fresh = None
for i, child in enumerate(body_current_fresh2):
    if i < bab4_start:
        continue
    tag = child.tag.split('}')[-1]
    if tag == 'p':
        xml_str = etree.tostring(child).decode('utf-8', errors='ignore')
        if 'SEQ Tabel' in xml_str:
            count3 += 1
            if count3 == 1:
                tabel41_fresh = i
            elif count3 == 2:
                tabel42_fresh = i
            elif count3 == 3:
                tabel43_fresh = i
                break

print(f"Tabel 4.1: [{tabel41_fresh}], Tabel 4.2: [{tabel42_fresh}], Tabel 4.3: [{tabel43_fresh}]")
print()

# Dapatkan referensi elemen untuk insert
elem_tabel41 = body_current_fresh2[tabel41_fresh]
elem_tabel42 = body_current_fresh2[tabel42_fresh]
elem_tabel43 = body_current_fresh2[tabel43_fresh]
elem_tabel45 = body_current_fresh2[tabel45_idx]

# INSERT dari bawah ke atas!

# 1. Insert H3 "Deskripsi Use Case Diagram" dan P penjelasan SEBELUM Tabel 4.5
print("Inserting H3 'Deskripsi Use Case Diagram' before Tabel 4.5...")
elem_tabel45.addprevious(copy_element(p_deskripsi_uc))
elem_tabel45.addprevious(copy_element(h3_deskripsi_uc))
print("  Done!")

# 2. Insert H3 "Identifikasi Aktor" dan P penjelasan SEBELUM Tabel 4.3
print("Inserting H3 'Identifikasi Aktor' and P before Tabel 4.3...")
elem_tabel43.addprevious(copy_element(p_identifikasi))
elem_tabel43.addprevious(copy_element(h3_identifikasi))
print("  Done!")

# 3. Insert H3 "Kebutuhan Perangkat Lunak" dan P penjelasan SEBELUM Tabel 4.2
print("Inserting H3 'Kebutuhan Perangkat Lunak' and P before Tabel 4.2...")
elem_tabel42.addprevious(copy_element(p_perangkat_lunak))
elem_tabel42.addprevious(copy_element(h3_perangkat_lunak))
print("  Done!")

# 4. Insert H3 "Kebutuhan Perangkat Keras" dan P penjelasan SEBELUM Tabel 4.1
print("Inserting H3 'Kebutuhan Perangkat Keras' and P before Tabel 4.1...")
elem_tabel41.addprevious(copy_element(p_perangkat_keras))
elem_tabel41.addprevious(copy_element(h3_perangkat_keras))
print("  Done!")

# === STEP 4: Simpan ===
print()
print("Menyimpan dokumen...")
doc_current.save('SKRIPSI.docx')
print("SELESAI! SKRIPSI.docx telah di-update.")

# Verifikasi
print()
print("=== Verifikasi ===")
doc_verify = docx.Document('SKRIPSI.docx')
body_verify = list(doc_verify._body._body)
print(f"Total elements: {len(body_verify)} (sebelumnya: 1245, diharapkan: ~1264)")

# Cek area BAB IV
count_v = 0
for i, child in enumerate(body_verify):
    if i < bab4_start:
        continue
    tag = child.tag.split('}')[-1]
    if tag == 'p':
        xml_str = etree.tostring(child).decode('utf-8', errors='ignore')
        text = get_text(child)
        pPr = child.find(qn('w:pPr'))
        style = ''
        if pPr is not None:
            pStyle = pPr.find(qn('w:pStyle'))
            if pStyle is not None:
                style = pStyle.get(qn('w:val'), '')
        
        if 'SEQ Tabel' in xml_str:
            count_v += 1
            print(f"  T[{count_v}] [{i}] style={style!r}: {repr(text[:70])}")
            if count_v > 5:
                break
        elif 'Kebutuhan Perangkat' in text or 'Identifikasi Aktor' in text or 'Deskripsi Use Case' in text:
            if not 'SEQ' in xml_str:
                print(f"  H [{i}] style={style!r}: {repr(text[:70])}")
