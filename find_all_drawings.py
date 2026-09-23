import docx
from lxml import etree
from docx.oxml.ns import qn

doc = docx.Document('SKRIPSI.docx')

print("=== ALL DRAWINGS IN BAB IV (P700 onwards) ===")
body_elements = list(doc._body._body)

for i, elem in enumerate(body_elements):
    tag = elem.tag.split('}')[-1]
    xml_str = etree.tostring(elem).decode('utf-8', errors='ignore')
    
    if 'w:drawing' in xml_str or 'w:pict' in xml_str:
        # It's a drawing! Let's look at context: 3 elements before and 3 elements after
        print(f"\n--- Drawing Element #{i} ---")
        for off in range(-3, 4):
            j = i + off
            if 0 <= j < len(body_elements):
                e = body_elements[j]
                t = e.tag.split('}')[-1]
                if t == 'p':
                    p_obj = docx.text.paragraph.Paragraph(e, doc)
                    txt = p_obj.text.strip()
                    has_seq = "SEQ" in etree.tostring(e).decode('utf-8', errors='ignore')
                    print(f"   [{j}] <p> (SEQ={has_seq}): '{txt[:70]}'")
                elif t == 'tbl':
                    print(f"   [{j}] <tbl>")
