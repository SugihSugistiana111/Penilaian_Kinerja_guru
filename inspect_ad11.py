import docx
from lxml import etree

doc = docx.Document('SKRIPSI.docx')
body = doc._body._body

print("Inspect elements around AD-10 to AD-13:")
for i, elem in enumerate(body):
    if elem.tag.endswith('p'):
        p = docx.text.paragraph.Paragraph(elem, doc)
        txt = p.text.strip()
        has_draw = 'w:drawing' in etree.tostring(elem).decode('utf-8', errors='ignore') or 'w:pict' in etree.tostring(elem).decode('utf-8', errors='ignore')
        if any(k in txt for k in ['AD-09', 'AD-10', 'AD-11', 'AD-12', 'AD-13', 'AD-14', 'Melihat Hasil Penilaian', 'Melihat Detail Penilaian']):
            print(f"[{i}] <p> (draw={has_draw}): '{txt[:70]}'")
    elif elem.tag.endswith('tbl'):
        pass
