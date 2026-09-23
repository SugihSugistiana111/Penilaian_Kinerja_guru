import docx

doc = docx.Document('SKRIPSI.docx')

print("=== VERIFIKASI 37 TABEL BAB IV ===")
count = 0
for i, p in enumerate(doc.paragraphs):
    xml = p._p.xml
    txt = p.text.strip()
    if 'SEQ Tabel' in xml and i > 740:
        count += 1
        runs_info = []
        for r in p.runs:
            runs_info.append(f"'{r.text}'(bold={r.font.bold})")
        print(f"{count:2d}. P{i}: {txt} | {' + '.join(runs_info)}")

print(f"\nTotal Tabel di BAB IV: {count} (Target: 37)")
