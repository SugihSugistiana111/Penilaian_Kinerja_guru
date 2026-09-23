import docx

doc = docx.Document('SKRIPSI.docx')
for i in range(838, 901):
    p = doc.paragraphs[i]
    has_img = 'w:drawing' in p._p.xml or 'w:pict' in p._p.xml
    txt = p.text.strip()
    print(f'P{i}: "{txt}" | HasImage: {has_img}')
