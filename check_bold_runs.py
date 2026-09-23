import docx
from lxml import etree
from docx.oxml.ns import qn

doc = docx.Document('SKRIPSI.docx')
body_elements = list(doc._body._body)

def get_text(elem):
    return ''.join(t.text or '' for t in elem.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t'))

print("=== VERIFIKASI BOLD / NON-BOLD RUNS PADA TABEL BAB IV ===")
for i in range(1030, 1070):
    if i >= len(body_elements):
        break
    elem = body_elements[i]
    if elem.tag.split('}')[-1] != 'p':
        continue
    xml = etree.tostring(elem).decode('utf-8', errors='ignore')
    if 'SEQ Tabel' not in xml:
        continue
    
    text = get_text(elem)
    runs_info = []
    for r in elem.findall(qn('w:r')):
        r_text = ''.join(t.text or '' for t in r.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t'))
        rPr = r.find(qn('w:rPr'))
        is_bold = False
        if rPr is not None:
            b_el = rPr.find(qn('w:b'))
            if b_el is not None and b_el.get(qn('w:val'), 'true') not in ['0', 'false']:
                is_bold = True
        runs_info.append(f"['{r_text}', bold={is_bold}]")
    print(f"Elem {i}: {' + '.join(runs_info)}")
