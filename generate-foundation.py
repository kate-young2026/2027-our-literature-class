from pathlib import Path
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer

ROOT=Path(__file__).resolve().parent
pdfmetrics.registerFont(TTFont('Malgun','C:/Windows/Fonts/malgun.ttf'))
pdfmetrics.registerFont(TTFont('MalgunBold','C:/Windows/Fonts/malgunbd.ttf'))
title=ParagraphStyle('title',fontName='MalgunBold',fontSize=19,leading=28,spaceAfter=14,wordWrap='CJK')
head=ParagraphStyle('head',fontName='MalgunBold',fontSize=12,leading=18,spaceBefore=10,spaceAfter=5,textColor=colors.HexColor('#99473d'),wordWrap='CJK')
body=ParagraphStyle('body',fontName='Malgun',fontSize=10,leading=17,spaceAfter=6,wordWrap='CJK')
small=ParagraphStyle('small',fontName='Malgun',fontSize=8,leading=13,wordWrap='CJK')
def p(s,style=body): return Paragraph(s,style)
def footer(canvas,doc):
 canvas.setFont('Malgun',8);canvas.drawString(20*mm,13*mm,'2027 우리들의 문학수업');canvas.drawRightString(190*mm,13*mm,str(doc.page))
def build(name,story): SimpleDocTemplate(str(ROOT/'pdf'/name),pagesize=(210*mm,297*mm),leftMargin=20*mm,rightMargin=20*mm,topMargin=20*mm,bottomMargin=20*mm).build(story,onFirstPage=footer,onLaterPages=footer)
prefix=[p('첫 시간 · 고1 · 50분',small),Spacer(1,4*mm),p('문학의 기초: 네 갈래와 작품의 구성',title)]
study=prefix+[p('오늘의 목표',head),p('서정·서사·극·교술의 특징을 구분하고 작품의 구성 요소가 의미를 만드는 방식을 설명한다.'),p('문학의 네 갈래',head),p('<b>서정</b>: 화자의 감정과 생각을 운율, 이미지, 비유 등으로 압축해 표현한다. 예: 시조, 현대시.'),p('<b>서사</b>: 인물에게 일어나는 사건을 시간과 공간을 배경으로 서술자가 전달한다. 예: 소설, 설화.'),p('<b>극</b>: 인물의 대사와 행동으로 사건을 보여 주며 지시문과 장면 구성을 활용한다. 예: 희곡, 시나리오.'),p('<b>교술</b>: 글쓴이가 실제 경험과 관찰을 바탕으로 생각과 깨달음을 비교적 직접적으로 전한다. 예: 수필.'),p('작품의 구성',head),p('주제는 작품이 전달하는 중심 생각이다. 소재·표현·구성은 서로 관계를 맺으며 주제를 드러낸다.'),p('서정: 화자·상황·정서·태도와 시어·심상·운율 / 서사: 인물·사건·배경·서술자·시점 / 극: 인물·갈등·대사·행동·지시문 / 교술: 글쓴이의 경험·관찰·생각과 표현'),p('기억하기',head),p('네 갈래는 작품을 이해하기 위한 분류이며 실제 작품에는 여러 갈래의 특성이 섞일 수 있다.'),p('출처: 경기도교육청, 2022 개정 국어과 성취평가 자료, 공통국어1 문학 영역.',small)]
worksheet=prefix+[p('학년·반: __________  번호: __________  이름: __________________',small),p('활동 1. 네 갈래 구별하기',head),p('화자의 정서가 중심이 되는 갈래: __________ / 인물의 대사와 행동이 중심이 되는 갈래: __________'),p('인물과 사건을 서술자가 전하는 갈래: __________ / 관찰과 생각을 비교적 직접 전하는 갈래: __________'),p('활동 2. 같은 상황, 다른 표현',head),p('‘비 오는 귀갓길’을 서정과 극의 방식으로 각각 표현해 보자.'),p('서정: __________________________________________________________________________'),p('_______________________________________________________________________________'),p('극: ____________________________________________________________________________'),p('_______________________________________________________________________________'),p('활동 3. 서사의 구성 요소',head),p('직접 만든 짧은 이야기를 바탕으로 인물·사건·배경을 적고, 한 요소가 바뀌면 의미가 어떻게 달라질지 설명하자.'),p('인물: __________________ 사건: __________________ 배경: __________________'),p('바꾼 요소와 효과: ______________________________________________________________'),p('_______________________________________________________________________________'),p('마무리',head),p('네 갈래 중 하나를 선택해 표현 방식과 효과를 한 문장으로 설명하자.'),p('_______________________________________________________________________________'),p('자기평가: □ 네 갈래의 특징을 설명할 수 있다  □ 작품 구성 요소의 관계를 생각했다',small)]
build('foundation-study.pdf',study);build('foundation-worksheet.pdf',worksheet)
print('Created foundation study and worksheet PDFs')
