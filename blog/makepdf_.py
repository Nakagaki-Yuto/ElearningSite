# -*- coding:utf-8 -*-

import time
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont

def make(filename,trans_data):
    doc = SimpleDocTemplate(filename,pagesize=A4,
                            rightMargin=72,leftMargin=72,
                            topMargin=72,bottomMargin=18)

    pdfmetrics.registerFont(UnicodeCIDFont("HeiseiKakuGo-W5"))

    Story=[]
    styles=getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))

    ptext = '<font size=12> ' + trans_data + ' </font>'
    #ptext.replace('\n','<br/>')
    print(ptext)

    Story.append(Paragraph(ptext, styles["Normal"]))
    doc.build(Story)
