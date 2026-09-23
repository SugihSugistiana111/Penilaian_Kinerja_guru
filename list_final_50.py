import docx

doc = docx.Document('SKRIPSI.docx')

print("=== 50 CAPTIONS IN EXACT ORDER ===")
count = 0
for i, p in enumerate(doc.paragraphs):
    xml = p._p.xml
    if 'SEQ Gambar' in xml and i > 700:
        count += 1
        print(f"{count:2d}. {p.text.strip()}")

print(f"Total: {count}")
