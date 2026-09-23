import docx

doc = docx.Document('BAB V.docx')
for i, p in enumerate(doc.paragraphs):
    print(f"P{i} [{p.style.name}]: text='{p.text}'")
    pPr = p._p.pPr
    if pPr is not None:
        numPr = pPr.find('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}numPr')
        if numPr is not None:
            print(f"   has numPr: {docx.oxml.xmlchemy.OxmlElement(numPr).xml if hasattr(numPr, 'xml') else 'numPr present'}")
