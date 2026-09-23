import docx
from docx.oxml import OxmlElement
from fast_fix_tables import set_table_caption

doc = docx.Document('SKRIPSI.docx')
body = doc._body._body

# Find table with header "Kode" or "Deskripsi Use Case"
for i, elem in enumerate(body):
    if elem.tag.endswith('tbl'):
        tbl_obj = docx.table.Table(elem, doc)
        if len(tbl_obj.rows) > 0:
            first_row_text = " ".join([c.text.strip() for c in tbl_obj.rows[0].cells])
            # Check if this is the Deskripsi Use Case table (16 rows, UC-01, etc.)
            if len(tbl_obj.rows) == 16 and "Kode" in first_row_text:
                print(f"Found Deskripsi Use Case table at body element #{i}: {first_row_text}")
                # Check previous paragraph
                prev_elem = body[i-1]
                p_prev = docx.text.paragraph.Paragraph(prev_elem, doc)
                print(f"  Prev paragraph: '{p_prev.text}'")
                
                # If prev paragraph is NOT already Tabel 4.5, insert it!
                if "Deskripsi Use Case" not in p_prev.text:
                    new_p = OxmlElement('w:p')
                    elem.addprevious(new_p)
                    new_para = docx.text.paragraph.Paragraph(new_p, doc)
                    set_table_caption(new_para, 5, "Deskripsi Use Case")
                    print("Inserted Tabel 4.5 Deskripsi Use Case before the table!")
                else:
                    set_table_caption(p_prev, 5, "Deskripsi Use Case")

doc.save('SKRIPSI.docx')
print("[SUCCESS] SKRIPSI.docx saved!")
