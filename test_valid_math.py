import docx
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

def create_valid_math_doc():
    doc = docx.Document()
    
    # In OpenXML Word:
    # A display equation paragraph is <w:p><w:pPr><w:jc w:val="center"/></w:pPr><m:oMathPara><m:oMath>...</m:oMath></m:oMathPara></w:p>
    # or inside a paragraph: paragraph._p.append(parse_xml(r'<m:oMathPara ...>'))
    p = doc.add_paragraph()
    p.paragraph_format.space_before = docx.shared.Pt(6)
    p.paragraph_format.space_after = docx.shared.Pt(6)
    p.alignment = docx.enum.text.WD_ALIGN_PARAGRAPH.CENTER
    
    omml = r'''
    <m:oMathPara %s>
        <m:oMath>
            <m:sSub>
                <m:e><m:r><m:t>x*</m:t></m:r></m:e>
                <m:sub><m:r><m:t>ij</m:t></m:r></m:sub>
            </m:sSub>
            <m:r><m:t> = </m:t></m:r>
            <m:f>
                <m:num>
                    <m:sSub>
                        <m:e><m:r><m:t>x</m:t></m:r></m:e>
                        <m:sub><m:r><m:t>ij</m:t></m:r></m:sub>
                    </m:sSub>
                </m:num>
                <m:den>
                    <m:rad>
                        <m:radPr><m:degHide m:val="1"/></m:radPr>
                        <m:deg/>
                        <m:e>
                            <m:nary>
                                <m:naryPr>
                                    <m:chr m:val="∑"/>
                                    <m:limLoc m:val="undOvr"/>
                                </m:naryPr>
                                <m:sub><m:r><m:t>i=1</m:t></m:r></m:sub>
                                <m:sup><m:r><m:t>m</m:t></m:r></m:sup>
                                <m:e>
                                    <m:sSup>
                                        <m:e>
                                            <m:sSub>
                                                <m:e><m:r><m:t>x</m:t></m:r></m:e>
                                                <m:sub><m:r><m:t>ij</m:t></m:r></m:sub>
                                            </m:sSub>
                                        </m:e>
                                        <m:sup><m:r><m:t>2</m:t></m:r></m:sup>
                                    </m:sSup>
                                </m:e>
                            </m:nary>
                        </m:e>
                    </m:rad>
                </m:den>
            </m:f>
        </m:oMath>
    </m:oMathPara>
    ''' % nsdecls("m")
    
    elem = parse_xml(omml)
    p._p.append(elem)
    
    doc.save("test_valid_math.docx")
    print("test_valid_math.docx created successfully!")

if __name__ == "__main__":
    create_valid_math_doc()
