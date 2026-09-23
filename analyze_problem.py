"""
Script ini hanya memperbaiki style caption Tabel 4.3 di SKRIPSI.docx
tanpa menghapus atau mengubah konten apapun.

Masalah: Elemen [802] di SKRIPSI.docx adalah Tabel 4.3 tapi pakai style Heading3.
Ini karena script sebelumnya mengubah heading 'Identifikasi Aktor' menjadi caption Tabel 4.3,
sehingga heading dan paragraf penjelasan sebelumnya hilang.

Solusi terbaik: Restore dari SKRIPSI_Sempurna.docx dan lakukan perbaikan caption yang benar.
"""
import shutil
import docx
from lxml import etree
from docx.oxml.ns import qn

# Step 1: Backup SKRIPSI.docx saat ini
print("Membuat backup SKRIPSI.docx...")
shutil.copy('SKRIPSI.docx', 'SKRIPSI_before_fix_tabel3.docx')
print("Backup dibuat: SKRIPSI_before_fix_tabel3.docx")

# Step 2: Cek kondisi SKRIPSI_Sempurna.docx di area BAB IV
doc_sempurna = docx.Document('SKRIPSI_Sempurna.docx')
body_sempurna = list(doc_sempurna._body._body)
print(f"\nSKRIPSI_Sempurna.docx: {len(body_sempurna)} body elements")

# Step 3: Cek kondisi SKRIPSI.docx di area BAB IV  
doc_current = docx.Document('SKRIPSI.docx')
body_current = list(doc_current._body._body)
print(f"SKRIPSI.docx: {len(body_current)} body elements")

# SKRIPSI_Sempurna: BAB IV di [784], total 1264
# SKRIPSI.docx: BAB IV di [784], total 1245
# Perbedaan: 1264 - 1245 = 19 elemen lebih sedikit di SKRIPSI.docx

# Elemen yang hilang di SKRIPSI.docx dari backup:
# Sempurna[790] H3 "Kebutuhan Perangkat Keras" -> hilang di current
# Sempurna[791] P "Kebutuhan perangkat keras merupakan..." -> hilang di current
# Sempurna[794] H3 "Kebutuhan Perangkat Lunak" -> hilang di current
# Sempurna[795] P "Kebutuhan perangkat lunak merupakan..." -> hilang di current
# Sempurna[800] H3 "Arsitektur Sistem Usulan" -> ada di current
# Sempurna[806] H3 "Identifikasi Aktor" -> DIGABUNG jadi caption di current
# Sempurna[807] P "Identifikasi aktor digunakan..." -> hilang di current
# Sempurna[815] H3 "Deskripsi Use Case Diagram" -> hilang di current

print("\n=== Memeriksa perbedaan elemen ===")
# Mapping:
# Sempurna idx -> Current idx, keterangan
diffs = [
    (790, None, "H3 'Kebutuhan Perangkat Keras' (HILANG di current)"),
    (791, None, "P  'Kebutuhan perangkat keras...' (HILANG di current)"),
    (794, None, "H3 'Kebutuhan Perangkat Lunak' (HILANG di current)"),
    (795, None, "P  'Kebutuhan perangkat lunak...' (HILANG di current)"),
    (806, 802, "H3 'Identifikasi Aktor' -> jadi caption Tabel 4.3 (style Heading3!)"),
    (807, None, "P  'Identifikasi aktor digunakan...' (HILANG di current)"),
    (815, None, "H3 'Deskripsi Use Case Diagram' (HILANG di current)"),
    (816, None, "P  'Berdasarkan kebutuhan fungsional...' (HILANG di current)"),
]

for sempurna_idx, current_idx, desc in diffs:
    elem_s = body_sempurna[sempurna_idx]
    text_s = ''.join(t.text or '' for t in elem_s.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t'))
    print(f"  Sempurna[{sempurna_idx}]: {desc}")
    print(f"    text: {repr(text_s[:80])}")
    if current_idx:
        elem_c = body_current[current_idx]
        text_c = ''.join(t.text or '' for t in elem_c.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t'))
        print(f"  Current[{current_idx}]: text={repr(text_c[:80])}")
    print()

print("\nKESIMPULAN: Script sebelumnya menghapus sub-heading dan penjelasan,")
print("lalu menggunakan sub-heading sebagai caption.")
print("\nSOLUSI: Restore dari SKRIPSI_Sempurna.docx dan perbaiki caption dengan cara yang benar.")
