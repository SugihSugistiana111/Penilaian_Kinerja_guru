import docx
import re

doc = docx.Document('SKRIPSI.docx')

# Remove duplicate old tabel captions like "Tabel 4.1 Struktur Tabel Role"
# (which don't have bold or have redundant numbers)
removed = 0
for p in list(doc.paragraphs):
    t = p.text.strip()
    if re.match(r'^Tabel 4\.\d+\s+Struktur Tabel', t):
        p._p.getparent().remove(p._p)
        removed += 1
        print(f"Removed old duplicate: {t}")
    elif t == "Tabel 4. Identifikasi Aktor" or t == "Tabel 4. Deskripsi Use Case":
        # Check if another one exists right next to it
        pass

# Also remove any redundant "Tabel 4. 3 Identifikasi Aktor" or "Tabel 4. 5 Deskripsi Use Case"
for p in list(doc.paragraphs):
    t = p.text.strip()
    if t.startswith("Tabel 4. 3 Identifikasi Aktor") or t.startswith("Tabel 4. 5 Deskripsi Use Case"):
        p._p.getparent().remove(p._p)
        removed += 1
        print(f"Removed redundant caption: {t}")

print(f"Removed {removed} duplicates")
doc.save('SKRIPSI.docx')
print("SKRIPSI.docx saved!")
