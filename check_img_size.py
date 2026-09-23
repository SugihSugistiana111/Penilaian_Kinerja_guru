import docx

doc = docx.Document('Bab4_Perancangan_Antarmuka.docx')
for i, p in enumerate(doc.paragraphs):
    for r in p.runs:
        if 'graphic' in r._r.xml:
            print(f"P{i} has image. Paragraph text: '{p.text}'")
            # check width
            for node in r._r.xpath('.//a:ext'):
                cx = node.get('cx')
                cy = node.get('cy')
                if cx and cy:
                    print(f"  Image size: cx={cx} ({int(cx)/914400:.2f} in, {int(cx)/360000:.2f} cm), cy={cy} ({int(cy)/914400:.2f} in, {int(cy)/360000:.2f} cm)")
