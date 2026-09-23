import docx
from lxml import etree
from docx.oxml.ns import qn

doc = docx.Document('SKRIPSI.docx')
body_elements = list(doc._body._body)

tbl_elem = body_elements[826]
print("Tbl tag:", tbl_elem.tag)

# Check tblPr
tblPr = tbl_elem.find(qn('w:tblPr'))
if tblPr is not None:
    print("tblPr XML:\n", etree.tostring(tblPr, pretty_print=True).decode())

# Check first row trPr
tr0 = tbl_elem.find(qn('w:tr'))
if tr0 is not None:
    trPr0 = tr0.find(qn('w:trPr'))
    if trPr0 is not None:
        print("trPr0 XML:\n", etree.tostring(trPr0, pretty_print=True).decode())

# Check row 0 cell 0 paragraphs
for r_idx, row in enumerate(tbl_elem.findall(qn('w:tr'))[:3]):
    c0 = row.find(qn('w:tc'))
    if c0 is not None:
        p0 = c0.find(qn('w:p'))
        if p0 is not None:
            pPr = p0.find(qn('w:pPr'))
            pPr_xml = etree.tostring(pPr).decode() if pPr is not None else "None"
            txt = "".join([t.text for t in p0.findall('.//' + qn('w:t')) if t.text])
            print(f"Row {r_idx} cell 0 text='{txt}' | pPr: {pPr_xml}")

# Also check caption paragraph [825]
p_cap = body_elements[825]
print("Caption [825] XML:\n", etree.tostring(p_cap, pretty_print=True).decode())
