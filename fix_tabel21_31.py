"""
Fix style caption Tabel 4.21 - 4.31 yang menggunakan Heading3Char -> ubah ke style normal.
Juga hapus properti heading (numPr, keepNext, indent) agar tidak muncul sebagai sub-bab.
"""
import docx
from lxml import etree
from docx.oxml.ns import qn

doc = docx.Document('SKRIPSI.docx')
body_elements = list(doc._body._body)

def get_text(elem):
    return ''.join(t.text or '' for t in elem.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t'))

fixed = 0

for i, elem in enumerate(body_elements):
    if i < 784:
        continue
    tag = elem.tag.split('}')[-1]
    if tag != 'p':
        continue
    xml = etree.tostring(elem).decode('utf-8', errors='ignore')
    if 'SEQ Tabel' not in xml:
        continue
    
    text = get_text(elem)
    pPr = elem.find(qn('w:pPr'))
    if pPr is None:
        continue
    
    pStyle = pPr.find(qn('w:pStyle'))
    if pStyle is None:
        continue
    
    style_val = pStyle.get(qn('w:val'), '')
    
    # Hanya fix yang pakai Heading style
    if 'Heading' not in style_val:
        continue
    
    print(f"  Fixing elem[{i}] style={style_val!r}: {repr(text[:60])}")
    
    # 1. Hapus pStyle (hilangkan heading style)
    pPr.remove(pStyle)
    
    # 2. Hapus numPr jika ada (numbering dari heading)
    numPr = pPr.find(qn('w:numPr'))
    if numPr is not None:
        pPr.remove(numPr)
        print(f"     - Removed numPr")
    
    # 3. Hapus keepNext jika ada
    keepNext = pPr.find(qn('w:keepNext'))
    if keepNext is not None:
        pPr.remove(keepNext)
        print(f"     - Removed keepNext")
    
    # 4. Hapus indent yang berlebih (dari heading numbering)
    ind = pPr.find(qn('w:ind'))
    if ind is not None:
        pPr.remove(ind)
        print(f"     - Removed indent")
    
    # 5. Pastikan spacing 0
    spacing = pPr.find(qn('w:spacing'))
    if spacing is None:
        from docx.oxml import OxmlElement
        spacing = OxmlElement('w:spacing')
        pPr.append(spacing)
    spacing.set(qn('w:before'), '0')
    spacing.set(qn('w:after'), '0')
    
    # 6. Pastikan center alignment
    jc = pPr.find(qn('w:jc'))
    if jc is None:
        from docx.oxml import OxmlElement
        jc = OxmlElement('w:jc')
        pPr.append(jc)
    jc.set(qn('w:val'), 'center')
    
    # 7. Fix semua run agar tidak inherit heading style (pastikan font benar)
    for run in elem.findall(qn('w:r')):
        rPr = run.find(qn('w:rPr'))
        if rPr is None:
            from docx.oxml import OxmlElement
            rPr = OxmlElement('w:rPr')
            run.insert(0, rPr)
        
        # Pastikan font Times New Roman
        rFonts = rPr.find(qn('w:rFonts'))
        if rFonts is None:
            from docx.oxml import OxmlElement
            rFonts = OxmlElement('w:rFonts')
            rPr.insert(0, rFonts)
        rFonts.set(qn('w:ascii'), 'Times New Roman')
        rFonts.set(qn('w:hAnsi'), 'Times New Roman')
        
        # Pastikan size 12pt (24 half-points)
        sz = rPr.find(qn('w:sz'))
        if sz is None:
            from docx.oxml import OxmlElement
            sz = OxmlElement('w:sz')
            rPr.append(sz)
        sz.set(qn('w:val'), '24')
        
        szCs = rPr.find(qn('w:szCs'))
        if szCs is None:
            from docx.oxml import OxmlElement
            szCs = OxmlElement('w:szCs')
            rPr.append(szCs)
        szCs.set(qn('w:val'), '24')
    
    fixed += 1
    print(f"     -> FIXED")

print()
print(f"Total fixed: {fixed} captions")

# Simpan
doc.save('SKRIPSI.docx')
print("Tersimpan!")

# Verifikasi
print()
print("=== Verifikasi ===")
doc_v = docx.Document('SKRIPSI.docx')
body_v = list(doc_v._body._body)
count = 0
problems = 0
for i, elem in enumerate(body_v):
    if i < 784:
        continue
    tag = elem.tag.split('}')[-1]
    if tag != 'p':
        continue
    xml = etree.tostring(elem).decode('utf-8', errors='ignore')
    if 'SEQ Tabel' not in xml:
        continue
    
    count += 1
    text = get_text(elem)
    pPr = elem.find(qn('w:pPr'))
    style = ''
    if pPr is not None:
        pStyle = pPr.find(qn('w:pStyle'))
        if pStyle is not None:
            style = pStyle.get(qn('w:val'), '')
    
    is_heading = 'Heading' in style
    if is_heading:
        problems += 1
        print(f"  T[{count}] MASALAH style={style!r}: {repr(text[:60])}")

print()
if problems == 0:
    print(f"✅ Semua {count} caption Tabel di BAB IV sudah benar (tidak ada yang pakai Heading style)")
else:
    print(f"❌ Masih ada {problems} caption bermasalah dari total {count}")
