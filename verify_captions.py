import docx

doc = docx.Document('SKRIPSI.docx')
paragraphs = doc.paragraphs

print("=== Verifying captions after fix ===")
print()

tabel_count = 0
gambar_count = 0

for i, p in enumerate(paragraphs):
    xml = p._p.xml
    if 'SEQ Tabel' in xml:
        tabel_count += 1
        print(f"Tabel #{tabel_count} at P{i}: {p.text[:90]}")
        # Check bold
        for run in p.runs:
            print(f"  Run: '{run.text[:40]}' bold={run.font.bold} font={run.font.name} size={run.font.size}")
    elif 'SEQ Gambar' in xml:
        gambar_count += 1
        print(f"Gambar #{gambar_count} at P{i}: {p.text[:90]}")

print(f"\nTotal: {tabel_count} Tabel SEQ, {gambar_count} Gambar SEQ")
