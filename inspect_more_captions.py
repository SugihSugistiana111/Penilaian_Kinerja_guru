import docx

for fn in ['Bab4_Perancangan_Antarmuka.docx', 'SKRIPSI_Sempurna.docx']:
    try:
        doc = docx.Document(fn)
        print(f"=== {fn} ===")
        found = 0
        for i, p in enumerate(doc.paragraphs):
            if 'Gambar 4.' in p.text or 'Gambar 5.' in p.text or 'Tabel 4.' in p.text or 'Tabel 5.' in p.text:
                print(f"  P{i} [{p.style.name}] (align={p.alignment}): '{p.text}'")
                found += 1
                if found >= 10:
                    break
    except Exception as e:
        print(f"Error {fn}: {e}")
