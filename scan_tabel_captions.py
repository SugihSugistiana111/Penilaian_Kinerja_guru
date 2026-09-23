import docx
from lxml import etree
from docx.oxml.ns import qn

doc = docx.Document('SKRIPSI.docx')
body_elements = list(doc._body._body)

def get_text(elem):
    return ''.join(t.text or '' for t in elem.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t'))

print(f"Total body elements: {len(body_elements)}")
print()
print("=== Scan semua caption Tabel di BAB IV ===")

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
    
    text = get_text(elem)
    pPr = elem.find(qn('w:pPr'))
    style = ''
    if pPr is not None:
        pStyle = pPr.find(qn('w:pStyle'))
        if pStyle is not None:
            style = pStyle.get(qn('w:val'), '')
    
    count += 1
    
    # Flag masalah
    is_heading = 'Heading' in style
    flag = ' <<< HEADING - MASALAH!' if is_heading else ''
    
    print(f"  T[{count}] elem[{i}] style={style!r}{flag}")
    print(f"          text={repr(text[:80])}")
