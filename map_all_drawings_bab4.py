import docx
from lxml import etree

doc = docx.Document('SKRIPSI.docx')
body_elements = list(doc._body._body)

print("=== ALL DRAWING ELEMENTS IN BAB IV ===")
for i in range(750, len(body_elements)):
    elem = body_elements[i]
    xml_str = etree.tostring(elem).decode('utf-8', errors='ignore')
    if 'w:drawing' in xml_str or 'w:pict' in xml_str:
        # Check prev 3 and next 3
        print(f"\nDrawing at body element #{i}:")
        for off in range(-3, 4):
            j = i + off
            if 0 <= j < len(body_elements):
                e = body_elements[j]
                t = e.tag.split('}')[-1]
                if t == 'p':
                    p_obj = docx.text.paragraph.Paragraph(e, doc)
                    txt = p_obj.text.strip()
                    has_seq = "SEQ" in etree.tostring(e).decode('utf-8', errors='ignore')
                    print(f"   [{j}] <p> (SEQ={has_seq}): '{txt[:75]}'")
                elif t == 'tbl':
                    print(f"   [{j}] <tbl>")
