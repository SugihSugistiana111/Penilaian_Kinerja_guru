import docx

doc = docx.Document('SKRIPSI.docx')

# Remove duplicate adjacent captions
to_remove = []
seen_captions = set()

for i, p in enumerate(doc.paragraphs):
    xml = p._p.xml
    txt = p.text.strip()
    if 'SEQ Tabel' in xml and i > 740:
        if i == 748 or i == 750 or i == 1035 or i == 1089:
            to_remove.append(p)
            print(f"Removing duplicate at P{i}: {txt}")

for p in to_remove:
    p._p.getparent().remove(p._p)

doc.save('SKRIPSI.docx')
print(f"Removed {len(to_remove)} duplicate table captions.")
