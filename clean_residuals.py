import docx
from lxml import etree

doc = docx.Document('SKRIPSI.docx')
body = doc._body._body

# Find and remove any residual double caption paragraphs
for p in list(doc.paragraphs):
    t = p.text.strip()
    # Check if this paragraph is a residual caption
    if t.startswith('Gambar 4.30 ') or t.startswith('Gambar 4.34 ') or t.startswith('Gambar 4.37 ') or t.startswith('Gambar 4.40 ') or t.startswith('Gambar 4.42 '):
        p._p.getparent().remove(p._p)
        print(f"Removed residual caption: {t}")

doc.save('SKRIPSI.docx')
print("[SUCCESS] Residual captions removed!")
