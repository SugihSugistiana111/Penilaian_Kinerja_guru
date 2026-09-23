import docx

def inspect_styles(docx_path):
    doc = docx.Document(docx_path)
    print(f"=== {docx_path} ===")
    for p in doc.paragraphs[:25]:
        if p.text.strip():
            font_names = set([r.font.name for r in p.runs if r.font.name])
            font_sizes = set([r.font.size.pt for r in p.runs if r.font.size])
            bolds = set([r.bold for r in p.runs])
            print(f"[{p.style.name}] (align={p.alignment}, font={font_names}, size={font_sizes}, bold={bolds}): '{p.text}'")

inspect_styles('BAB V.docx')
inspect_styles('SKRIPSI_Sempurna.docx')
