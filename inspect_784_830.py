import docx
from lxml import etree
from docx.oxml.ns import qn

doc = docx.Document('SKRIPSI.docx')
body_elements = list(doc._body._body)

print(f"Total body elements: {len(body_elements)}")
print()

# Lihat detail elemen [784] sampai [830]
print("=== Body elements [784] sampai [830] ===")
for j in range(784, min(len(body_elements), 831)):
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
        
        has_seq_tabel = 'SEQ Tabel' in xml_str
        has_seq_gambar = 'SEQ Gambar' in xml_str
        has_section = 'sectPr' in xml_str
        
        seq_info = ''
        if has_seq_tabel:
            seq_info = ' [SEQ-TABEL]'
        if has_seq_gambar:
            seq_info = ' [SEQ-GAMBAR]'
        
        print(f"  [{j}] P | style={style!r}{seq_info} | sect={has_section} | text={repr(text[:100])}")
    elif tag == 'tbl':
        rows = elem.findall('.//' + qn('w:tr'))
        first_cell_text = ''
        try:
            first_row = elem.find('.//' + qn('w:tr'))
            if first_row is not None:
                first_cell_text = ''.join(t.text or '' for t in first_row.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t'))[:80]
        except:
            pass
        print(f"  [{j}] TBL | rows={len(rows)} | first_row={repr(first_cell_text)}")
    elif tag == 'sectPr':
        print(f"  [{j}] SECTPR")
    else:
        print(f"  [{j}] {tag.upper()}")
