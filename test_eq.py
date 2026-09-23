import docx
from docx.oxml import parse_xml

doc = docx.Document()
p = doc.add_paragraph()
omml = r'''
<m:oMathPara xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math">
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
'''
elem = parse_xml(omml)
doc._body._body.append(elem)
doc.save('test_equation.docx')
print('OMML equation test successful!')
