import docx
from lxml import etree

doc = docx.Document('SKRIPSI.docx')
body = doc._body._body

print("Searching for drawings in the entire document:")
for i, elem in enumerate(body):
    xml_s = etree.tostring(elem).decode('utf-8', errors='ignore')
    if 'w:drawing' in xml_s or 'w:pict' in xml_s:
        # get text of paragraph or surrounding
        txt = ""
        for off in range(-1, 2):
            if 0 <= i + off < len(body):
                e = body[i+off]
                if e.tag.endswith('p'):
                    p_obj = docx.text.paragraph.Paragraph(e, doc)
                    if p_obj.text.strip():
                        txt += f" | {p_obj.text.strip()[:35]}"
        print(f"Drawing #{i}: {txt}")
