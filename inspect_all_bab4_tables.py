import docx
from lxml import etree

doc = docx.Document('SKRIPSI.docx')

print("=== ALL TABLE CAPTIONS IN BAB IV ===")
count = 0
for i, p in enumerate(doc.paragraphs):
    xml = p._p.xml
    txt = p.text.strip()
    if ('SEQ Tabel' in xml or txt.startswith('Tabel 4.') or txt.startswith('Tabel 4 ')) and i > 700:
        count += 1
        runs_info = []
        for r in p.runs:
            runs_info.append(f"'{r.text}'(bold={r.font.bold})")
        print(f"#{count:2d} P{i}: {txt[:80]} | {' + '.join(runs_info)}")

print(f"\nTotal Table Captions in BAB IV: {count}")
