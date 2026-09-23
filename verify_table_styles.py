import docx
from lxml import etree
from docx.oxml.ns import qn

doc = docx.Document('SKRIPSI.docx')
body_elements = list(doc._body._body)

def get_text(elem):
    return ''.join(t.text or '' for t in elem.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t'))

print("=== VERIFIKASI CAPTION TABEL BAB IV ===")
count = 0
for i, elem in enumerate(body_elements):
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
    outline = ''
    num = ''
    if pPr is not None:
        pStyle = pPr.find(qn('w:pStyle'))
        if pStyle is not None:
            style = pStyle.get(qn('w:val'), '')
        outline_el = pPr.find(qn('w:outlineLvl'))
        if outline_el is not None:
            outline = outline_el.get(qn('w:val'), '')
        num_el = pPr.find(qn('w:numPr'))
        if num_el is not None:
            num = 'has_numPr'
            
    is_heading = ('Heading' in style) or (outline != '') or (num != '')
    status = "[SUBBAB ERROR]" if is_heading else "[OK]"
    print(f"T[{count:02d}] {status} elem[{i}] style='{style}' outline='{outline}' num='{num}' | {text[:50]}")
