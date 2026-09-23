import docx

doc = docx.Document('SKRIPSI_Sempurna.docx')
for i, p in enumerate(doc.paragraphs):
    if p.text.startswith('Gambar') or p.text.startswith('Tabel'):
        print(f"P{i} [{p.style.name}]: {p.text}")
        if i > 50:
            break
