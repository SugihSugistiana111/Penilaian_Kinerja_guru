import docx
import re

doc = docx.Document('SKRIPSI.docx')

# Remove duplicate unnumbered captions at P747, P750, P768
for p in list(doc.paragraphs):
    t = p.text.strip()
    if t == "Tabel 4. Kebutuhan Perangkat Keras" or t == "Tabel 4. Kebutuhan Perangkat Lunak" or t == "Tabel 4. Deskripsi Use Case":
        # Check if the next paragraph or previous is also a caption
        p._p.getparent().remove(p._p)
        print(f"Removed unnumbered duplicate: {t}")

doc.save('SKRIPSI.docx')
print("SKRIPSI.docx saved!")
