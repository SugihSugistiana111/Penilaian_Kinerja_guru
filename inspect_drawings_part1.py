import docx
from lxml import etree

doc = docx.Document('SKRIPSI.docx')
body_elements = list(doc._body._body)

for i in range(750, 1086):
    elem = body_elements[i]
    xml_str = etree.tostring(elem).decode('utf-8', errors='ignore')
    if 'w:drawing' in xml_str or 'w:pict' in xml_str:
        print(f"\nDrawing at #{i}:")
        for off in range(-2, 3):
            j = i + off
            if 0 <= j < len(body_elements):
                e = body_elements[j]
                t = e.tag.split('}')[-1]
                if t == 'p':
                    p_obj = docx.text.paragraph.Paragraph(e, doc)
                    print(f"   [{j}] <p>: '{p_obj.text.strip()[:70]}'")
                elif t == 'tbl':
                    print(f"   [{j}] <tbl>")
