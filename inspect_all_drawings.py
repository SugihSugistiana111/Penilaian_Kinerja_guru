import docx
from lxml import etree

doc = docx.Document('SKRIPSI.docx')
body = doc._body._body

print("Inspect all drawings:")
drawings = []
for i, elem in enumerate(body):
    xml_s = etree.tostring(elem).decode('utf-8', errors='ignore')
    if 'w:drawing' in xml_s or 'w:pict' in xml_s:
        # Check if BAB IV
        # Find context
        ctx = ""
        for off in range(-2, 3):
            if 0 <= i + off < len(body):
                e = body[i+off]
                if e.tag.endswith('p'):
                    p = docx.text.paragraph.Paragraph(e, doc)
                    if p.text.strip():
                        ctx += f" [{p.text.strip()[:30]}]"
        print(f"Drawing #{i}: {ctx}")
