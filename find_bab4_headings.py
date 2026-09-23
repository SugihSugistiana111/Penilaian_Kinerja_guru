import docx
from lxml import etree
from docx.oxml.ns import qn

doc = docx.Document('SKRIPSI.docx')
body_elements = list(doc._body._body)

print(f"Total body elements: {len(body_elements)}")
print()

# Cari semua heading dan tabel yang ada "BAB IV" atau style Heading1 atau Heading2 dengan "4."
print("=== Mencari semua Heading dan Section dengan BAB IV ===")
for i, elem in enumerate(body_elements):
    tag = elem.tag.split('}')[-1]
    if tag != 'p':
        continue
    
    text = ''.join(t.text or '' for t in elem.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t'))
    
    pPr = elem.find(qn('w:pPr'))
    style = ''
    if pPr is not None:
        pStyle = pPr.find(qn('w:pStyle'))
        if pStyle is not None:
            style = pStyle.get(qn('w:val'), '')
    
    # Cari heading yang ada angka 4.
    if 'Heading1' in style and ('4' in text or 'BAB IV' in text or 'BAB 4' in text):
        print(f"  [{i}] H1 | text={repr(text[:80])}")
    elif 'Heading2' in style and text.strip().startswith('4.'):
        print(f"  [{i}] H2 | text={repr(text[:80])}")
    elif 'Heading3' in style and text.strip().startswith('4.'):
        print(f"  [{i}] H3 | text={repr(text[:80])}")
    elif 'BAB IV' in text and 'BAB' in text:
        print(f"  [{i}] {style!r} | text={repr(text[:80])}")

print()

# Sekarang cari section 4.1, 4.2, 4.3 heading 
print("=== Paragraf dengan 4.1, 4.2, 4.3 heading ===")
for i, elem in enumerate(body_elements):
    tag = elem.tag.split('}')[-1]
    if tag != 'p':
        continue
    
    text = ''.join(t.text or '' for t in elem.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t'))
    
    pPr = elem.find(qn('w:pPr'))
    style = ''
    if pPr is not None:
        pStyle = pPr.find(qn('w:pStyle'))
        if pStyle is not None:
            style = pStyle.get(qn('w:val'), '')
    
    t = text.strip()
    if t.startswith('4.1') or t.startswith('4.2') or t.startswith('4.3') or t.startswith('4.4'):
        if 'Heading' in style or len(t) < 100:
            print(f"  [{i}] {style!r} | text={repr(t[:100])}")
