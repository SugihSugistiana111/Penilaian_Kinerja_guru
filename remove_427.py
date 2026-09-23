import docx

doc = docx.Document('SKRIPSI.docx')

for p in list(doc.paragraphs):
    t = p.text.strip()
    if 'Gambar 4.27' in t:
        p._p.getparent().remove(p._p)
        print(f"Removed: {t}")

doc.save('SKRIPSI.docx')
print("SKRIPSI.docx updated!")
