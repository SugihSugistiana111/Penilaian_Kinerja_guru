import docx
from docx.oxml.ns import qn

doc = docx.Document('SKRIPSI.docx')

# Let's inspect elements in doc._body._body around P778
body_elements = list(doc._body._body)

from lxml import etree

for idx, elem in enumerate(body_elements):
    tag = elem.tag.split('}')[-1]
    xml_str = etree.tostring(elem).decode('utf-8', errors='ignore')
    if "Deskripsi Use Case" in xml_str or "UC-01" in xml_str:
        print(f"Body element #{idx}: <{tag}>")
        # print surrounding 5 elements
        for offset in range(-2, 5):
            j = idx + offset
            if 0 <= j < len(body_elements):
                e = body_elements[j]
                t = e.tag.split('}')[-1]
                preview = ""
                if t == 'p':
                    p_obj = docx.text.paragraph.Paragraph(e, doc)
                    preview = p_obj.text[:70]
                    # check spacing
                    pPr = e.find(qn('w:pPr'))
                    spacing = pPr.find(qn('w:spacing')) if pPr is not None else None
                    sp_info = ""
                    if spacing is not None:
                        sp_info = f"before={spacing.get(qn('w:before'))} after={spacing.get(qn('w:after'))}"
                    pagebreak = "PAGEBREAK" if 'w:br' in e.xml or 'w:pageBreakBefore' in e.xml else ""
                    print(f"   [{j}] <p> {pagebreak} {sp_info}: '{preview}'")
                elif t == 'tbl':
                    tbl_obj = docx.table.Table(e, doc)
                    rows_cnt = len(tbl_obj.rows)
                    # Check first row tblHeader
                    tr0 = tbl_obj.rows[0]._tr
                    trPr = tr0.find(qn('w:trPr'))
                    tblHeader = trPr.find(qn('w:tblHeader')) if trPr is not None else None
                    cantSplit = trPr.find(qn('w:cantSplit')) if trPr is not None else None
                    has_tblH = tblHeader is not None
                    has_cant = cantSplit is not None
                    
                    # Also check first cell text
                    cell0 = tbl_obj.rows[0].cells[0].text.strip() if tbl_obj.rows else ""
                    print(f"   [{j}] <tbl> rows={rows_cnt}, header='{cell0}', tblHeader={has_tblH}, cantSplit={has_cant}")
        print("=" * 60)
        break
