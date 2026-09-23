import docx
from lxml import etree
from docx.oxml.ns import qn

doc = docx.Document('SKRIPSI.docx')
body_elements = list(doc._body._body)

for j in range(820, min(860, len(body_elements))):
    e = body_elements[j]
    t = e.tag.split('}')[-1]
    if t == 'p':
        p_obj = docx.text.paragraph.Paragraph(e, doc)
        pPr = e.find(qn('w:pPr'))
        spacing = pPr.find(qn('w:spacing')) if pPr is not None else None
        sp_info = ""
        if spacing is not None:
            sp_info = f"before={spacing.get(qn('w:before'))} after={spacing.get(qn('w:after'))}"
        pagebreak = "PAGEBREAK" if 'w:br' in etree.tostring(e).decode() or 'w:pageBreakBefore' in etree.tostring(e).decode() else ""
        print(f"[{j}] <p> {pagebreak} {sp_info}: '{p_obj.text[:70]}'")
    elif t == 'tbl':
        tbl_obj = docx.table.Table(e, doc)
        rows_cnt = len(tbl_obj.rows)
        tr0 = tbl_obj.rows[0]._tr
        trPr = tr0.find(qn('w:trPr'))
        tblHeader = trPr.find(qn('w:tblHeader')) if trPr is not None else None
        cantSplit = trPr.find(qn('w:cantSplit')) if trPr is not None else None
        has_tblH = tblHeader is not None
        has_cant = cantSplit is not None
        cell0 = tbl_obj.rows[0].cells[0].text.strip() if tbl_obj.rows else ""
        print(f"[{j}] <tbl> rows={rows_cnt}, header='{cell0}', tblHeader={has_tblH}, cantSplit={has_cant}")
