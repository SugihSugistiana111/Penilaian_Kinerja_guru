import docx
from lxml import etree
from docx.oxml.ns import qn

doc = docx.Document('SKRIPSI_Sempurna.docx')

print("=== State caption di SKRIPSI_Sempurna.docx ===")
print()

tabel_count = 0
gambar_count = 0

for i, p in enumerate(doc.paragraphs):
    xml = p._p.xml
    text = p.text.strip()
    
    if 'SEQ Tabel' in xml:
        tabel_count += 1
        print(f"  T[{tabel_count}] Para[{i}] style={p.style.name!r}: {repr(text[:80])}")
    elif 'SEQ Gambar' in xml:
        gambar_count += 1
        print(f"  G[{gambar_count}] Para[{i}] style={p.style.name!r}: {repr(text[:80])}")

print()
print(f"Total Tabel captions: {tabel_count}")
print(f"Total Gambar captions: {gambar_count}")

# Juga cek apakah ada heading yang ada di dalam caption Tabel 4.3
print()
print("=== Cek area Tabel 4.3 di SKRIPSI_Sempurna.docx ===")
body_elements = list(doc._body._body)
for j in range(800, 820):
    elem = body_elements[j]
    tag = elem.tag.split('}')[-1]
    if tag == 'p':
        xml_bytes = etree.tostring(elem)
        xml_str = xml_bytes.decode('utf-8', errors='ignore')
        text = ''.join(t.text or '' for t in elem.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t'))
        pPr = elem.find(qn('w:pPr'))
        style = ''
        if pPr is not None:
            pStyle = pPr.find(qn('w:pStyle'))
            if pStyle is not None:
                style = pStyle.get(qn('w:val'), '')
        has_seq = 'SEQ Tabel' in xml_str or 'SEQ Gambar' in xml_str
        print(f"  [{j}] P style={style!r} SEQ={has_seq} text={repr(text[:80])}")
    elif tag == 'tbl':
        rows = elem.findall('.//' + qn('w:tr'))
        print(f"  [{j}] TBL rows={len(rows)}")
