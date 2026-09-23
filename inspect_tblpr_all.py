import docx
from lxml import etree
from docx.oxml.ns import qn

doc = docx.Document('SKRIPSI.docx')
body_elements = list(doc._body._body)

tbl_elem = body_elements[826]
tblPr = tbl_elem.find(qn('w:tblPr'))
print("tblPr XML:\n", etree.tostring(tblPr, pretty_print=True).decode())

# Check all rows in tbl_elem
for idx, row in enumerate(tbl_elem.findall(qn('w:tr'))):
    trPr = row.find(qn('w:trPr'))
    trPr_str = etree.tostring(trPr).decode() if trPr is not None else "None"
    print(f"Row {idx} trPr: {trPr_str}")
