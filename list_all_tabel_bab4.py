import docx
from lxml import etree

doc = docx.Document('SKRIPSI.docx')
body_elements = list(doc._body._body)

def get_text(elem):
    return ''.join(t.text or '' for t in elem.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t'))

count = 0
for i, elem in enumerate(body_elements):
    tag = elem.tag.split('}')[-1]
    if tag != 'p':
        continue
    xml = etree.tostring(elem).decode('utf-8', errors='ignore')
    if 'SEQ Tabel' in xml:
        count += 1
        text = get_text(elem)
        if i >= 784:
            print(f"BAB IV Tabel #{count} (elem {i}): {text}")

print(f"\nTotal Tabel captions in BAB IV: {count - 39}")
