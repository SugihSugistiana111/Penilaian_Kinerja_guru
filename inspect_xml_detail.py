import docx
from lxml import etree
from docx.oxml.ns import qn

doc = docx.Document('SKRIPSI.docx')
body_elements = list(doc._body._body)

print("=== XML detail element [789] (Heading2 Kebutuhan Perancangan) ===")
print(etree.tostring(body_elements[789], pretty_print=True).decode('utf-8', errors='ignore')[:1000])
print()

print("=== XML detail element [790] (Tabel 4.1) ===")
print(etree.tostring(body_elements[790], pretty_print=True).decode('utf-8', errors='ignore')[:2000])
print()

print("=== XML detail element [791] (Table after 4.1) - first few rows ===")
tbl = body_elements[791]
rows = tbl.findall('.//' + qn('w:tr'))
print(f"Total rows: {len(rows)}")
print("Row 0:")
print(etree.tostring(rows[0], pretty_print=True).decode('utf-8', errors='ignore')[:500])
print()

print("=== XML detail element [792] (Tabel 4.2) ===")
print(etree.tostring(body_elements[792], pretty_print=True).decode('utf-8', errors='ignore')[:2000])
print()

print("=== XML detail element [793] (Table after 4.2) - first row ===")
tbl2 = body_elements[793]
rows2 = tbl2.findall('.//' + qn('w:tr'))
print(f"Total rows: {len(rows2)}")
print()

print("=== XML detail element [794] ===")
print(etree.tostring(body_elements[794], pretty_print=True).decode('utf-8', errors='ignore')[:500])
print()

print("=== XML detail element [802] (Tabel 4.3 - bermasalah) ===")
print(etree.tostring(body_elements[802], pretty_print=True).decode('utf-8', errors='ignore')[:3000])
