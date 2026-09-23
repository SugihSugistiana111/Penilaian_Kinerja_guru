import docx
from lxml import etree
from docx.oxml.ns import qn

doc = docx.Document('SKRIPSI.docx')
body_elements = list(doc._body._body)

print(f"Total body elements: {len(body_elements)}")

for i in range(len(body_elements) - 1):
    e1 = body_elements[i]
    e2 = body_elements[i+1]
    
    t1 = e1.tag.split('}')[-1]
    t2 = e2.tag.split('}')[-1]
    
    # Check if e1 is a caption paragraph
    if t1 == 'p':
        xml_str = etree.tostring(e1).decode()
        if "SEQ Tabel" in xml_str:
            p_obj = docx.text.paragraph.Paragraph(e1, doc)
            cap_text = p_obj.text.strip()
            
            # Check e2
            if t2 == 'tbl':
                tbl_obj = docx.table.Table(e2, doc)
                tblPr = e2.find(qn('w:tblPr'))
                tblpPr = tblPr.find(qn('w:tblpPr')) if tblPr is not None else None
                is_floating = tblpPr is not None
                
                tr0 = tbl_obj.rows[0]._tr
                trPr0 = tr0.find(qn('w:trPr'))
                tblHeader = trPr0.find(qn('w:tblHeader')) if trPr0 is not None else None
                has_tblHeader = tblHeader is not None
                
                # Check keep_with_next on caption
                pPr = e1.find(qn('w:pPr'))
                kwn = pPr.find(qn('w:keepNext')) if pPr is not None else None
                has_kwn = kwn is not None
                
                print(f"Caption [{i}]: '{cap_text}' -> Table [{i+1}] (rows={len(tbl_obj.rows)}):")
                print(f"   Floating={is_floating}, tblHeader={has_tblHeader}, keepNext={has_kwn}")
            else:
                # e2 is NOT a table! There's something in between!
                print(f"Caption [{i}]: '{cap_text}' -> NEXT IS <{t2}> (NOT A TABLE!)")
                # print next 3 elements
                for off in range(1, 4):
                    if i + off < len(body_elements):
                        eo = body_elements[i+off]
                        to = eo.tag.split('}')[-1]
                        if to == 'p':
                            po = docx.text.paragraph.Paragraph(eo, doc)
                            print(f"      + {off} <p>: '{po.text[:60]}'")
                        elif to == 'tbl':
                            to_obj = docx.table.Table(eo, doc)
                            print(f"      + {off} <tbl>: rows={len(to_obj.rows)}")
