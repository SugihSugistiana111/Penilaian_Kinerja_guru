import docx
from lxml import etree
from docx.oxml.ns import qn

# Cek SKRIPSI_Sempurna.docx sebagai referensi
doc = docx.Document('SKRIPSI_Sempurna.docx')
body_elements = list(doc._body._body)

print(f"Total body elements in SKRIPSI_Sempurna.docx: {len(body_elements)}")
print()

# Cari BAB IV
bab4_idx = None
for i, elem in enumerate(body_elements):
    tag = elem.tag.split('}')[-1]
    if tag == 'p':
        text = ''.join(t.text or '' for t in elem.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t'))
        if 'BAB IV' in text and len(text) < 50:
            print(f"  Candidate BAB IV [{i}]: {repr(text[:80])}")
            
            pPr = elem.find(qn('w:pPr'))
            style = ''
            if pPr is not None:
                pStyle = pPr.find(qn('w:pStyle'))
                if pStyle is not None:
                    style = pStyle.get(qn('w:val'), '')
            print(f"    style={style!r}")
            
            if 'Heading' in style or 'BAB' in text:
                bab4_idx = i

print()
if bab4_idx:
    print(f"=== SKRIPSI_Sempurna.docx - Elements from [{bab4_idx}] ===")
    for j in range(bab4_idx, min(len(body_elements), bab4_idx + 60)):
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
            
            seq_info = ''
            if has_seq_tabel:
                seq_info = ' [SEQ-TABEL]'
            if has_seq_gambar:
                seq_info = ' [SEQ-GAMBAR]'
            
            print(f"  [{j}] P | style={style!r}{seq_info} | text={repr(text[:100])}")
        elif tag == 'tbl':
            rows = elem.findall('.//' + qn('w:tr'))
            first_cell_text = ''
            try:
                first_row = elem.find('.//' + qn('w:tr'))
                if first_row is not None:
                    first_cell_text = ''.join(t.text or '' for t in first_row.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t'))[:60]
            except:
                pass
            print(f"  [{j}] TBL | rows={len(rows)} | first_row={repr(first_cell_text)}")
        elif tag == 'sectPr':
            print(f"  [{j}] SECTPR")
        else:
            print(f"  [{j}] {tag.upper()}")
