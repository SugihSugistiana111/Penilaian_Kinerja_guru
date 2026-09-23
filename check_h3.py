import docx
from docx.oxml.ns import qn

doc = docx.Document('SKRIPSI_Sempurna.docx')
for i, p in enumerate(doc.paragraphs):
    if p.style.name.startswith('Heading'):
        pPr = p._p.pPr
        numPr_str = "None"
        if pPr is not None:
            numPr = pPr.find(qn('w:numPr'))
            if numPr is not None:
                ilvl = numPr.find(qn('w:ilvl'))
                numId = numPr.find(qn('w:numId'))
                numPr_str = f"ilvl={ilvl.get(qn('w:val')) if ilvl is not None else '?'}, numId={numId.get(qn('w:val')) if numId is not None else '?'}"
        print(f"P{i} [{p.style.name}] (numPr={numPr_str}): '{p.text}'")
        if i > 60:
            break
