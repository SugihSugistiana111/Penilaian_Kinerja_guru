import docx

doc = docx.Document('SKRIPSI.docx')

print("=== VERIFIKASI SELURUH CAPTION GAMBAR DI BAB IV ===")
count = 0
for i, p in enumerate(doc.paragraphs):
    xml = p._p.xml
    if 'SEQ Gambar' in xml and i > 700:
        count += 1
        runs_info = []
        for r in p.runs:
            runs_info.append(f"'{r.text}'(bold={r.font.bold}, size={r.font.size.pt if r.font.size else None})")
        print(f"#{count} P{i}: {p.text} | {' + '.join(runs_info)}")

print(f"\nTotal Caption Gambar di BAB IV: {count} (Target: 50)")
