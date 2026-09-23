import docx

doc = docx.Document('SKRIPSI.docx')

markers = [
    "AD-15",
    "SD-04",
    "SD-07",
    "SD-10",
    "SD-12",
    "Dashboard & Profil Mandiri"
]

for m in markers:
    print(f"--- Marker: {m} ---")
    for i, p in enumerate(doc.paragraphs):
        if m in p.text:
            print(f"  P{i}: '{p.text[:70]}'")
